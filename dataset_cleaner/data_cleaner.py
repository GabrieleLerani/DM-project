import csv
import html
import re
import os
import pandas as pd
from create_location import *


dataset_path = "dataset"


def remove_quotes_in_pairs(row):
    count = 0
    for c in row:
        if c == "'":
            count += 1

    if count != 0 and count % 2 == 0:
        row = row.replace("'", "")
    return row


def clean_special_characters(text):
    # Decode HTML entities
    decoded_text = html.unescape(text)

    # Remove forward slashes that are not part of "n/a"
    cleaned_text = re.sub(r"(?<!n/a)/|/(?=n/a(,|$))", " ", decoded_text)

    # Remove non-alphanumeric characters
    cleaned_text = "".join(
        c if c.isalnum() or c.isspace() or c in ":,.'\"" else " " for c in cleaned_text
    )

    # Remove multiple spaces and strip leading/trailing spaces
    cleaned_text = " ".join(cleaned_text.split())

    cleaned_text = cleaned_text.replace("n a", "n/a")
    return cleaned_text


def clean_row(row, clean_book=False):
    cleaned_row = []
    if not clean_book:
        cleaned_row.append(row[0])  # append user id

        # clean special characters
        cleaned_value = clean_special_characters(row[1])

        # remove \n ""
        cleaned_value = cleaned_value.replace("\n", "").replace('"', "").strip()
        cleaned_row.append(cleaned_value)
        cleaned_row.append(row[2])

    else:
        for i in range(len(row)):
            if i > 0:
                cleaned_value = clean_special_characters(row[i])

                cleaned_value = cleaned_value.replace("\n", "").replace('"', "").strip()

                if i == 1:
                    cleaned_value = remove_quotes_in_pairs(cleaned_value)

                cleaned_row.append(
                    cleaned_value if "http" not in cleaned_value else None
                )

            else:
                cleaned_row.append(row[i] if "http" not in row[i] else None)

    return cleaned_row


def clean_user_file(input_filename, output_filename):
    path = "cleaned_dataset"
    if not os.path.exists(path):
        os.makedirs(path)
    output_path = os.path.join(path, output_filename)

    input_path = os.path.join(dataset_path, input_filename)

    with open(input_path, "r", encoding="utf-8") as input_file:
        reader = csv.reader(input_file)
        with open(output_path, "w", encoding="utf-8", newline="") as output_file:
            writer = csv.writer(output_file)

            for row in reader:
                cleaned_row = clean_row(row)

                # valid_location_pattern = r"^[a-zA-Z\s,]+"
                # match = re.match(valid_location_pattern, cleaned_row[1])
                # if match:
                # cleaned_row[1] = match.group()
                writer.writerow(cleaned_row)

    print(f"CSV file '{input_filename}' cleaned and saved as '{output_filename}'.")
    merge_location_from_user("Cleaned_Users.csv", "Users_file.csv")


def merge_location_from_user(input_filename, output_filename):
    path = "cleaned_dataset"
    if not os.path.exists(path):
        os.makedirs(path)
    output_path = os.path.join(path, output_filename)

    input_path = os.path.join(path, input_filename)

    with open(input_path, "r", encoding="utf-8") as input_file:
        reader = csv.reader(input_file)

        # move to the next line to skip the first one
        next(reader)
        fieldnames = [
            "User-ID",
            "Country",
            "Province",
            "Age",
        ]  # Select the desired columns

        with open(output_path, "w", encoding="utf-8", newline="") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()  # Write the header

            for row in reader:
                line = get_location(row, with_user_id=True)

                # don't add line with null value or with 6.a
                if None not in line and "6.a" not in line[2]:
                    # Write only the selected columns to the output file
                    writer.writerow(
                        {
                            "User-ID": line[0],
                            "Country": line[1],
                            "Province": line[2],
                            "Age": line[3],
                        }
                    )

    print(f"CSV file created and saved as '{output_filename}'.")


