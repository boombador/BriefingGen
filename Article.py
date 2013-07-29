
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
            if len(toAdd) > 0 :
                self.content = self.content + ' ' + toAdd
            i+=1
        self.content = re.compile(r'\r?\n').sub(' ', self.content)
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
        # def printArticleHTML(categoryName, submitterName, articleText, articleTitle="", linkUrl="") :
        categoryName = self.category
        submitterName = self.contributor
        articleText = self.content
        articleTitle = self.title
        linkUrl = self.href

        imgsrc = 'https://imga.nxjimg.com/secured/image/briefing/'
        isDailyTeaching = False
        barColor = "#f47321"
        backgroundColor="#f4f5f4"

        if ('Technology News' == categoryName) :
            imgsrc += 'technology.jpg'
        elif ('eCommerce News' == categoryName) :
            imgsrc = 'http://imgb.nxjimg.com/emp_image/dailybriefing/ecommerce.png'
        elif ('eCommerce News' == categoryName) :
            imgsrc = 'http://imgb.nxjimg.com/emp_image/dailybriefing/ecommerce.png'
        elif ('STEM Education' == categoryName) :
            imgsrc += 'technology.jpg'
        elif ('Wellness' == categoryName) :
            imgsrc += 'wellness.jpg'
            barColor = '#4bc23b'
            backgroundColor = '#dcf9d8'
        elif ('Marketing' == categoryName) :
            imgsrc += 'marketing.jpg'
        elif ('Design' == categoryName) :
            imgsrc += 'design.jpg '
        elif ('Next Jump Teachings' == categoryName) :
            imgsrc += 'dteaching.jpg'
            isDailyTeaching = True
        elif ('Bigger Hearts' == categoryName) :
            imgsrc = 'http://imgb.nxjimg.com/emp_image/dailybriefing/heart.png'
            barColor = '#ED0C31'
        else :
            imgsrc += 'marketing.jpg'

        html = """
        <table border="0" cellpadding="0" cellspacing="0" width="100%">
            <tr height="30" bgcolor=\"""" + barColor + """" class="articleBar">
                <td width="36">
                    <img src=\"""" + imgsrc + """" width="36" height="30">
                </td>
                <td width="100%" style="color: white; font-family: Calibri;" class="articleBarText">
                    <b>""" + categoryName.upper() + """</b>"""
        if not isDailyTeaching :
            html += """ - submitted by """ + submitterName
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
        if not isDailyTeaching :
            html += """ class="readMoreLink\""""

        html += """>
                                    <td></td>
                                    <td align="left">"""
        if isDailyTeaching :
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
