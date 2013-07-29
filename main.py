
from Briefing import *
import ConfigParser

cfg = ConfigParser.ConfigParser()
cfg.read("static.conf")
cfg.read("categories.conf")
brief = Briefing(cfg)

f = open("DailyBriefing.html", "w")
f.write(brief.printBriefingHTML())
