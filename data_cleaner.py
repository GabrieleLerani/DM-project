import csv
import html
import re
import os
from create_location import *



def clean_special_characters(text):
    # Decode HTML entities
    decoded_text = html.unescape(text)
    
    # Remove forward slashes that are not part of "n/a"
    cleaned_text = re.sub(r'(?<!n/a)/|/(?=n/a(,|$))', ' ', decoded_text)
    
    # Remove non-alphanumeric characters
    cleaned_text = ''.join(c if c.isalnum() or c.isspace() or c == ',' else ' ' for c in cleaned_text)
    
    # Remove multiple spaces and strip leading/trailing spaces
    cleaned_text = ' '.join(cleaned_text.split())

    cleaned_text = cleaned_text.replace('n a', 'n/a')
    return cleaned_text

def clean_row(row):
    cleaned_row = []
    cleaned_row.append(row[0]) # append user id
    
    # clean special characters
    cleaned_value = clean_special_characters(row[1])

    # remove \n "" and .
    cleaned_value = cleaned_value.replace('\n', '').replace('"', '').replace(".",'').strip()
    cleaned_row.append(cleaned_value)
    cleaned_row.append(row[2])
    return cleaned_row


def clean_user_file(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as input_file:
        reader = csv.reader(input_file)
        with open(output_filename, 'w', encoding='utf-8', newline='') as output_file:
            writer = csv.writer(output_file)
        
            for row in reader:
                
                cleaned_row = clean_row(row)
                writer.writerow(cleaned_row)
    
    print(f"CSV file '{input_filename}' cleaned and saved as '{output_filename}'.")
    merge_location_from_user("Cleaned_Users.csv", "Users_file.csv")


def merge_location_from_user(input_filename, output_filename):

    path = 'cleaned_dataset'
    if not os.path.exists(path):
        os.makedirs(path)
    output_path = os.path.join(path,output_filename)

    with open(input_filename, 'r', encoding='utf-8') as input_file:
        reader = csv.reader(input_file)
        
        # move to the next line to skip the first one
        next(reader)
        fieldnames = ['User-ID', 'Country', 'Province', 'Age']  # Select the desired columns
        
        with open(output_path, 'w', encoding='utf-8', newline='') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()  # Write the header
            
            for row in reader:
                line = get_location(row, with_user_id=True)
                # Write only the selected columns to the output file
                writer.writerow({'User-ID': line[0], 'Country': line[1], 'Province': line[2], 'Age': line[3]})

    print(f"CSV file created and saved as '{output_filename}'.")
    

def remove_book_image_url(input_filename, output_filename):

    path = 'cleaned_dataset'
    if not os.path.exists(path):
        os.makedirs(path)
    output_path = os.path.join(path,output_filename)

    with open(input_filename, 'r', encoding='utf-8') as input_file:
        reader = csv.reader(input_file)
        
        # move to the next line to skip the first one
        next(reader)
        fieldnames = ['ISBN','Book-Title','Book-Author','Year-Of-Publication','Publisher']  # Select the desired columns
        
        with open(output_path, 'w', encoding='utf-8', newline='') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()  # Write the header
            
            for row in reader:
                
                # Write only the selected columns to the output file
                
                writer.writerow({'ISBN': row[0], 'Book-Title': row[1], 'Book-Author': row[2], 'Year-Of-Publication': row[3], 'Publisher': row[4]})

    print(f"CSV file created and saved as '{output_filename}'.")
    

def clean_rating_file(input_filename, output_filename):
    path = 'cleaned_dataset'
    if not os.path.exists(path):
        os.makedirs(path)
    output_path = os.path.join(path,output_filename)
    
    with open(input_filename, 'r', encoding='utf-8') as input_file:
        reader = csv.reader(input_file)
        with open(output_path, 'w', encoding='utf-8', newline='') as output_file:

            fieldnames = ['User-ID', 'ISBN', 'Book-Rating']  # Select the desired columns
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()  # Write the header
            
            for row in reader:
                cleaned_row = clean_row(row)
                isbn = cleaned_row[1]
                if len(isbn) == 10:
                    print(cleaned_row)
                    pass
                    #writer.writerow({'User-ID': cleaned_row[0], 'ISBN': cleaned_row[1], 'Book-Rating': cleaned_row[2]})
                if "" in cleaned_row or '' in cleaned_row:
                    pass


    print(f"CSV file '{input_filename}' cleaned and saved as '{output_filename}'.")
    

if __name__ == '__main__':
    # clean_user_file('Users.csv','Cleaned_Users.csv')
    # create_location_file('Cleaned_Users.csv','Location.csv')
    # remove_book_image_url("Books.csv","Books_file.csv")

    clean_rating_file('Ratings.csv','Ratings_file.csv')