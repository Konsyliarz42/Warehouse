import os, logging
import functions

logging.basicConfig(    level = logging.DEBUG, 
                        format = '%(asctime)s %(message)s', 
                        handlers = [logging.FileHandler('logfile.log', 'w', 'utf-8')] )
refresh = False
change = False
items = list()
status_file = "status file.CSV"
string_input = "What will we do?\n>: "
path = os.getcwd()

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

#================================================================
logging.debug("-------- START --------")
print('='*64 + "\n\tW A R E H O U S E  M E N A G E N T\n" + '='*64)

while True:
    if refresh == True:
        os.system("cls")
        print('='*64 + "\n\tW A R E H O U S E  M E N A G E N T\n" + '='*64)
        refresh = False

    if items == []:
        try:
            status_file = functions.check_files(path)
            logging.debug(f"Try open {status_file}")
            print("Loading warehouse status...")
            open(status_file, 'r')
        except:
            logging.debug("file not found")
            print(f"File {status_file} not found\n")
        else:
            logging.debug(f"Loading {status_file}")
            items = functions.load_status(status_file)
            print(f"({status_file}) Loading complete...\n")

    logging.debug("Waiting on input...")
    x = input(string_input)
    x = x.lower()
    list_input = list(x.split(' '))

    if list_input == []:
        logging.debug("Input is empty")
        list_input.append(None)

    logging.debug(f"User write: '{x}'")
    string_input = "What will we do?\n>: "
    
    #Quit program
    if list_input[0] == "exit" and confirm_choice() == True:
        logging.debug("Program is end")
        print("Goodbye")
        break

    #Clear window
    elif list_input[0] == 'clear':
        logging.debug("Clear window")
        refresh = True

    #Save status
    elif list_input[0] == 'save' and confirm_choice() == True:
        file_name = "status file.CSV"

        if 'in' in list_input and len(list_input) > 2:
            file_name = ' '.join(list_input[2:])

            if '.' not in file_name:
                file_name += '.CSV'

        logging.debug("Saving status...")
        print(f"Status is saving in '{file_name}'")
        functions.save_status(items, file_name)
        change = False

    #Load status
    elif list_input[0] == 'load' and len(list_input) > 1:
        x = ' '.join(list_input[1:])

        if os.path.isfile(x) == True:
            if confirm_choice() == True:
                print(f"({x}) Loading complete...")
                items = functions.load_status(x)
        
        else:
            print("File not found\nTo show list of CSV file write 'show csv'")

    #Show CSV list
    elif list_input[0] == 'show' and len(list_input) > 1:
        if list_input[1] == 'csv':
            print([file_in_dir for file_in_dir in os.listdir(path) if file_in_dir.endswith('.CSV')])

    #Remove file
    elif list_input[0] == 'remove' and len(list_input) > 1:
        x = ' '.join(list_input[1:])

        if os.path.isfile(x) == True:
            if confirm_choice() == True:
                print(f"{x} is deleted")
                os.remove(x)
        
        else:
            print("File not found")

    #Repeat input
    else:
        logging.debug("Incorrect input\n")
        string_input = "Can you write again?\n>: "

    #Loop
    print('')

logging.debug("-------- END --------")