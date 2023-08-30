import csv
import os

fields = ['Country','Province']


def clean_location(location):

    # remove duplicate to have location of the same length for every user-id
    location = list(dict.fromkeys(location))
        
    # remove line space
    location = [elem.strip() for elem in location]

    # remove '' from line if there is
    if '' in location:
        location.remove('')

    if ' ' in location:
        location.remove(' ')

    return location 

def get_location(row, with_user_id = False):

    location = row[1].split(",")
    
    location = clean_location(location)
    country = location[-1] if location[-1] != 'n/a' else None 
    province = ''
    if len(location) > 1:
        province = location[-2] if location[-2] != 'n/a' else None

    # To avoid storing "western/australia"
    if country != None and '/' in country:
        country = country.split('/')[1]
    
    
    if province != None and '/' in province:
        province = province.split('/')[1]
    
    if not with_user_id: 
        return [country, province] 
    else:
        user_id = row[0]
        age = row[2]
        return [user_id, country, province, age]

def create_location_file(input_filename, output_filename):
    path = 'cleaned_dataset'
    
    if not os.path.exists(path):
        os.makedirs(path)
    output_path = os.path.join(path,output_filename)

    
    with open(input_filename, 'r', encoding='utf-8') as input_file:
        reader = csv.reader(input_file)
        
        # move to the next line to skip the first one
        next(reader)

        with open(output_path, 'w', encoding='utf-8', newline='') as output_file:
            writer = csv.writer(output_file)
            
            writer.writerow(fields)
            seen = list() # avoid duplicate insertion
            for row in reader:
                location_row = get_location(row)
                if location_row not in seen:
                    writer.writerow(location_row)
                    seen.append(location_row)
            
    if os.path.exists(input_filename):
        os.remove(input_filename)

