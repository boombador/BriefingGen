
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
        self.entries = []
        self.articles = []
        if not cc: 
            self.maxCharacters = int(cfg.get('static', 'maxCharacters'))
        else :
            self.maxCharacters = cc

        contentType = cfg.get("static", "contentType")
        if contentType == 'local':
            contentSource = cfg.get("static", "contentSource")
            print 'Info: looking for content in ' + contentSource
            self.readContentFile(contentSource, cfg)
        else:
            print 'Info: using rss source: ' + url
            url = cfg.get("static", "briefingUrl")
            briefConn = urlopen(url)
            briefing = briefConn.read()
            soup = BeautifulSoup(briefing)
            for item in  soup.findAll('item', limit=5) :
                newArticle = Article.from_item(item)
                newArticle.clamp(self.maxCharacters)
                self.articles.append(newArticle)

        entryFileName = cfg.get("static", "entriesFile")
        try:
            with open(entryFileName):
                entryList = CustomEntry(entryFileName)
                todaysEntry = entryList.loadEntry()
                self.entries.append(todaysEntry)
        except IOError:
            print 'Warning: Problem reading ' + entryFileName +', moving on...'

        # sort articles by prominence
        self.articles.sort(key=attrgetter('prominence'), reverse=True)

        # debug print statement
        # for item in self.articles:
            # print item

    def readContentFile(self, fileName, cfg) :
        with open(fileName, 'r') as f :
            curArticle = None
            for line in f :
                line = line.strip()
                if line == '---' :
                    if curArticle :
                        curArticle.clamp(self.maxCharacters)
                        self.articles.append(curArticle)
                    if len(self.articles) >= 5 :
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

    def printBriefingHTML(self) :
        articles = self.articles
        cfg = self.cfg
        style = self.cssText()
        params = {
            'dateString': datetime.now().strftime('%B %d, %Y'),
            'CVerb': cfg.get("static", "CVerb"),
            'compiler': cfg.get("static", "Compiler") 
        }
        headerHTML = loadPartial('layout', 'header', params)

        html = """
        <table border="0" style="background-color:#FFFFFF; max-width: 960px; font-family: Calibri;" cellpadding="0" cellspacing="0">
            <tr>
                <td>
                    """+headerHTML+"""
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">"""

        if len(self.entries) > 0 :
            row = self.entries[0]
            html += """
                <tr><!-- begin dp section -->
                    <td width="100%">
                        """ + row.getHTML(cfg) + """
                    </td>
                </tr>"""

        for article in articles :
            html += article.toHTML(cfg, 'rowWrapper')

        footer = loadPartial('layout', 'footer')
        html += """
                    </table>
                    """ + footer + """
                </td>
            </tr>
        </table>"""
        return style + html

