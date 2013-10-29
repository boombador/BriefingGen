
# needed?
from datetime import datetime, timedelta
from csv import *
import re
from cgi import escape
import pprint
import sys
import os

# yes
from CustomEntry import *
from Section import *
from bs4 import BeautifulSoup
from urllib import urlopen
from operator import attrgetter

def loadPartial(partialType, partial, params=None) :
    name = partialType+'/'+partial+'.'+partialType
    with open(name, 'r') as f :
        layout = f.read()
        if params :
            for key in params :
                needle = '{{{ '+key+' }}}'
                replace = params[key]
                layout = layout.replace(needle, replace)
        return layout

def detexify(str) :
    simpleEscaped = re.compile(r'\\([#$%&~_^{}|])')
    mathEscaped = re.compile(r'\$([<>])\$')
    str = mathEscaped.sub(r'\1', str)
    str = simpleEscaped.sub(r'\1', str)
    str = str.replace('\\textbacklash', '\\')
    return str
    
def hexColor(str) :
    return "#%02X%02X%02X" % tuple([int(num) for num in str.split()])


class Briefing :
    def __init__(self, cfg, cc=0) : 
        self.cfg = cfg

        self.date = datetime.now().strftime('%Y%m%d')
        self.sections = []
        self.maxCharacters = cc

    def readTheme(self) :
        cfg = self.cfg
        archive = cfg.get("toplevel", "archiveDir")
        theme   = cfg.get("toplevel", "theme")

        themeDir = '/themes/'+theme+'/'
        root = os.getcwd()
        self.themeDir = root + themeDir
        self.archiveDir = root + '/' +archive+'/'

        self.root = root

    def parseTheme(self) :
        os.chdir(self.themeDir)
        cfg = self.cfg

        cfg.read("static.conf")
        cfg.read("categories.conf")
        self.maxCharacters = int(cfg.get('static', 'maxCharacters'))

        style = ''
        with open(self.themeDir+'css/screen.css', 'r') as f :
            content = f.read()
            params = { 'media': 'print', 'content': content }
            style += loadPartial('layout', 'css', params)

        with open(self.themeDir+'css/print.css', 'r') as f :
            content = f.read()
            params = { 'media': 'print', 'content': content }
            style += loadPartial('layout', 'css', params)
        self.style = '<style>\n' + style + '\n</style>'

        os.chdir(self.root)

    def readContent(self) :
        # read special entries, originally the Daily Practices
        cfg = self.cfg
        entryFileName = cfg.get("static", "entriesFile")
        print os.getcwd()
        if entryFileName != 'none' :
            try:
                with open(entryFileName) as f :
                    entryList = CustomEntry(entryFileName)
                    todaysEntry = entryList.loadEntry()
                    if todaysEntry :
                        self.sections.append(todaysEntry)
                        self.foundSpecialEntry = 1
            except IOError:
                print 'Warning: Problem reading ' + entryFileName +', moving on...'
                self.foundSpecialEntry = 0
                try:
                    self.readContentFile('entries.txt', cfg, 1)
                    self.foundSpecialEntry = 1
                except:
                    self.foundSpecialEntry = 0

        contentType = cfg.get("static", "contentType")
        if contentType == 'local':
            contentSource = cfg.get("static", "contentSource")
            self.readContentFile(contentSource, cfg, 5)
        else:
            url = cfg.get("static", "briefingUrl")
            briefConn = urlopen(url)
            briefing = briefConn.read()
            soup = BeautifulSoup(briefing)
            for item in  soup.findAll('item', limit=5) :
                newSection = Section.from_item(item)
                newSection.clamp(self.maxCharacters)
                self.sections.append(newSection)

        # sort sections by prominence
        self.sections.sort(key=attrgetter('prominence'), reverse=True)

    def readContentFile(self, fileName, cfg, limit=5) :
        with open(fileName, 'r') as f :
            curSection = None
            numSections = 0
            for line in f :
                line = line.strip()
                if line == '---' :
                    if curSection :
                        curSection.clamp(self.maxCharacters)
                        self.sections.append(curSection)
                        numSections += 1
                    if numSections >= limit :
                        return
                    curSection = Section()
                else :
                    index = line.find(':')
                    key = line[0:index]
                    val = line[index+2:]
                    curSection.setField(key, val)
                    if key == 'category' :
                        hasProm = cfg.has_option(val, 'prominence')
                        if hasProm :
                            prom = cfg.get(val, 'prominence')
                        else :
                            prom = cfg.get('Default', 'prominence')
                        curSection.prominence = prom

    def getFileName(self, withDate=False, type="Email") :
        name = "Briefing"+type
        if withDate :
            name += self.date
        name += ".html"
        return name

    def headerHTML(self) :
        cfg = self.cfg
        os.chdir(self.themeDir)
        params = {
            'dateString': datetime.now().strftime('%B %d, %Y'),
            'CVerb': cfg.get("static", "CVerb"),
            'compiler': cfg.get("static", "Compiler") 
        }
        html = loadPartial('layout', 'header', params)
        os.chdir(self.root)
        return html

    def printBriefingHTML(self) :
        if hasattr(self, 'style') :
            style = self.style
        headerHTML = self.headerHTML()
        sections = self.sections
        os.chdir(self.themeDir)
        footerName = self.cfg.get('static', 'footerfile');
        footerHTML = loadPartial('layout', footerName)
        os.chdir(self.root)

        articleHTML = ''
        for section in sections :
            articleHTML += section.toHTML(self.cfg, 'rowWrapper', self.themeDir)

        os.chdir(self.themeDir)
        params = {
            'style': style,
            'header': headerHTML,
            'sections': articleHTML,
            'footer': footerHTML,
        }
        html = loadPartial('layout', 'standard', params)
        print html
        os.chdir(self.root)
        return html

