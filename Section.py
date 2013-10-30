from bs4 import BeautifulSoup, NavigableString
from ununicode import toascii
from HTMLParser import HTMLParser
import os
import re

def loadPartial(partialType, partial, params=None) :
    name = partialType+'/'+partial+'.'+partialType
    with open(name, 'r') as f :
        layout = f.read()
        if params :
            for key in params :
                replace = params[key]
                if replace :
                    needle = '{{{ '+key+' }}}'
                    layout = layout.replace(needle, replace)
        return layout


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

class Section :
    def __init__(self, title='', contributor='user', category='General', content='Empty post', href=None, xml=None, layout='article') :
        self.title = title
        self.contributor = contributor
        self.category = category
        self.content = content
        self.href = href
        self.prominence = 5
        self.layout = layout

    @classmethod
    def from_item(cls, item) :
        title = toascii(unicode(item.title.string))
        contributor = toascii(unicode(item.find('dc:creator').string))
        href = toascii(unicode(item.link.string))
        category = toascii(unicode(item.category.string))
        content = ''
        paragraphs = item.find('content:encoded')
        paragraphs = BeautifulSoup(unicode(paragraphs.string)).findAll('p')
        i = 0
        h = HTMLParser()
        while i<len(paragraphs) :
            toAdd = h.unescape(toascii(unicode(strip_tags(unicode(paragraphs[i])))).strip()) 
            if len(toAdd) > 0 :
                content = content + ' ' + toAdd
            i+=1
        content = re.compile(r'\r?\n').sub(' ', content)
        xml = item
        return cls(title, contributor, category, content, href, xml)

    # this is actually a pretty difficult function, ideally would cut off at the same length
    # more accurately to simplify the spacing requirements in the email layout
    def clamp(self, cc=0) :
        content = self.content
        if cc > 0 :
            newContent = ''
            for word in content.split() :
                newContent += ' ' + word
                if len(newContent) >= cc :
                    newContent = newContent.strip() + '...'
                    break
            self.content = newContent.strip()

    def setField(self, key, val) :
        if key == 'title' :
            self.title = val
        elif key == 'contributor' :
            self.contributor = val
        elif key == 'category' :
            self.category = val
        elif key == 'content' :
            self.content = val
        elif key == 'href' :
            self.href = val
        elif key == 'xml' :
            self.xml = val

    def __str__(self) :
        return str(self.prominence) + " " \
            +  self.href + ": (" \
            +  self.category + ") " \
            +  self.contributor + " posted \"" \
            +  self.title \
            + ' ['+self.layout+']\n' \
            + self.content + "\n"
    def csv(self) :
        return texify(self.href) + "|" \
            + texify(self.title) + "|" \
            + texify(self.category) + "|" \
            + texify(self.contributor) + "|" \
            + texify(self.content)

    def category(self) :
        return self.category
    def contributor(self) :
        return self.contributor
    def title(self) :
        return self.title
    def text(self) :
        return self.content
    def url(self) :
        return self.href

    def getDefault( self, cfg, option, optionalBackup=False ):
        if cfg.has_option( 'Default', option ):
            return cfg.get("Default", option )
        return optionalBackup

    def toHTML(self, cfg, containerApply=None, themeDir=None) :
        categoryName = self.category
        params = {
            'categoryName': categoryName.upper(),
            'submitterName': self.contributor,
            'articleTitle': self.title,
            'articleText': self.content,
            'linkUrl': self.href
        }
        params['barColor']        =  self.getDefault( cfg, 'barColor' )
        params['backgroundColor'] =  self.getDefault( cfg, 'backgroundColor' )
        params['imgBaseUrl']      =  self.getDefault( cfg, 'imgBaseUrl' )
        params['img']             =  self.getDefault( cfg, 'img' )
        params['nameIntro']       =  self.getDefault( cfg, 'nameIntro' )
        if cfg.has_section(categoryName):
            options = cfg.options(categoryName)
            for option in options :
                val = cfg.get(categoryName, option)
                params[option] = val
                #if option == "barcolor":
                    #barColor = val
                #elif option == "backgroundcolor":
                    #backgroundColor = val
                #elif option == "imgbaseurl":
                    #imgBaseUrl = val
                #elif option == "img":
                    #img = val
                #elif option == "agentintrophrase":
                    #nameIntro = val
        if cfg.has_option(categoryName, 'layout') :
            self.layout = cfg.get(categoryName, 'layout')
        else :
            self.layout = cfg.get("Default", 'layout')
        if params['imgBaseUrl'] and params['img'] :
            params['imgurl'] = params['imgBaseUrl'] + params['img']

        root = os.getcwd()
        if themeDir :
            os.chdir(themeDir)
        html = loadPartial('layout', self.layout, params)
        if containerApply :
            html = loadPartial('layout', containerApply, { 'content': html })
        os.chdir(root)
        return html

