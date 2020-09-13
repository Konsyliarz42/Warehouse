import os, logging, datetime
import new_functions as func

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
help            - Show list of comends
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

    comend  = input(string_input)
    comend  = comend.lower()
    comend  = comend.strip()

    string_input    = "What will we do? >: "
    logging.debug(f"user wrote: '{comend}'")

    #--------------------------------
    if comend == 'exit':
        if change == True:
            print("Status of warehouse in this session was changed and you not saved this!")

        if func.confirm_choice() == True:
            logging.debug("program will be ended")
            print('Goodbye')
            break
    
    #--------------------------------
    elif comend == 'clear':
        logging.debug("clear console\n")
        os.system('cls')
        print('='*64 + f"\n{title}\n" + '='*64)

    #--------------------------------
    elif comend == 'help':
        logging.debug("print help list\n")
        print(help_list)

    #--------------------------------
    if comend == 'sell item' or comend == 'add item' or comend == 'update item':
        string_input_list   = ["Item name  : ", "Quantity   : ", "Unit       : ", "Price      : "]
        dictionary_list     = list()

        logging.debug("waiting on get input list...")
        for string in string_input_list:
            if comend == 'sell item' and 'Unit' in string:
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
        if comend == 'sell item':
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
        elif comend == 'add item':
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
    elif 'load' in comend or 'save' in comend or 'remove' in comend:
        logging.debug("detect operation on files...")
        if 'in' in comend or 'from' in comend:
            status_file = comend[comend.rfind(' '):].strip()
            status_file = status_file.strip()

            if '.' not in status_file:
                status_file += '.CSV'

            logging.debug(f"operation has argument: {status_file}")
        else:
            status_file = "status file.CSV"

        #Load option
        if 'load' in comend:
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
        elif 'save' in comend:
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
    elif 'show' in comend:
        if 'info' in comend:
            logging.debug("show information about program\n")
            print('Author:', author, '\nVersion', version)

        elif 'status' in comend:
            logging.debug("show information about items in warehouse\n")
            print('name'.center(16,' '), 'quantity'.center(6,' '), 'unit'.center(4,' '), 'price'.center(8,' '), sep=' | ')
            print('—'*(16 + 8*2 + 4 + 3*3))

            for item in items_list:
                print(f"{item['name']:<16} | {item['quantity']:>8} | {item['unit']:<4} | {item['unit_price']:>5} €")

        elif 'item' in comend:
            name = comend[comend.find('item') + 4:].strip()
            item = func.is_in_list(name, items_list)
            logging.debug(f"show information about item: '{name}'\n")

            if item != False:
                for it in items_list[item]:
                    print(f"{it:>12} : {items_list[item][it]}")

        elif 'revenue' in comend:
            logging.debug("show revenues\n")
            revenue_list    = func.load_revenue(date, path)
            items_value     = 0
            selling         = 0

            print(  'date'.center(8,' '),   'time'.center(8,' '), 
                    'name'.center(16,' '),  'quantity'.center(6,' '), 
                    'unit'.center(4,' '),   'price'.center(8,' '),      sep=' | ')
            print('—'*(16 + 8*4 + 4 + 3*5))

            for item in revenue_list:
                print(f"{item['date']:<8} | {item['time']:<8} | {item['name']:<16} | {item['quantity']:>8} | {item['unit']:<4} | {item['unit_price']:>5} €")
                selling += float(item['unit_price']) * int(item['quantity'])

            for item in items_list:
                items_value += float(item['unit_price']) * int(item['quantity'])

            print(  '\n' + '-'*32, 
                    '\nValue of warehouse   = ', round(items_value, 2),
                    '\nValue of selling     = ', round(selling, 2), 
                  '\n\nRevenue              = ', round(selling - items_value, 2)  )

        else:
            logging.debug("input is incorrect")
            string_input = "Can you write again? >: "

    #--------------------------------
    else:
        logging.debug("input is incorrect\n")
        string_input = "Can you write again? >: "

    print('')
logging.debug("-------- END --------")