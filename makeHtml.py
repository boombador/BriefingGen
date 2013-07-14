#!/usr/bin/python
from datetime import datetime, timedelta
from csv import *
import re
from cgi import escape

import pprint

def detexify(str) :
    simpleEscaped = re.compile(r'\\([#$%&~_^{}|])')
    mathEscaped = re.compile(r'\$([<>])\$')
    str = mathEscaped.sub(r'\1', str)
    str = simpleEscaped.sub(r'\1', str)
    str = str.replace('\\textbacklash', '\\')
    return str

currdate = datetime.now().strftime('%Y%m%d')

dp = DictReader(open('DailyPractice' + currdate + '.csv', "rb"), delimiter="|")
articles = DictReader(open('Articles' + currdate + '.csv', "rb"), delimiter="|")
stat = DictReader(open('StaticData.csv', "rb"), delimiter="|")

#parse the dictreader, this way we can know how many practices we have before printing them
dailyPractices = []
for row in dp :
    prac = { "Category": escape(detexify(row['Category'])), 'Contributor': escape(detexify(row['Contributor'])), 'Text': escape(detexify(row['Practice'])), 'URL': escape(detexify(row['Link_URL'])) }
    dailyPractices.append(prac)
numPractices = len(dailyPractices)

static = stat.next()
    
def hexColor(str) :
    return "#%02X%02X%02X" % tuple([int(num) for num in str.split()])

def printBriefingHTML(articles) :
    print """
    <style>
    @media screen {
        .overflowEllipsis {
            display: none;
        }
    }
    @media print {
        table {
            font-size: 11px;
        }
        .articleBar {
            height: 20px;
        }
        .articleBar img {
            height: 19px;
            width: 24px;
        }
        .articleTitle {
            font-size: 12px !important;
        }
        .readMoreLink {
            display: none;
        }
        .articleBoxWrapper {
            padding-bottom: 10px;
        }
        .articleBoxWrapper.noTitle {
            padding-bottom: 18px;
        }
        .articleBox {
            max-height: 130px;
            overflow: hidden;
            position: relative;
        }
        .noTitle .articleBox {
            max-height:124px;
        }
        .overflowEllipsis {
            display: block;
            position: absolute;
            right: 15;
            bottom: 2;
            background-color: #f4f5f4;
            padding-left: 10px;
        }
        .noTitle .overflowEllipsis {
            bottom: 0;
        }
        .articleBoxTopSpacer {
            height: 5px;
        }
        .articleBoxBottomSpacer {
            display: none;
        }
    }
    </style>

    <table border="0" style="background-color:#FFFFFF; max-width: 960px; font-family: Calibri;" cellpadding="0" cellspacing="0">
        <tr><td>
            <!-- Header section table -->
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                    <td width="200" style="font-family: Calibri;">
                        """ + datetime.now().strftime('%B %d, %Y') + """<br/>
                        Daily Briefing: """ + escape(detexify(static['CVerb']))  + " by " + escape(detexify(static['Compiler'])) +"""<br/>
                        <a href="https://briefing.nextjump.com/">Daily Briefing Site</a><br/>
                        <a href="https://wiki.nextjump.com/wiki/index.php/Daily_Briefing">Daily Briefing Wiki</a>
                    </td>
                    <td width="760" valign="middle" align="right">
                        <img src="https://imga.nxjimg.com/secured/image/briefing/dblogo.jpg" width="300" height="65">
                    </td>
                </tr>
                <tr height="10">
                </tr>
            </table>
            <table border="0" cellpadding="0" cellspacing="0" width="100%">"""
            
    if numPractices > 0 :
        if numPractices == 1 :
            print """
                <tr><!-- begin dp section -->
                    <td width="100%">"""
            row = dailyPractices[0]
            printArticleHTML(row['Category'], row['Contributor'], row['Text'], '', row['URL'])
            print """
                    </td>
                </tr>"""
        else :
            print """
                <tr><!-- more than 1 daily practice -->
                    <td width="100%">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                            <tr valign="top">
                                <td width="30%">"""
            row = dailyPractices[0]
            printArticleHTML(row['Category'], row['Contributor'], row['Text'], '', row['URL'])
            print """
                                </td>
                                <td width="2%"></td>
                                <td width="68%">"""
            row = dailyPractices[1]
            printArticleHTML(row['Category'], row['Contributor'], row['Text'], '', row['URL'])
            print """
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>"""

    for row in articles :
        print """
                <tr>
                    <td width="100%">
                    """
        printArticleHTML(escape(detexify(row['Category'])), escape(detexify(row['Contributor'])), escape(detexify(row['Text'])), escape(detexify(row['Title'])), escape(detexify(row['URL'])))
        print """
                    </td>
                </tr>"""
    print """
            </table>
        <!-- Footer table-->
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr height="10">
                </tr>
                <tr>
                    <td align="center">
                        Want to get involved? Email comments, suggestions, and articles to Team Daily Briefing!
                    </td>
                </tr>
            </table>
        </td></tr>
    </table>"""

     
def printArticleHTML(categoryName, submitterName, articleText, articleTitle="", linkUrl="") :
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

    print """
    <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr height="30" bgcolor=\"""" + barColor + """" class="articleBar">
            <td width="36">
                <img src=\"""" + imgsrc + """" width="36" height="30">
            </td>
            <td width="100%" style="color: white; font-family: Calibri;" class="articleBarText">
                <b>""" + categoryName.upper() + """</b>"""
    if not isDailyTeaching :
        print """ - submitted by """ + submitterName
    print """
            </td>
        </tr>
        <tr>
            <td colspan="2" bgcolor=\"""" + backgroundColor + """">
                <div class="articleBoxWrapper">
                    <div class="articleBox">"""

    print """
                        <table width="100%" border="0" cellpadding="0" cellspacing="0">
                            <tr height="10" class="articleBoxTopSpacer">
                                <td colspan="3"></td>
                            </tr>"""
    if articleTitle :
        print """
                            <tr><!-- Title row, not always needed -->
                                <td width="15"></td>
                                <td align="left" style="font-size: 18px; font-weight: 700;" class="articleTitle">""" + articleTitle + """</td>
                                <td width="15"></td>
                            </tr>
                            <tr height="5">
                            </tr>"""
    print """
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
        print """ class="readMoreLink\""""

    print """>
                                <td></td>
                                <td align="left">"""
    if isDailyTeaching :
        print submitterName
    else : 
        print """<a href=\"""" + linkUrl + """">Read More</a>"""
    print """
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

printBriefingHTML(articles)
