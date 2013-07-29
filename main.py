
from Briefing import *
import ConfigParser

cfg = ConfigParser.ConfigParser()
cfg.read("static.conf")
cfg.read("categories.conf")
brief = Briefing(cfg)

#parse the dictreader, this way we can know how many practices we have before printing them
# dailyPractices = []
# for row in dp :
    # prac = { "Category": escape(detexify(row['Category'])), 'Contributor': escape(detexify(row['Contributor'])), 'Text': escape(detexify(row['Practice'])), 'URL': escape(detexify(row['Link_URL'])) }
    # dailyPractices.append(prac)
# numPractices = len(dailyPractices)

f = open("DailyBriefing.html", "w")
f.write(brief.printBriefingHTML())
