
from getArticles import *
import ConfigParser

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

print "URL|Title|Category|Contributor|Text"

for article in articles :
    print(article.csv())
