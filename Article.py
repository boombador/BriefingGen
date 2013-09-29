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
    def __init__(self, title='Title', contributor='user', category='General', content='Empty post', href=None, xml=None) :
        self.title = title
        self.contributor = contributor
        self.category = category
        self.content = content
        self.href = href
        self.prominence = 5

    @classmethod
    def from_item(cls, item) :
        global MINLENGTH
        title = toascii(unicode(item.title.string))
        contributor = toascii(unicode(item.find('dc:creator').string))
        href = toascii(unicode(item.link.string))
        category = toascii(unicode(item.category.string))
        content = ''
        paragraphs = item.find('content:encoded')
        paragraphs = BeautifulSoup(unicode(paragraphs.string)).findAll('p')
        i = 0
        h = HTMLParser()
        while len(content)<MINLENGTH and i<len(paragraphs) :
            toAdd = h.unescape(toascii(unicode(strip_tags(unicode(paragraphs[i])))).strip()) 
            if len(toAdd) > 0 :
                content = content + ' ' + toAdd
            i+=1
        content = re.compile(r'\r?\n').sub(' ', content)
        xml = item
        return cls(title, contributor, category, content, href, xml)

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
            +  self.title + "\"\n" \
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

    def getHTML(self, cfg) :
        categoryName = self.category
        submitterName = self.contributor
        articleText = self.content
        articleTitle = self.title
        linkUrl = self.href

        imgBaseUrl = 'https://imga.nxjimg.com/secured/image/briefing/'
        img = 'marketing.jpg'

        barColor = cfg.get("Default", "barColor")
        backgroundColor = cfg.get("Default", "backgroundColor")
        isDailyTeaching = cfg.get("Default", "isDailyTeaching")
        imgBaseUrl = cfg.get("Default", "imBaseUrl")
        img = cfg.get("Default", "img")
        nameIntro = cfg.get("Default", "agentIntroPhrase");

        if cfg.has_section(categoryName):
            options = cfg.options(categoryName)
            for option in options :
                val = cfg.get(categoryName, option)
                if option == "barcolor":
                    barColor = val
                elif option == "backgroundcolor":
                    backgroundColor = val
                elif option == "isdailyteaching":
                    isDailyTeaching = val
                elif option == "imgbaseurl":
                    imgBaseUrl = val
                elif option == "img":
                    img = val
                elif option == "agentintrophrase":
                    nameIntro = val

        imgurl = imgBaseUrl + img

        html = """
        <table border="0" cellpadding="0" cellspacing="0" width="100%">
            <tr height="30" bgcolor=\"""" + barColor + """" class="articleBar">
                <td width="36">
                    <img src=\"""" + imgurl + """" width="36" height="30">
                </td>
                <td width="100%" style="color: white; font-family: Calibri;" class="articleBarText">
                    <b>""" + categoryName.upper() + """</b>"""
        if isDailyTeaching == 'False':
            if submitterName :
                html += " - " + nameIntro + " " + submitterName
        html += """
                </td>
            </tr>
            <tr>
                <td colspan="2" bgcolor=\"""" + backgroundColor + """">
                    <div class="articleBoxWrapper">
                        <div class="articleBox">"""

        html += """
                            <table width="100%" border="0" cellpadding="0" cellspacing="0">
                                <tr height="10" class="articleBoxTopSpacer">
                                    <td colspan="3"></td>
                                </tr>"""
        if articleTitle :
            html += """
                                <tr><!-- Title row, not always needed -->
                                    <td width="15"></td>
                                    <td align="left" style="font-size: 18px; font-weight: 700;" class="articleTitle">""" + articleTitle + """</td>
                                    <td width="15"></td>
                                </tr>
                                <tr height="5">
                                </tr>"""
        html += """
                                <tr>
                                    <td width="15"></td>
                                    <td>""" + articleText + """</td>
                                    <td width="15"></td>
                                </tr>
                                <tr height="10" class="readMoreLink">
                                    <td colspan="3"></td>
                                </tr>
                                <tr"""
        if isDailyTeaching == 'False':
            html += """ class="readMoreLink\""""

        html += """>
                                    <td></td>
                                    <td align="left">"""
        if isDailyTeaching == 'True':
            if submitterName :
                html += submitterName
        else : 
            html += """<a href=\"""" + linkUrl + """">Read More</a>"""
        html += """
                                    </td>
                                    <td></td>
                                </tr>
                                <tr height="20" class="articleBoxBottomSpacer">
                                </tr>
                            </table>
                        </div>
                    </div>
                </td>
            </tr>
        </table>
        """
        return html
