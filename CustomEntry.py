#!/usr/bin/python
from xlrd import *
from datetime import datetime
from ununicode import toascii
from sys import *
import re
from Article import *

def texify(str) :
    simpleEscape = re.compile(r'([#$%&~_^{}|])')
    mathEscape = re.compile(r'([<>])')
    str = str.replace('\\', '\\textbacklash')
    str = simpleEscape.sub(r'\\\1', str)
    str = mathEscape.sub(r'$\1$', str)
    return str

currdate = datetime.now().strftime('%m/%d/%Y')
XLS_FILE_NAME = 'Daily Practices - 2013.xlsx'


class CustomEntry :
    def __init__(self, entriesFile) :
        ceBook = open_workbook(entriesFile)
        ceSheet = ceBook.sheet_by_index(0)
        self.nameCol = 0
        self.quoteCol = 0
        self.pubCol = 0
        self.catCol = 0
        self.urlCol = 0

        i = 0
        while i < ceSheet.ncols :
            val = ceSheet.cell_value(0,i)
            if val == "Name" :
                self.nameCol = i
            elif val == "Practice" :
                self.quoteCol = i 
            elif val == "Published" :
                self.pubCol = i
            elif val == "Category" :
                self.catCol = i
            elif val == "Link_URL" :
                self.urlCol = i
            i+=1

        self.sheet = ceSheet

    def loadEntry(self) :
        row = 1
        displayRows = []
        backupRow = 0
        ceSheet = self.sheet
        # set datestr to practice that is in sheet's last row, or to today's practice
        while row < ceSheet.nrows :
            val = ceSheet.cell_value(row, self.pubCol)
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

        for row in displayRows :
            name =  texify(toascii(ceSheet.cell_value(row, self.nameCol)))
            practice =  texify(re.compile(r'\r?\n').sub(' ', toascii(ceSheet.cell_value(row, self.quoteCol))))
            category = texify(toascii(ceSheet.cell_value(row, self.catCol)))
            if not category :
                category = 'Next Jump Teachings'
            url = texify(toascii(ceSheet.cell_value(row, self.urlCol)))
        self.article = Article("", name, category, practice, url, None)

#
#if (nameCol + quoteCol) * (nameCol + pubCol) * (quoteCol + pubCol) == 0 :
 #   print >> stderr, "ERROR: Missing Column in %s, Looking for \"Name\", \"Practice\" and \"Published\"" % XLS_FILE_NAME
  #  exit(1)


