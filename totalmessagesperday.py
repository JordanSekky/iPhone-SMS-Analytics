#!/usr/bin/env python
# encoding: utf-8
from iOSReader import reader
import datetime


# Constants:
prefixes = ["King", "Sechler", "Field", "Remley", "Garisto"]

for i in prefixes:
    r = reader()
    r.addAddressBook("People/" + i + "/AddressBook/AddressBook.sqlitedb")
    r.addSMSDatabase("People/" + i + "/SMS/sms.db")

    numdays = (r.lastDate() - r.firstDate()).days
    print(i + ": " + str(r.totalMessages()//numdays))
