
from Article import *
import ConfigParser
from urllib import urlopen

cfg = ConfigParser.ConfigParser()
cfg.read("static.conf")

from makeHtml import *

categories = ConfigParser.ConfigParser()
categories.read("categories.conf")

url = cfg.get("static", "briefingUrl")
briefConn = urlopen(url)
briefing = briefConn.read()

soup = BeautifulSoup(briefing)
articles = []

for item in  soup.findAll('item', limit=5) :
    articles.append(Article(item))

currdate = datetime.now().strftime('%Y%m%d')

# dp = DictReader(open('DailyPractice' + currdate + '.csv', "rb"), delimiter="|")
# stat = DictReader(open('StaticData.csv', "rb"), delimiter="|")

#parse the dictreader, this way we can know how many practices we have before printing them
# dailyPractices = []
# for row in dp :
    # prac = { "Category": escape(detexify(row['Category'])), 'Contributor': escape(detexify(row['Contributor'])), 'Text': escape(detexify(row['Practice'])), 'URL': escape(detexify(row['Link_URL'])) }
    # dailyPractices.append(prac)
# numPractices = len(dailyPractices)

printBriefingHTML(articles, cfg)
