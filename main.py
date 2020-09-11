import os, logging
import functions

logging.basicConfig(    level = logging.DEBUG, 
                        format = '%(asctime)s %(message)s', 
                        handlers = [logging.FileHandler('logfile.log', 'w', 'utf-8')] )
path = os.getcwd()
status_file = "status file.CSV"
items = list()

title = "W A R E H O U S E  M E N A G E N T".center(64, ' ')
author = "Tomasz Kordiak"
version = 1.0
change = False

string_input = "What will we do?\n>: "
help_list = """add item        - start adding procedure
clear           - clearing window
exit            - quit program
help            - show list of all comends
info            - show information about program
load            - load status from 'status file.CSV'
load from ...   - load status from other file
remove          - remove 'status file.CSV'
remove file ... - remove file
save            - save status in 'status file.CSV'
save in ...     - save status in other file
sell item ...   - start selling procedure
show files      - show list of all founded CSV files
show revenue    - show revenue of warehouse
show item ...   - show information about item
show items      - show array of all items in warehouse
update item ... - update status of item in warehouse"""

#================================================================
logging.debug("-------- START --------")
print('='*64 + f"\n{title}\n" + '='*64)

try:
    status_file = functions.check_files(path)
    logging.debug(f"Try open {status_file}")
    print("Loading warehouse status...")
    open(status_file, 'r')
except:
    logging.debug("files not found")
    print("Files not found\n")
else:
    logging.debug(f"Loading data form {status_file}")
    items = functions.load_status(status_file)
    print(f"({status_file}) Loading complete...\n")

while True:
    logging.debug("waiting on input...")
    x = input(string_input)
    x = x.lower()
    x = x.strip()
    string_input = "What will we do?\n>: "
    logging.debug(f"user write: '{x}'")

    #----------------
    if x == 'add item':
        logging.debug("start adding procedure")
        print("To abort procedure confirm empty input")
        variables_name  = ['name', 'quantity', 'unit', 'price']
        variables = list()

        logging.debug("waiting on values of variables...")
        for var in variables_name:
            x = input('- ' + var + ' >: ')

            if x == '':
                break

            else:
                variables.append(x)

        if len(variables) < len(variables_name):
            logging.debug("procedure is aborted")
            print("Adding procedure is aborted")

        else:
            while functions.is_number(variables[1]) == False:
                print("Value of quantity is not a number!\nPleas fix it")
                variables[1] = input(">: ")
            
            while functions.is_number(variables[3]) == False:
                print("Value of price is not a number!\nPleas fix it")
                variables[3] = input(">: ")

            if functions.is_in_list(variables[0], items) == True:
                print("Item is already in warehouse!\nIf you want change item status use 'update item ...'")

            elif functions.confirm_choice() == True:
                logging.debug(f"adding {variables[0]}\n")
                x = functions.add_item(variables[0], variables[1], variables[2], variables[3])
                items.append(x)
                change = True
                print("Item is added to warehouse")

    #----------------
    elif 'update item' in x:
        item_name = x[x.rfind(' '):].strip()

        for item in items:
            if item_name == item['name']:
                print(item, '\n')
                x = input("What you want change? >: ")

                while x not in item.keys():
                    x = input("Can you write again? >: ")

                y = input("Write new value >: ")

                if x == 'quantity' or x == 'unit_price':
                    while functions.is_number(y) == False:
                        y = input("Value is not a number! >: ")

                logging.debug(f"item '{item_name}' is update")
                print("Item is updated")
                item[x] = y
                change = True
                break
        
    #----------------
    elif x == 'exit':
        if change == True:
            print("In this session status was changed and not will saved!")

        if functions.confirm_choice() == True:
            logging.debug("end program")
            print('Goodbye')
            break

    #----------------
    elif x == 'help':
        logging.debug("print 'help_list'\n")
        print(help_list)

    #----------------
    elif x == 'clear':
        logging.debug("refresh window\n")
        os.system('cls')
        print('='*64 + f"\n{title}\n" + '='*64)

    #----------------
    elif 'load' in x:
        if 'from' in x:
            status_file = functions.get_file(x)
        else:
            status_file = 'status file.CSV'

        if change == True:
            print("The function 'load' is block, because in this session status was changed!")

        else:
            if os.path.isfile(status_file) == True:
                if change == True:
                    print("Warehouse status is changed!")

                if functions.confirm_choice() == True:
                    logging.debug(f"loading data form {status_file}")
                    print(f"Loading {status_file}")
                    items = functions.load_status(status_file)
                    print("Loading complete...")
            else:
                print(f"{status_file} not found\nUse 'show files' to checks files")

    #----------------
    elif 'save' in x:
        if 'in' in x:
            status_file = functions.get_file(x)
        else:
            status_file = 'status file.CSV'

        if functions.confirm_choice() == True:
            logging.debug(f"saving in {status_file}")
            print(f"Saving in {status_file}")
            functions.save_status(items, status_file)
            change = False
            print("Saving complete...")

    #----------------
    elif x == 'show files':
        logging.debug("print all CSV files\n")
        files = [file_in_dir for file_in_dir in os.listdir(path) if file_in_dir.endswith('.CSV')]

        for i in files:
            print('- ' + i)

    #----------------
    elif 'remove' in x:
        status_file = functions.get_file(x)

        if os.path.isfile(status_file) == True:
            if functions.confirm_choice() == True:
                logging.debug(f"removing {status_file}\n")
                print(f"{status_file} is deleted")
                os.remove(status_file)
        
        else:
            print("File not found")

    #----------------
    elif x == 'info':
        logging.debug("print info about program\n")
        print("author:", author)
        print("version:", version)

    #----------------
    else:
        logging.debug("comend is incorrect\n")
        string_input = "Can you write again?\n>: "
    
    print('')

logging.debug("-------- END --------")