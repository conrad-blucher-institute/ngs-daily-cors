import os
from ftplib import FTP
from functions import *
import datetime

if isEnvFileAvailable() == False:
    print("Cannot find .env file. Please create .env file based on .env.dist")
    print("Exiting script.....")
    exit()

STORAGE_PATH = os.getenv("STORAGE_PATH")
# login to ftp server and navigate to the CORS directory of curren day and and year
# eg. ftp://www.ngs.noaa.gov/cors/rinex/2020/001/ (001 mean first day of 2020)
# "ftp://www.ngs.noaa.gov/cors/rinex/2020/001/1lsu/1lsu0010.20d.Z",
# cors/rinex/2020/001/1lsu/1lsu0010.20d.Z

start = datetime.datetime.now()
print("Getting CORS data from NOAA...")
print("Start Time: " + start.strftime("%Y-%m-%d %H:%M:%S"))

ftp = FTP("www.ngs.noaa.gov")
ftp.login()
ftp.cwd("cors/rinex")
ftp.cwd(str(getCurrentYear()))
ftp.cwd(getTodayPosition())


# List all files/dirs in ftp
# files = ftp.nlst()

# create dirs
if not os.path.exists('temp'):
    os.makedirs('temp')

# get sites from sites.txt
sites = getSites()

# Download data for each sites and move them to the approriate directory
for site in sites:
    getSiteTodayData(ftp, site)


ftp.close()
end = datetime.datetime.now()
diff = end - start
print("Done.... End time: " + end.strftime("%Y-%m-%d %H:%M:%S"))
print("All files downloaded for " + str(diff.seconds) + "s")
