
from Briefing import *
import ConfigParser
import shutil

cfg = ConfigParser.ConfigParser()
cfg.read("static.conf")
cfg.read("categories.conf")
brief = Briefing(cfg)

html = brief.printBriefingHTML()
briefingFile = brief.getFileName()

f = open(briefingFile, "w")
f.write(html)
f.close()

archive = cfg.get("static", "archiveDir")
shutil.copy(briefingFile, archive)

