#!/usr/bin/env python
# encoding: utf-8
from iOSReader import reader

r = reader()

# Constants:
prefix = "Sechler"
numlines = 10

# Initialize the reader.
r.addAddressBook("People/" + prefix + "/AddressBook/AddressBook.sqlitedb")
r.addSMSDatabase("People/" + prefix + "/SMS/sms.db")
# Get a list of the top numbers sorted by message count.
numberlist = sorted(r.getListOfNumbers(), key=lambda item: r.countFromNumber(item), reverse=True)[:numlines]
num = 0
for i in numberlist:
    messages = r.messagesFromNumber(i)
    numsent = 0
    for message in messages:
        if message.sent:
            numsent += 1
    print("{:0>2d}: {: >19s}: {: >6,d} messages {: >7,d} words {: >2,d} words/message {:0>2,.0%} sent".format(
        num+1, r.getNameFromNumber(i), r.countFromNumber(i), r.wordsFromNumber(i), r.wordsFromNumber(i)//r.countFromNumber(i), r.sentFromNumber(i)/r.countFromNumber(i)))
    num += 1
