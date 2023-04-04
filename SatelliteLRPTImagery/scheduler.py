import datetime
import time
import schedule
from pyorbital import tlefile
from pyorbital.orbital import Orbital
import subprocess

tle = tlefile.read("/path/to/tle.txt")
orb = Orbital("METEOR-M 2", tle)

def capture_imagery():
    # Set up RTL-SDR parameters
    freq = 137.1e6
    samp_rate = 2.4e6
    gain = 30

    # Set up file name and path
    file_name = "lrpt_{0}.raw".format(datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S"))
    file_path = "/path/to/save/raw/file/"

    # Use RTL-SDR to capture the raw data
    subprocess.call(["rtl_sdr", "-f", str(freq), "-s", str(samp_rate), "-g", str(gain), "-n", "120000000", file_path + file_name])

    # Use GQRX to convert the raw data to an image file
    subprocess.call(["gqrx-remote", "-c", "set freq={0}M;set gainmode=lna;set mode=LRPT;set lna=1;set vga=10;set samp_rate={1};set rtl_sdr_dev=/dev/rtl_sdr_0;".format(freq/1e6, samp_rate/1e6), "-r", file_path + file_name, "-f", "jpeg", "-o", file_path])

# Define the start and end time for the scheduled data capture
start_time = datetime.time(hour=8, minute=0)
end_time = datetime.time(hour=18, minute=0)

# Define the time interval for data capture
time_interval = 10  # minutes

# Schedule the data capture
schedule.every().day.at(start_time.strftime("%H:%M")).do(capture_imagery)
schedule.every(time_interval).minutes.between(start_time.strftime("%H:%M"), end_time.strftime("%H:%M")).do(capture_imagery)

# Loop to run the scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)
