#!/usr/bin/env python3
# encoding: utf-8
# Import Statements:
from iOSReader import reader
import datetime
import matplotlib.pyplot as plt
from clint.textui import progress

r = reader()

# Constants:
prefix = "Sechler"
numlines = 10
word = "love"

# Initialize the reader.
r.addAddressBook("People/" + prefix + "/AddressBook/AddressBook.sqlitedb")
r.addSMSDatabase("People/" + prefix + "/SMS/sms.db")
numberlist = sorted(r.getListOfNumbers(), key=lambda item: r.countFromNumber(item), reverse=True)[:numlines]

for i in numberlist:
    print(r.getNameFromNumber(i) + ": " + str(r.instancesOf(word, i)))
    print(r.getNameFromNumber(i) + ": " + str(r.instancesOf(word, i)/r.countFromNumber(i)))
