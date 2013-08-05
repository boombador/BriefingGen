
from Briefing import *
import ConfigParser
import os

cfg = ConfigParser.ConfigParser()
cfg.read("static.conf")
cfg.read("categories.conf")
brief = Briefing(cfg)

html = brief.printBriefingHTML()

briefingFile = brief.getFileName()
f = open(briefingFile, "w")
print "Writing briefing to file: " + briefingFile
f.write(html)
f.close()

# get archive dir, create it if not existent
archive = cfg.get("static", "archiveDir")
if not os.path.exists(archive):
    os.makedirs(archive)
os.chdir(archive)
print "Moving to archive directory: " + archive

briefingFile = brief.getFileName(True)
f = open(briefingFile, "w")
print "Writing briefing to file: " + briefingFile
f.write(html)
f.close()

print "Newsletter generated successfully, please press enter to terminate program..."
raw_input()

