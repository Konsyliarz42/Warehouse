import logging, os, csv

#----------------------------------------------------------------
def check_files(path_dir):
    """The function find all CSV files, check time last modifications and return file name."""

    logging.debug(f"check_files() is run with argument: '{path_dir}'")
    file_name = None
    file_time = 0

    for file_in_dir in os.listdir(path_dir):
        if file_in_dir.endswith('.CSV'):
            logging.debug(f"- check {file_in_dir}")
            time = os.path.getmtime(file_in_dir)

            if time > file_time:
                file_name = file_in_dir
                file_time = time

    logging.debug(f"- returns {file_name}\n")
    return file_name

#----------------------------------------------------------------
def load_file(file_name):
    """This function open file and creates dictionares in list."""

    logging.debug(f"load_file() is run with argument: '{file_name}'")
    items_list = list()

    with open(file_name, newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        items_list.extend(csv_reader)

    logging.debug("- returns list\n")
    return items_list

#----------------------------------------------------------------
def save_file(file_name, items_list):
    """The funkcion save list in program to CSV file or other file."""

    logging.debug(f"save_file() is run")

    with open(file_name, 'w', newline='') as csv_file:
        logging.debug(f"- write '{file_name}'")
        keys = ['name','quantity','unit','unit_price']
        csv_writer = csv.DictWriter(csv_file, keys)
        csv_writer.writeheader()

        for dictionary in items_list:
            csv_writer.writerow(dictionary)
    
    logging.debug("- file is saved\n")

#----------------------------------------------------------------
def confirm_choice():
    """The function run in loop."""

    while True:
        x = input("Are you sure? >: ")
        x = x.lower()
        x = x.strip()

        if x == 'yes':
            return True

        elif x == 'no':
            return False

#----------------------------------------------------------------
def save_revenue(date, item_dict, path):
    logging.debug(f"save_revenue() is run")
    file_name = "history/" + date + '.CSV'
    file_name = os.path.realpath(file_name) 

    if os.path.isfile(file_name) == False:
        write_header = True

    else:
        write_header = False

    with open(file_name, 'a', newline='') as csv_file:
        logging.debug(f"- write '{file_name}'")
        keys = ['date','time','name','quantity','unit','unit_price']
        csv_writer = csv.DictWriter(csv_file, keys)

        if write_header == True:
            csv_writer.writeheader()
            
        csv_writer.writerow(item_dict)
    
    logging.debug("- file is saved\n")

#----------------------------------------------------------------
def load_revenue(date, path_dir):
    logging.debug(f"load_revenue() is run with arguments: '{date}', '{path_dir}'")
    items_list = list()
    path_dir += '\\history'
    files = date[date.find('-') + 1:] + '.CSV'

    for file_in_dir in os.listdir(path_dir):
        if file_in_dir.endswith(files):
            file_in_dir = os.path.join(path_dir, file_in_dir)
            
            with open(file_in_dir, newline='') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                print(file_in_dir)
                for reader in csv_reader:
                    items_list.append(reader)
                

    logging.debug("- returns list\n")
    return items_list

#----------------------------------------------------------------
def is_number(string):
    try:
        float(string)

    except:
        return False

    else:
        return True

#----------------------------------------------------------------
def is_in_list(element_name, elements_list):
    for element in elements_list:
        if element_name == element['name']:
            position = elements_list.index(element)
            return position
    
    return False