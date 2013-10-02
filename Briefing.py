
# needed?
from datetime import datetime, timedelta
from csv import *
import re
from cgi import escape
import pprint
import sys

# yes
from CustomEntry import *
from Article import *
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
        self.date = datetime.now().strftime('%Y%m%d')
        self.cfg = cfg
        self.articles = []
        if not cc: 
            self.maxCharacters = int(cfg.get('static', 'maxCharacters'))
        else :
            self.maxCharacters = cc

        # read special entries, originally the Daily Practices
        entryFileName = cfg.get("static", "entriesFile")
        try:
            with open(entryFileName) as f :
                entryList = CustomEntry(entryFileName)
                todaysEntry = entryList.loadEntry()
                if todaysEntry :
                    self.articles.append(todaysEntry)
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
                newArticle = Article.from_item(item)
                newArticle.clamp(self.maxCharacters)
                self.articles.append(newArticle)


        # sort articles by prominence
        self.articles.sort(key=attrgetter('prominence'), reverse=True)

    def readContentFile(self, fileName, cfg, limit=5) :
        with open(fileName, 'r') as f :
            curArticle = None
            numArticles = 0
            for line in f :
                line = line.strip()
                if line == '---' :
                    if curArticle :
                        curArticle.clamp(self.maxCharacters)
                        self.articles.append(curArticle)
                        numArticles += 1
                    if numArticles >= limit :
                        return
                    curArticle = Article()
                else :
                    index = line.find(':')
                    key = line[0:index]
                    val = line[index+2:]
                    curArticle.setField(key, val)
                    if key == 'category' :
                        hasProm = cfg.has_option(val, 'prominence')
                        if hasProm :
                            prom = cfg.get(val, 'prominence')
                        else :
                            prom = cfg.get('Default', 'prominence')
                        curArticle.prominence = prom

    def getFileName(self, withDate=False) :
        name = "BriefingEmail"
        if withDate :
            name += self.date
        name += ".html"
        return name

    def cssText(self) :
        style = ''
        with open('css/screen.css', 'r') as f :
            content = f.read()
            params = { 'media': 'print', 'content': content }
            style += loadPartial('layout', 'css', params)

        with open('css/print.css', 'r') as f :
            content = f.read()
            params = { 'media': 'print', 'content': content }
            style += loadPartial('layout', 'css', params)

        style = '<style>\n' + style + '\n</style>'
        return style

    def headerHTML(self) :
        cfg = self.cfg
        params = {
            'dateString': datetime.now().strftime('%B %d, %Y'),
            'CVerb': cfg.get("static", "CVerb"),
            'compiler': cfg.get("static", "Compiler") 
        }
        return loadPartial('layout', 'header', params)

    def printBriefingHTML(self) :
        style = self.cssText()
        headerHTML = self.headerHTML()
        articles = self.articles
        footerHTML = loadPartial('layout', 'footer_teamdb')

        articleHTML = ''
        for article in articles :
            articleHTML += article.toHTML(self.cfg, 'rowWrapper')

        params = {
            'style': style,
            'header': headerHTML,
            'articles': articleHTML,
            'footer': footerHTML,
        }
        return loadPartial('layout', 'standard', params)