def clean_book_file(input_filename, output_filename):
    path = "cleaned_dataset"
    if not os.path.exists(path):
        os.makedirs(path)
    output_path = os.path.join(path, output_filename)

    input_path = os.path.join(dataset_path, input_filename)

    with open(input_path, "r", encoding="utf-8") as input_file:
        reader = csv.reader(input_file)

        # move to the next line to skip the first one
        next(reader)
        fieldnames = [
            "ISBN",
            "Book-Title",
            "Book-Author",
            "Year-Of-Publication",
            "Publisher",
        ]  # Select the desired columns

        with open(output_path, "w", encoding="utf-8", newline="") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()  # Write the header

            for row in reader:
                cleaned_row = clean_row(row[:5], clean_book=True)
                isbn = cleaned_row[0]

                if len(isbn) == 10 and None not in cleaned_row:
                    writer.writerow(
                        {
                            "ISBN": cleaned_row[0],
                            "Book-Title": cleaned_row[1],
                            "Book-Author": cleaned_row[2],
                            "Year-Of-Publication": cleaned_row[3],
                            "Publisher": cleaned_row[4],
                        }
                    )

    print(f"CSV file created and saved as '{output_filename}'.")


def clean_rating_file(input_filename, output_filename):
    path = "cleaned_dataset"
    if not os.path.exists(path):
        os.makedirs(path)
    output_path = os.path.join(path, output_filename)

    input_path = os.path.join(dataset_path, input_filename)

    with open(input_path, "r", encoding="utf-8") as input_file:
        reader = csv.reader(input_file)
        with open(output_path, "w", encoding="utf-8", newline="") as output_file:
            fieldnames = [
                "User-ID",
                "ISBN",
                "Book-Rating",
            ]  # Select the desired columns
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()  # Write the header

            for row in reader:
                cleaned_row = clean_row(row)
                isbn = cleaned_row[1]
                if len(isbn) == 10:
                    writer.writerow(
                        {
                            "User-ID": cleaned_row[0],
                            "ISBN": cleaned_row[1],
                            "Book-Rating": cleaned_row[2],
                        }
                    )

    print(f"CSV file '{input_filename}' cleaned and saved as '{output_filename}'.")


def ensure_constraint_file(rating_filename, book_filename, user_filename):
    path = "cleaned_dataset"
    if not os.path.exists(path):
        os.makedirs(path)
    rating_path = os.path.join(path, rating_filename)
    book_path = os.path.join(path, book_filename)
    user_path = os.path.join(path, user_filename)

    # Load the book and rating CSV files into DataFrames
    book_df = pd.read_csv(book_path, encoding="utf-8")
    rating_df = pd.read_csv(rating_path, encoding="utf-8")
    user_df = pd.read_csv(user_path, encoding="utf-8")

    # Create a set of unique ISBN values from the book DataFrame
    valid_isbns = set(book_df["ISBN"])
    valid_userId = set(user_df["User-ID"])

    # Filter the rating DataFrame to keep only rows with valid ISBNs
    filtered_rating_df = rating_df[
        (rating_df["ISBN"].isin(valid_isbns))
        & (rating_df["User-ID"].isin(valid_userId))
    ]

    # Save the filtered rating DataFrame to a new CSV file
    filtered_rating_df.to_csv(
        os.path.join(path, "Filtered_rating_file.csv"), index=False, encoding="utf-8"
    )

    print("Filtered rating CSV saved as 'Filtered_rating.csv'")


if __name__ == "__main__":
    clean_user_file("Users.csv", "Cleaned_Users.csv")
    create_location_file("Cleaned_Users.csv", "Location.csv")
    clean_book_file("Books.csv", "Books_file.csv")
    clean_rating_file("Ratings.csv", "Ratings_file.csv")
    ensure_constraint_file("Ratings_file.csv", "Books_file.csv", "Users_file.csv")
