#!/usr/bin/env python
# encoding: utf-8

from iOSReader import reader, datetime
from clint.textui import progress
from subprocess import call

r = reader()

prefix = "Sechler"
outfile = prefix + ".txt"

r.addAddressBook(prefix + "/AddressBook/AddressBook.sqlitedb")
r.addSMSDatabase(prefix + "/sms/sms.db")

numberlist = sorted(r.getListOfNumbers(), key=lambda item: r.countFromNumber(item), reverse=True)[:10]

call("mkdir -p SechlerTexts", shell=True)


for number in numberlist:
    out = open(prefix + "Texts/" + r.getNameFromNumber(number) + ".txt", 'w')
    for message in sorted(r.messagesFromNumber(number), key=lambda item: item.timestamp):
        if message.sent:
            out.write(str(message.timestamp) + " " + message.text + "\n")
        else:
            out.write(str(message.timestamp) + " " + message.text + "\n")
        


