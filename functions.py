import csv, logging, os

#--------------------------------
def try_open(file_name):
    try:
        open(file_name, 'r')
    except:
        return False
    else:
        return True
        
#--------------------------------
def confirm_choice():
    while True:
        x = input("Are you sure? >: ")
        x = x.lower()
        x = x.strip()

        if x == 'y' or x == 'yes':
            return True

        elif x == 'n' or x == 'no':
            return False

#--------------------------------
def get_file(string):
    file_name = 'status file.CSV'

    if ' ' in string:
        file_name = string[string.rfind(' '):].strip()

        if '.' not in file_name:
            file_name += '.CSV'

    return file_name

#--------------------------------
def check_files(path_dir=os.getcwd()):
    """The function search .CSV files, check time last modifications and return file name"""

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

#--------------------------------
def load_status(file_name):
    """This function open file and creates dictionares in list."""

    logging.debug(f"load_status() is run with argument: '{file_name}'")
    items_list = list()

    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        logging.debug("- creates dictionares")

        for line in csv_reader:
            dictionary = {  'name': line[0],
                            'quantity': line[1],
                            'unit': line[2],
                            'unit_price': line[3]   }
            items_list.append(dictionary)

    items_list.remove(items_list[0])

    logging.debug("- returns list\n")
    return items_list

#--------------------------------
def save_status(items_list, file_name="status file.CSV"):
    """The funkcion save list in program to CSV file or other file."""

    logging.debug(f"save_status() is run")

    with open(file_name, 'w', newline='') as csv_file:
        logging.debug(f"- write '{file_name}'")
        keys = ['name','quantity','unit','unit_price']
        csv_writer = csv.DictWriter(csv_file, keys)
        csv_writer.writeheader()

        for dictionary in items_list:
            csv_writer.writerow(dictionary)
    
    logging.debug("- file is saved\n")

#--------------------------------
def add_item(name, quantity, unit, unit_price):
    dictionary = {  'name': name,
                    'quantity': quantity,
                    'unit': unit,
                    'unit_price': unit_price    } 

#================================================================
if __name__ == "__main__":
    pass