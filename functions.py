
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


def getTodayDate():
    today = date.today()
    return today.strftime("%B%d")


# Today is the nth day of current year (julian date)
# convert to string and padding 3
def getTodayPosition():
    return str(((date.today() - date(getCurrentYear(), 1, 1)).days)).zfill(3)


def getCurrentYear():
    return datetime.datetime.now().year

# Write to log file (not being used)
def appendLog():
    currentDateTime = datetime.datetime.now()
    out = open("log.txt", "a")
    out.write("Run at " + str(currentDateTime) + "\n")
    out.close()

# Get Array of site data from sites.txt
def getSites():
    with open('sites.txt') as f:
        sitesArray = f.read().splitlines()
    return sitesArray


# Move file to dir specified in the .env file
def moveFileToStorage(site, filename):
    STORAGE_FULL_PATH = str(os.getenv("STORAGE_DESTINATION_PATH"))
    path = STORAGE_FULL_PATH + "/" + str(getCurrentYear())
    if not os.path.exists(path):
        os.makedirs(path)
    path += "/" + site
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        shutil.move("./temp/" + filename, path + "/" + filename)
    except:
        print("Failed: Cannot move file " + filename + " to " + path)
    else:
        print("Moved file" + filename + " to " + path)


# Download today data and save to temp dir
def getSiteTodayData(ftp, site):
    try:
        ftp.cwd(site)
    except:
        print("Failed: Remote directory " + site +
              " does not exist or script is canceled manually.")
    else:
        targetFileExt = str(getCurrentYear())[:2] + 'd.Z'
        filename = site + getTodayPosition() + '0.' + targetFileExt
        try:
            ftp.retrbinary("RETR " + filename,
                           open("temp/" + filename, "wb").write)
        except:
            print("Failed: Cannot download file from site " + site +
                  ". File may not exist or has a different name.")
            # go back one dir in ftp
            ftp.cwd('../')
        else:
            # go back one dir in ftp
            ftp.cwd('../')
            print("Downloaded: " + filename +
                  " | Site " + site + " | Path: " + ftp.pwd())
            moveFileToStorage(site, filename)
            # Move data to storage
