import os, logging, datetime
import new_functions as func, main_functions as mfunc

logging.basicConfig(    level = logging.DEBUG, 
                        format = '%(asctime)s %(message)s', 
                        handlers = [logging.FileHandler('logfile.log', 'w', 'utf-8')] )
path            = os.getcwd()
status_file     = "status file.CSV"
items_list      = list()
revenue_list    = list()

title   = "W A R E H O U S E  M E N A G E N T".center(64, ' ')
author  = "Tomasz Kordiak"
version = 2.0

change          = False
string_input    = "What will we do? >: "
help_list       = """add item        - Start adding procedure
sell item       - Start selling procedure
update item     - Start updating procedure

load            - Load status from default CSV file
load from ...   - Load status from other CSV file
save            - save status in default CSV file
save in ...     - save status in other CSV file
remove ...      - remove CSV file

show info       - Show information about program
show status     - Show array of all items in warehouse
show item ...   - Show information about item
show revenue    - Show list of month history revenues

clear           - Clear window
help            - Show list of commands
exit            - Quit program"""

#================================================================
logging.debug("-------- START --------")
print('='*64 + f"\n{title}\n" + '='*64)
today_date  = datetime.datetime.now()
date        = today_date.strftime('%d-%b-%Y')

#Create folder history
try:
    os.mkdir(path + '\\history')
except:
    pass

#Load last modified file
try:
    status_file = func.check_files(path)
    print("Loading status of warehouse...")
    open(status_file, 'r')

except:
    logging.debug(f"{status_file} not found")
    print(f"{status_file} not found!\n")

else:
    items_list = func.load_file(status_file)
    print(f"({status_file}) Loading complete\n")

#Start main program
while True:
    logging.debug("waiting on input...")

    command  = input(string_input)
    command  = command.lower()
    command  = command.strip()

    string_input    = "What will we do? >: "
    logging.debug(f"user wrote: '{command}'")

    #--------------------------------
    if command == 'exit':
        if change == True:
            print("Status of warehouse in this session was changed and you not saved this!")

        if func.confirm_choice() == True:
            logging.debug("program will be ended")
            print('Goodbye')
            break
    
    #--------------------------------
    elif command == 'clear':
        logging.debug("clear console\n")
        os.system('cls')
        print('='*64 + f"\n{title}\n" + '='*64)

    #--------------------------------
    elif command == 'help':
        logging.debug("print help list\n")
        print(help_list)

    #--------------------------------
    elif command == 'sell item' or command == 'add item' or command == 'update item':
        string_input_list   = ["Item name  : ", "Quantity   : ", "Unit       : ", "Price      : "]
        dictionary_list     = list()

        logging.debug("waiting on get input list...")
        for string in string_input_list:
            if command == 'sell item' and 'Unit' in string:
                x = 'psc'

            else:
                x = False

                while x == False:
                    x = input(string)

                    if x == '':
                        x = None
                        break

                    elif 'Quantity' in string or 'Price' in string:
                        if func.is_number(x) == False:
                            print(f"Value is not a number!")
                            x = False

            dictionary_list.append(x)

            if x == None:
                break

        position = func.is_in_list(dictionary_list[0], items_list)

        #Selling procedure
        if command == 'sell item':
            logging.debug("start selling procedure")

            if position == False:
                logging.debug("item is not found in warehouse\n")
                print(f"'{dictionary_list[0]}' is not found in warehouse!")

            else:
                if None not in dictionary_list:
                    dictionary = {  'date'      : today_date.strftime("%x"),
                                    'time'      : today_date.strftime("%X"),
                                    'name'      : dictionary_list[0],
                                    'quantity'  : dictionary_list[1],
                                    'unit'      : dictionary_list[2],
                                    'price'     : dictionary_list[3]    }

                    if func.confirm_choice() == True:
                        logging.debug("accepting of selling")
                        print("Start selling...", end=' ')
                        revenue_list.append(dictionary)
                        func.save_revenue(date, dictionary, path)
                        items_list[position]['quantity'] = int(items_list[position]['quantity']) - int(dictionary_list[1])
                        change = True
                        print('complete', ' ')

                else:
                    logging.debug("procedure is abort")
                    print("Procedure is abort")

        #Adding procedure
        elif command == 'add item':
            logging.debug("start adding procedure")

            if position != False:
                dictionary_list[1] = int(items_list[position]['quantity']) + int(dictionary_list[1])

            else:
                if None not in dictionary_list:
                    dictionary = {  'name'          : dictionary_list[0],
                                    'quantity'      : dictionary_list[1],
                                    'unit'          : dictionary_list[2],
                                    'unit_price'    : dictionary_list[3]    }

                    if func.confirm_choice() == True:
                        logging.debug("accepting of adding")
                        print("Start adding...", end=' ')
                        items_list.append(dictionary)
                        change = True
                        print('complete', ' ')
                
                else:
                    logging.debug("procedure is abort")
                    print("Procedure is abort")

        #Updating procedure
        else:
            logging.debug("start updating procedure")

            if position == False:
                logging.debug("item is not found in warehouse\n")
                print(f"'{dictionary_list[0]}' is not found in warehouse!")
            
            else:
                if None not in dictionary_list:
                    dictionary = {  'name'          : dictionary_list[0],
                                    'quantity'      : dictionary_list[1],
                                    'unit'          : dictionary_list[2],
                                    'unit_price'    : float(dictionary_list[3]) }

                    if func.confirm_choice() == True:
                        logging.debug("accepting of updating")
                        print("Start updating...", end=' ')
                        items_list[position] = dictionary
                        change = True
                        print('complete', ' ')
                
                else:
                    logging.debug("procedure is abort")
                    print("Procedure is abort")

    #--------------------------------
    elif 'load' in command or 'save' in command or 'remove' in command:
        logging.debug("detect operation on files...")
        status_file = mfunc.status_file_name(command)

        #Load option
        if 'load' in command:
            logging.debug("start 'load' operation")
            while os.path.isfile(status_file) == False:
                status_file = input("File not found! Write again >: ")

            if change == True:
                print("Status of warehouse in this session was changed and you not saved this!")

            if func.confirm_choice() == True:
                print("Loading...", end=' ')
                items_list = func.load_file(status_file)
                change = False
                print("complete", ' ')

        #Save option
        elif 'save' in command:
            logging.debug("start 'save' operation")
            if func.confirm_choice() == True:
                print("Saving...", end=' ')
                func.save_file(status_file, items_list)
                change = False
                print("complete", ' ')

        #Remove option
        else:
            logging.debug("start 'remove' operation")
            while os.path.isfile(status_file) == False:
                status_file = input("File not found! Write again >: ")

            if func.confirm_choice() == True:
                print("Removing...", end=' ')
                os.remove(status_file)
                print("complete", ' ')
    
    #--------------------------------
    elif 'show' in command:
        if 'info' in command:
            mfunc.show_info(author, version)

        elif 'status' in command:
            mfunc.show_status(items_list)

        elif 'item' in command:
            mfunc.show_item(command, items_list)

        elif 'revenue' in command:
            mfunc.show_revenue(date, path, items_list)

        else:
            logging.debug("input is incorrect")
            string_input = "Can you write again? >: "

    #--------------------------------
    else:
        logging.debug("input is incorrect\n")
        string_input = "Can you write again? >: "

    print('')
logging.debug("-------- END --------")