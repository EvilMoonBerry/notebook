import xmlrpc.client
import sys
# server proxy
s = xmlrpc.client.ServerProxy('http://localhost:9000/')

# function to add a topic to an xml file


def add_topic():
    topic = input("\nGive topic: ")
    note = input("Give note: ")
    text = input("Give text: ")
    print("")
    # call the server and pass the topic note and text as a parameter and print what the server returns
    try:
        print(s.add_topic(topic, note, text))
    except ConnectionRefusedError:
        print("Could not connect to server")
    except xmlrpc.client.Fault as err:
        print("A fault occurred")
        print("Fault code: %d" % err.faultCode)
        print("Fault string: %s" % err.faultString)


def notes():
    topic = input("\nGive topic: ")
    print("")
    # saving the data found from xml file to list
    try:
        list = s.notes(topic)

        # if the list is empty then there was no topic with a given name
        if len(list) > 0:
            print(topic)
            for i in list:
                print(i)
        else:  # giving the user the possibility to add a new topic with note and text
            choise = input(
                "Topic was not found. Would you like to add a topic?\nyes/no?\n")

            if choise == "yes":
                add_topic()
            elif choise == "no":
                main()
            else:
                print("Not a valid argument\n")  # check for invalid inputs
        print("")
    except ConnectionRefusedError:  # Error check
        print("Could not connect to the server")
    except xmlrpc.client.Fault as err:
        print("A fault occurred")
        print("Fault code: %d" % err.faultCode)
        print("Fault string: %s" % err.faultString)


# main function for asking for user input
def main():
    i = 9
    while i != 0:
        print("1. Add topic: ")
        print("2. Get notes on topic: ")
        print("0. end program: ")
        i = int(input("Option: "))
        if i == 0:
            break
        elif i == 1:
            add_topic()
        elif i == 2:
            notes()
        else:
            print("Unvalid argument\n")  # check for invalid inputs


try:
    if __name__ == "__main__":
        main()
except KeyboardInterrupt:
    print("\nKeyboard interrupt received, exiting.")
    sys.exit(0)
