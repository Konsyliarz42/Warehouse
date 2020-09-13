import logging
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
    if 'in' in command or 'from' in command:
        status_file = command[command.rfind(' '):].strip()
        status_file = status_file.strip()

        if '.' not in status_file:
            status_file += '.CSV'

        logging.debug(f"operation has argument: {status_file}")

    else:
        status_file = "status file.CSV"

    return status_file

#----------------------------------------------------------------
