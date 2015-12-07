#!/bin/bash
echo Please, enter your name
read NAME
echo What is the ip of the jailbroken phone?
read IP
mkdir -p People
cd People
mkdir -p $NAME
cd $NAME
mkdir -p SMS
mkdir -p AddressBook
cd SMS
sftp root@$IP:/var/mobile/Library/SMS/sms.db*
cd ../AddressBook
sftp root@$IP:/var/mobile/Library/AddressBook/AddressBook.sqlitedb*
