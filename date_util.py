import platform
from datetime import datetime


def today_date_str(flag="normal"):
    # %Y/%-m/%-d Linux, MacOS
    # %Y/%#m/%#d Windows
    if flag == "normal":
        if platform.platform().lower().find("windows") > -1:
            today_str = datetime.now().strftime("%#m월 #%d일, 0시")
        else:
            today_str = datetime.now().strftime("%-m월 %-d일, 0시")
    else:
        if platform.platform().lower().find("windows") > -1:
            today_str = datetime.now().strftime("%#m.%#d.")
        else:
            today_str = datetime.now().strftime("%-m.%-d.")
    return today_str


def today_date_yyyymmdd():
    return datetime.now().strftime("%Y-%m-%d")
