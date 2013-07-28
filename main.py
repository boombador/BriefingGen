
from Article import *
from getArticles import *
import ConfigParser

cfg = ConfigParser.ConfigParser()
cfg.read("static.conf")

from makeHtml import *

"""
import sys

if len(sys.argv)>1 :
    try:
        MINLENGTH = int(sys.argv[1])
    except:
        pass
"""

config = ConfigParser.ConfigParser()
config.read("categories.conf")
defaults = config.options("Default")


briefingUrl = "https://briefing.nextjump.com/?feed=rss2"
briefConn = urlopen(briefingUrl)
briefing = briefConn.read()

soup = BeautifulSoup(briefing)
articles = []

for item in  soup.findAll('item', limit=5) :
    articles.append(Article(item))

for article in articles :
    print article

# print "URL|Title|Category|Contributor|Text"

# for article in articles :
    # print(article.csv())

currdate = datetime.now().strftime('%Y%m%d')

# dp = DictReader(open('DailyPractice' + currdate + '.csv', "rb"), delimiter="|")
# articles = DictReader(open('Articles' + currdate + '.csv', "rb"), delimiter="|")
# stat = DictReader(open('StaticData.csv', "rb"), delimiter="|")

#parse the dictreader, this way we can know how many practices we have before printing them
# dailyPractices = []
# for row in dp :
    # prac = { "Category": escape(detexify(row['Category'])), 'Contributor': escape(detexify(row['Contributor'])), 'Text': escape(detexify(row['Practice'])), 'URL': escape(detexify(row['Link_URL'])) }
    # dailyPractices.append(prac)
# numPractices = len(dailyPractices)

# static = stat.next()

# printBriefingHTML(articles, cfg)
