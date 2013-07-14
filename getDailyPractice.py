#!/usr/bin/python
from xlrd import *
from datetime import datetime
from ununicode import toascii
from sys import *
import re

currdate = datetime.now().strftime('%m/%d/%Y')
XLS_FILE_NAME = 'Daily Practices - 2013.xlsx'

def texify(str) :
    simpleEscape = re.compile(r'([#$%&~_^{}|])')
    mathEscape = re.compile(r'([<>])')
    str = str.replace('\\', '\\textbacklash')
    str = simpleEscape.sub(r'\\\1', str)
    str = mathEscape.sub(r'$\1$', str)
    return str

dPs = open_workbook(XLS_FILE_NAME)

practiceSheet = dPs.sheet_by_index(0)


# parse the header row to determine column labels

nameCol = 0
quoteCol = 0
pubCol = 0
catCol = 0
urlCol = 0


i = 0
while i < practiceSheet.ncols :
    val = practiceSheet.cell_value(0,i)
    if val == "Name" :
        nameCol = i
    elif val == "Practice" :
        quoteCol = i 
    elif val == "Published" :
        pubCol = i
    elif val == "Category" :
        catCol = i
    elif val == "Link_URL" :
        urlCol = i
    i+=1
    
row = 1

#
#if (nameCol + quoteCol) * (nameCol + pubCol) * (quoteCol + pubCol) == 0 :
 #   print >> stderr, "ERROR: Missing Column in %s, Looking for \"Name\", \"Practice\" and \"Published\"" % XLS_FILE_NAME
  #  exit(1)

displayRows = []
backupRow = 0
# set datestr to practice that is in sheet's last row, or to today's practice
while row < practiceSheet.nrows :
    val = practiceSheet.cell_value(row,pubCol)
    if val:
        valDate = xldate_as_tuple(val, 0) #Magic number means Datemode since 1900 instead of 1904. Stupid proprietary Excel Dates.
        datestr = "%02d/%02d/%04d" % (valDate[1], valDate[2], valDate[0])
        backupRow = row
        if datestr == currdate:
            displayRows.append(row)
    row+=1

if not backupRow :
    print >> stderr, "WARNING: No practices found for any date"
    exit(0)

if not displayRows :
    print >> stderr, "WARNING: Today's Daily Practice not found - checked %d rows for \"%s\"" % (row, currdate)
    displayRows.append(backupRow)

print "Contributor|Practice|Category|Link_URL"
for row in displayRows :
    name =  texify(toascii(practiceSheet.cell_value(row, nameCol)))
    practice =  texify(re.compile(r'\r?\n').sub(' ', toascii(practiceSheet.cell_value(row, quoteCol))))
    category = texify(toascii(practiceSheet.cell_value(row, catCol)))
    if not category :
        category = 'Next Jump Teachings'
    url = texify(toascii(practiceSheet.cell_value(row, urlCol)))
    print name + "|" + practice + "|" + category + "|" + url

