
from Briefing import *
import ConfigParser
import os
import pprint

if len(sys.argv) > 1 :
    cc = int(sys.argv[1])
else :
    cc = 0

cfg = ConfigParser.ConfigParser()
cfg.read("top.conf")

brief = Briefing(cfg, cc)
brief.readTheme()
brief.parseTheme()
brief.readContent()

html = brief.printBriefingHTML()

briefingFile = brief.getFileName()
f = open(briefingFile, "w")
f.write(html)
f.close()

# get archive dir, create it if not existent
if not os.path.exists(brief.archiveDir):
    os.makedirs(brief.archiveDir)
os.chdir(brief.archiveDir)

briefingFile = brief.getFileName(True)
f = open(briefingFile, "w")
f.write(html)
f.close()

os.chdir('..')

# print version
cfg.read("print.conf")
brief = Briefing(cfg, cc)
brief.readTheme()
brief.parseTheme()
html = brief.printBriefingHTML()
briefingFile = brief.getFileName(False, 'Print')
f = open(briefingFile, "w")
f.write(html)
f.close()
