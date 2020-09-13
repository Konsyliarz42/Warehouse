import logging, os
import new_functions as func

#----------------------------------------------------------------
def show_info(author, version):
    logging.debug("show information about program\n")
    print('Author:', author, '\nVersion', version)

#----------------------------------------------------------------
def show_status(items_list):
    logging.debug("show information about items in warehouse\n")
    print('name'.center(16,' '), 'quantity'.center(6,' '), 'unit'.center(4,' '), 'price'.center(8,' '), sep=' | ')
    print('—'*(16 + 8*2 + 4 + 3*3))

    for item in items_list:
        print(f"{item['name']:<16} | {item['quantity']:>8} | {item['unit']:<4} | {item['unit_price']:>5} €")

#----------------------------------------------------------------
def show_item(command, items_list):
    name = command[command.find('item') + 4:].strip()
    item = func.is_in_list(name, items_list)
    logging.debug(f"show information about item: '{name}'\n")

    if item != False:
        for it in items_list[item]:
            print(f"{it:>12} : {items_list[item][it]}")

#----------------------------------------------------------------
def show_revenue(date, path, items_list):
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

#----------------------------------------------------------------
def status_file_name(command):
    if 'in' in command or 'from' in command or 'remove' in command:
        if 'save' in command:
            pos = command.index('in') + 2
        elif 'from' in command:
            pos = command.index('from') + 4
        else:
            pos = command.index('remove') + 6
        
        status_file = command[pos:].strip()
        status_file = status_file.strip()

        if len(status_file) == 0:
            status_file = "status file.CSV"
        elif '.' not in status_file:
            status_file += '.CSV'

        logging.debug(f"operation has argument: {status_file}")

    else:
        status_file = "status file.CSV"

    return status_file

#----------------------------------------------------------------
def get_pos_and_dict(items_list, command='nothing'):
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
                
                elif 'Quantity' in string or 'Price' in string:
                    if func.is_number(x) == False:
                        print(f"Value is not a number!")
                        x = False

        dictionary_list.append(x)
        if x == None:
            break

    position = func.is_in_list(dictionary_list[0], items_list)
    return position, dictionary_list

#----------------------------------------------------------------
def sell_item(revenue_list, items_list, today_date, path):
    logging.debug("start selling procedure")
    change  = False
    date    = today_date.strftime('%d-%b-%Y')
    position, dictionary_list = get_pos_and_dict(items_list, 'sell_item')

    if position == False:
        logging.debug("item is not found in warehouse\n")
        print(f"'{dictionary_list[0]}' is not found in warehouse!")

    else:
        if None not in dictionary_list:
            dictionary = {  'date'          : today_date.strftime("%x"),
                            'time'          : today_date.strftime("%X"),
                            'name'          : dictionary_list[0],
                            'quantity'      : dictionary_list[1],
                            'unit'          : dictionary_list[2],
                            'unit_price'    : float(dictionary_list[3]) }

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

    return change, revenue_list, items_list

#----------------------------------------------------------------
def add_item(items_list):
    logging.debug("start adding procedure")
    change  = False
    position, dictionary_list = get_pos_and_dict(items_list)

    if position != False:
        dictionary_list[1] = int(items_list[position]['quantity']) + int(dictionary_list[1])

    else:
        if None not in dictionary_list:
            dictionary = {  'name'          : dictionary_list[0],
                            'quantity'      : dictionary_list[1],
                            'unit'          : dictionary_list[2],
                            'unit_price'    : float(dictionary_list[3]) }

            if func.confirm_choice() == True:
                logging.debug("accepting of adding")
                print("Start adding...", end=' ')
                items_list.append(dictionary)
                change = True
                print('complete', ' ')
                
        else:
            logging.debug("procedure is abort")
            print("Procedure is abort")
    
    return change, items_list

#----------------------------------------------------------------
def update_item(items_list):
    logging.debug("start updating procedure")
    change  = False
    position, dictionary_list = get_pos_and_dict(items_list)

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

    return change, items_list

#----------------------------------------------------------------
def load(change, status_file):
    logging.debug("start 'load' operation")

    while os.path.isfile(status_file) == False:
        status_file = input("File not found! Write again >: ")

        if status_file == '':
            status_file = None
            break

    if status_file != None:
        if change == True:
            print("Status of warehouse in this session was changed and you not saved this!")

        if func.confirm_choice() == True:
            print("Loading...", end=' ')
            items_list = func.load_file(status_file)
            change = False
            print("complete", ' ')

        return change, items_list

    else:
        logging.debug("procedure is abort")
        print("Procedure is abort")
        return None, None

#----------------------------------------------------------------
def save(status_file, items_list):
    logging.debug("start 'save' operation")

    if func.confirm_choice() == True:
        print("Saving...", end=' ')
        func.save_file(status_file, items_list)
        change = False
        print("complete", ' ')
    
    return change

#----------------------------------------------------------------
def remove(status_file):
    logging.debug("start 'remove' operation")

    while os.path.isfile(status_file) == False:
        status_file = input("File not found! Write again >: ")

        if status_file == '':
            status_file = None
            break

    if status_file != None and status_file != "status file.CSV":

        if func.confirm_choice() == True:
            print("Removing...", end=' ')
            os.remove(status_file)
            print("complete", ' ')

    elif status_file != "status file.CSV":
        logging.debug("procedure is abort")
        print("You can't remove default file")

    else:
        logging.debug("procedure is abort")
        print("Procedure is abort")