
from bs4 import BeautifulSoup, NavigableString
from ununicode import toascii
from HTMLParser import HTMLParser
import re

MINLENGTH = 800

def strip_tags(html):
    soup = BeautifulSoup(html)

    for tag in soup.findAll(True):
        s = ""

        for c in tag.contents:
            if not isinstance(c, NavigableString):
                c = strip_tags(unicode(c))
            s += unicode(c)

        tag.replaceWith(s)

    return soup

def texify(str) :
    simpleEscape = re.compile(r'([#$%&~_^{}|])')
    mathEscape = re.compile(r'([<>])')
    str = str.replace('\\', '\\textbacklash')
    str = simpleEscape.sub(r'\\\1', str)
    str = mathEscape.sub(r'$\1$', str)
    return str

class Article :
    def __init__(self, item) :
        global MINLENGTH
        self.title = toascii(unicode(item.title.string))
        self.contributor = toascii(unicode(item.find('dc:creator').string))
        self.href = toascii(unicode(item.link.string))
        self.category = toascii(unicode(item.category.string))
        self.content = ''
        paragraphs = item.find('content:encoded')
        paragraphs = BeautifulSoup(unicode(paragraphs.string)).findAll('p')
        i = 0
        h = HTMLParser()
        while len(self.content)<MINLENGTH and i<len(paragraphs) :
            toAdd = h.unescape(toascii(unicode(strip_tags(unicode(paragraphs[i])))).strip()) 
                #Gotta Unescape yer HTMLEntities before you can Escape them!
            if len(toAdd) > 0 :
                self.content = self.content + ' ' + toAdd
            i+=1
        #self.content = self.content.replace('\n', ' ')
        self.content = re.compile(r'\r?\n').sub(' ', self.content)
        #print i, len(self.content), len(paragraphs)


        self.xml = item

    def __str__(self) :
        return self.href + ": (" \
            +  self.category + ") " \
            +  self.contributor + " posted \"" \
            +  self.title + "\"\n\n" \
            + self.content 
    def csv(self) :
        return texify(self.href) + "|" \
            + texify(self.title) + "|" \
            + texify(self.category) + "|" \
            + texify(self.contributor) + "|" \
            + texify(self.content)

