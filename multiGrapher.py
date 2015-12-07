#!/usr/bin/env python3
# encoding: utf-8
# Import Statements:
from iOSReader import reader, datetime
import matplotlib.pyplot as plt
from clint.textui import progress

r = reader()

# Constants:
prefix = "Sechler"
numlines = 10
numdays = 365*2//1 
pollingnum = 10

# Initialize the reader.
r.addAddressBook("People/" + prefix + "/AddressBook/AddressBook.sqlitedb")
r.addSMSDatabase("People/" + prefix + "/sms/sms.db")
# Get a list of the top numbers sorted by message count.
numberlist = sorted(r.getListOfNumbers(), key=lambda item: r.countFromNumber(item), reverse=True)[:numlines]
# Find the date of the most recent message.
lastday = r.lastDate()
# Find the first day to iterate from.
firstday = lastday - datetime.timedelta(days=numdays)

monthlinenums = []
# Iterate through the months between the last day and the first day.
curMonth = datetime.date(lastday.year, lastday.month, 1)
monthdict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
             7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
while curMonth > firstday.date():
    # Make a list of tuples of the x values to place line at, and the integer
    # corresponding to the month is represents.
    monthlinenums.append(((curMonth - firstday.date()).days, curMonth))
    if curMonth.month == 1:
        curMonth = datetime.date(curMonth.year - 1, 12, 1)
    else:
        curMonth = datetime.date(curMonth.year, curMonth.month - 1, 1)
# Create a list of x values to place lines at.
monthx = [x[0] for x in monthlinenums]
# Create a list of labels.
monthnames = [monthdict[x[1].month] + "\n" + str(x[1].year) for x in monthlinenums]

# PRIMARY GRAPH

# Create a line on the graph for each
rank = 0
for number in numberlist:
    # Create the the lists to store coordinates in.
    xlist = []
    ylist = []
    # For each day since first day
    for i in range(numdays, -1, -1):
        date = lastday - datetime.timedelta(days=i)
        xlist.append(numdays-i)
        total = r.totalOnDate(date, number)
        # Append the total count
        ylist.append(total)
        # Update the progress bar.
    # Plot the line on the final graph
    plt.plot(xlist, ylist, linewidth=2.0, label=r.getNameFromNumber(number))
    # Add a y axis label
    plt.ylabel('Number of Messages')
    # Create a legend
    plt.legend([r.getNameFromNumber(number)], loc=2)
    # Plot the dotted lines
    for line in monthx:
        plt.axvline(x=line, ls='--')
    # Remove extra x values
    plt.autoscale(enable=True, axis='x', tight=True)
    # Add x axis labels
    plt.xticks(monthx, monthnames)
    # Create figure for export
    fig = plt.gcf()
    # Set an export size
    fig.set_size_inches(26.0, 10.5)
    # Export the graph to file
    print("Saving {}'s Graph".format(r.getNameFromNumber(number)))
    fig.savefig("Graphs/" + str(rank) + " " + r.getNameFromNumber(number) + '.png', dpi=100, bbox_inches = 'tight')
    rank += 1
    # Reset the graph
    plt.clf()


