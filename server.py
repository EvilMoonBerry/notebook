from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET
from datetime import datetime
import sys

# Sources:
# Writing to a xml file: https://stackabuse.com/reading-and-writing-xml-files-in-python/
# How to build xmlrp.server: https://docs.python.org/3/library/xmlrpc.server.html#module-xmlrpc.server
# How to use ElementTree: https://docs.python.org/3/library/xml.etree.elementtree.html

# Client calls this function to get information from xml file


def notes(topic):
    tree = ET.parse("/home/cardea/DisSys/notebook/db.xml")
    root = tree.getroot()
    list = []
    tName = topic
    print(tName)
    for topic in root.findall('topic'):  # iterating through all found topics
        # If a found topic is the same that the client wants and its not none iterate through it
        if topic is not None and topic.get('name') == tName:
            for note in topic:  # Get the found topics' content
                topics = topic.get('name')
                print(topics)
                note = topic.find('note').get('name')
                list.append(note)
                texty = topic.find('note').find('text').text
                list.append(texty)
                time = topic.find('note').find('timestamp').text
                list.append(time)
        else:
            print("No topic")  # if there was not a topic with the same name

    return list  # Return a list

# client calls this function to write new topic with note, text and timestamp to xml file


def add_topic(topic, note, text):

    tree = ET.parse("/home/cardea/DisSys/notebook/db.xml")
    root = tree.getroot()
    time = datetime.now()

    attrib = {'name': topic}
    # Makes a new element to the end of xml file
    element = root.makeelement('topic', attrib)
    root.append(element)

    # Sub element note for element topic
    subnote = ET.SubElement(element, 'note')
    # sub element text for element note
    subtext = ET.SubElement(subnote, 'text')
    # sub element timestamp for element note
    subtime = ET.SubElement(subnote, 'timestamp')

    subnote.set('name', note)  # set name for element note
    subtext.text = text  # Set text to element text
    # set time as text to element timestamp
    subtime.text = time.strftime('%d/%m/%Y - %H:%M:%S')

    tree.write('/home/cardea/DisSys/notebook/db.xml')  # write to xml file

    return "topic added"


# Making a server
# Bind  to localhost port 9000
with SimpleXMLRPCServer(("localhost", 9000)) as server:
    # Registering functions that the client can call
    server.register_introspection_functions()
    server.register_function(notes, "notes")
    server.register_function(add_topic, "add_topic")

    # note that the server has started
    print("Starting...")

    # Run the server's main loop
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)
