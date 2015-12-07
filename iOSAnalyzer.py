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
numdays = 365*2//1
pollingnum = 14

# Initialize the reader.
r.addAddressBook("People/" + prefix + "/AddressBook/AddressBook.sqlitedb")
r.addSMSDatabase("People/" + prefix + "/SMS/sms.db")
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
# With a progress bar library
with progress.Bar(expected_size=numdays*numlines+(numdays*numlines)//pollingnum) as bar:

    # PRIMARY GRAPH

    # Keep count of library function calls for the progress bar.
    count = 0
    # Create the progress bar.
    bar.show(count)
    # Create a line on the graph for each
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
            count += 1
            # Update the progress bar.
            bar.show(count)
        # Plot the line on the final graph
        plt.plot(xlist, ylist, linewidth=2.0, label=r.getNameFromNumber(number))
    # Add a y axis label
    plt.ylabel('Number of Messages')
    # Create a legend
    plt.legend([r.getNameFromNumber(number) for number in numberlist], loc=2)
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
    fig.set_size_inches(18.5, 10.5)
    # Export the graph to file
    fig.savefig("People/" + prefix + 'png.png', dpi=100, bbox_inches = 'tight')
    # Reset the graph
    plt.clf()

    # SLOPE GRAPHS

    # For each of the top numbers
    for number in numberlist:
        # Create the lists of x and y values
        xlist = []
        ylist = []
        # Calculate the beginning and end date of the polling interval
        startdate = lastday - datetime.timedelta(days=numdays)
        enddate = startdate + datetime.timedelta(days=pollingnum)
        # For each date range before the final message
        for i in range(numdays//pollingnum, -1, -1):
            # Find the total number of messages on both dates
            endtotal = r.totalOnDate(enddate, number)
            begtotal = r.totalOnDate(startdate, number)
            # Subtract the two
            difference = endtotal - begtotal
            # Add the x value and the messages per day to the lists
            xlist.append(numdays//pollingnum - i)
            ylist.append(difference // pollingnum)
            # Move the date range forward
            startdate += datetime.timedelta(days=pollingnum)
            enddate += datetime.timedelta(days=pollingnum)
            count += 1
            # Update the progress bar
            bar.show(count)
        # Plot the graphs of the slopes
        plt.plot(xlist, ylist, linewidth=2.0, label=r.getNameFromNumber(number))
    # Add a y axis label
    plt.ylabel('Number of Messages per day, {} day polling'.format(pollingnum))
    # Add a legend of names
    plt.legend([r.getNameFromNumber(number) for number in numberlist], loc=2)
    # Create a new list of x values to label the months.
    smonthx = [x//pollingnum for x in monthx]
    # Create dotted lines on the months.
    for line in monthlinenums:
        plt.axvline(x=line[0]/pollingnum, ls='--')
    # Prevent as much extra white space on the right.
    plt.autoscale(enable=True, axis='x', tight=True)
    # Add the month tick labels
    plt.xticks(smonthx, monthnames)
    # Create a figure, initialize it, and export it.
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    fig.savefig("People/" + prefix + 'slopes.png', dpi=100, bbox_inches = 'tight')
