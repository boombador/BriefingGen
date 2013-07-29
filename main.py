
from Briefing import *
import ConfigParser

cfg = ConfigParser.ConfigParser()
cfg.read("static.conf")

from makeHtml import *

categories = ConfigParser.ConfigParser()
categories.read("categories.conf")

brief = Briefing(cfg)

currdate = datetime.now().strftime('%Y%m%d')

# dp = DictReader(open('DailyPractice' + currdate + '.csv', "rb"), delimiter="|")
# stat = DictReader(open('StaticData.csv', "rb"), delimiter="|")

#parse the dictreader, this way we can know how many practices we have before printing them
# dailyPractices = []
# for row in dp :
    # prac = { "Category": escape(detexify(row['Category'])), 'Contributor': escape(detexify(row['Contributor'])), 'Text': escape(detexify(row['Practice'])), 'URL': escape(detexify(row['Link_URL'])) }
    # dailyPractices.append(prac)
# numPractices = len(dailyPractices)

brief.printBriefingHTML()
