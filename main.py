
from Briefing import *
import ConfigParser
import os

if len(sys.argv) > 1 :
    cc = int(sys.argv[1])
else :
    cc = 0

cfg = ConfigParser.ConfigParser()
cfg.read("static.conf")
cfg.read("categories.conf")
brief = Briefing(cfg, cc)

html = brief.printBriefingHTML()

briefingFile = brief.getFileName()
f = open(briefingFile, "w")
# print "Info: Writing briefing to file: " + briefingFile
f.write(html)
f.close()

# get archive dir, create it if not existent
archive = cfg.get("static", "archiveDir")
if not os.path.exists(archive):
    os.makedirs(archive)
os.chdir(archive)
# print "Info: Moving to archive directory: " + archive

briefingFile = brief.getFileName(True)
f = open(briefingFile, "w")
# print "Info: Writing briefing to file: " + briefingFile
f.write(html)
f.close()

# print "Info: Newsletter generated successfully"

