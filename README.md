This is a Python script to get daily cors data from NOAA at: ftp://www.ngs.noaa.gov/cors/
This should be run as cron job on a VM

### SETUP

- `pip install -r requirements.txt`
- Create `.env` file based on `.env.dist` and change the environment variable approriately

### ADD MORE SITES

- Modify `sites.txt` as desired (site name must be in lower case)

### RUN

- `python main.py`
