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
        #Selling procedure
        if command == 'sell item':
            change, revenue_list, items_list = mfunc.sell_item(revenue_list, items_list, today_date, path)

        #Adding procedure
        elif command == 'add item':
            change, items_list = mfunc.add_item(items_list)

        #Updating procedure
        else:
            change, items_list = mfunc.update_item(items_list)

    #--------------------------------
    elif 'load' in command or 'save' in command or 'remove' in command:
        logging.debug("detect operation on files...")
        status_file = mfunc.status_file_name(command)

        #Load option
        if 'load' in command:
            x, y = mfunc.load(change, status_file)
            
            if x != None:
                change, items_list = x, y

        #Save option
        elif 'save' in command:
            change = mfunc.save(status_file, items_list)

        #Remove option
        else:
            mfunc.remove(status_file)
    
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