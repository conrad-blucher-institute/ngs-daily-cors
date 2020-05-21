
import datetime
import os
import shutil
from datetime import date
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

# Return true if .env file exists


def isEnvFileAvailable():
    if os.path.exists('.env'):
        return True
    return False

# Return formatted string


def getTodayDate():
    today = date.today()
    return today.strftime("%B%d")


# Today is the nth day of current year (julian date)
# convert to string and padding 3
def getTodayPosition():
    return str(((date.today() - date(getCurrentYear(), 1, 1)).days)).zfill(3)

# return an int


def getCurrentYear():
    return datetime.datetime.now().year

# Write to log file (not being used)


def appendLog(msg):
    fileNameWithPath = "./log/" + \
        str(getCurrentYear()) + "_" + getTodayPosition() + ".txt"

    if not os.path.exists(fileNameWithPath):
        with open(fileNameWithPath, 'w'):
            pass
    out = open(fileNameWithPath, "a")
    logMsg = datetime.datetime.now().strftime("%H:%M:%S.%f") + ": " + msg + "\n"
    out.write(logMsg)
    out.close()

# Append to log and print


def logPrint(msg):
    print(msg)
    appendLog(msg)

# Get Array of site data from sites.txt


def getSites():
    with open('sites.txt') as f:
        sitesArray = f.read().splitlines()
    return sitesArray


# DEPRECATED: Move file to dir specified in the .env file
def moveFileToStorage(site, filename):
    STORAGE_FULL_PATH = str(os.getenv("STORAGE_DESTINATION_PATH"))
    path = STORAGE_FULL_PATH + "/" + str(getCurrentYear()) + "/" + site
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        shutil.move("./temp/" + filename, path + "/" + filename)
    except:
        logPrint("Failed: Cannot move file " + filename + " to " + path)
    else:
        logPrint("Moved file " + filename + " to " + path)


# Download today data and save to temp dir
def getSiteTodayData(ftp, site):
    STORAGE_FULL_PATH = str(
        os.getenv("STORAGE_DESTINATION_PATH")) + "/" + str(getCurrentYear()) + "/" + site
    if not os.path.exists(STORAGE_FULL_PATH):
        os.makedirs(STORAGE_FULL_PATH)
    try:
        ftp.cwd(site)
    except:
        logPrint("Failed: Remote directory " + site +
                 " does not exist or script is canceled manually.")
    else:
        targetFileExt = str(getCurrentYear())[:2] + 'd.Z'
        filename = site + getTodayPosition() + '0.' + targetFileExt
        try:
            ftp.retrbinary("RETR " + filename,
                           open(STORAGE_FULL_PATH + "/" + filename, "wb").write)
        except:
            logPrint("Failed: Cannot download file from site " + site +
                     ". File may not exist or has a different name.")
            # go back one dir in ftp
            ftp.cwd('../')
        else:
            # go back one dir in ftp
            ftp.cwd('../')
            logPrint("Downloaded: " + filename +
                     " | Site " + site + " | Path: " + ftp.pwd())
            # File is now downloaded straight to the storage so no need to move it
            # moveFileToStorage(site, filename)
