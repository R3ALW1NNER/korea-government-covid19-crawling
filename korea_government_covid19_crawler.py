# Create based on python 3.8
import time

import requests
from bs4 import BeautifulSoup, element

import date_util
from constant import *

base_url = "https://www.cdc.go.kr"
list_url = base_url + "/board/board.es?mid=a20501000000&bid=0015"


def get_today_post_link():
    url = None

    # Get today post link
    while not url:
        req = requests.get(list_url)
        bs = BeautifulSoup(req.text, "html.parser")
        for row in bs.find("div", {"class": "dbody"}).find_all("ul"):
            if row.find("li", {"class": "title title2"}).find("a").get("title").find(date_util.today_date_str()) > -1:
                url = row.find("li", {"class": "title title2"}).find("a").get("href")
                break
        else:
            print("data not created... 10 sec sleep")
            time.sleep(10)

    return base_url + url


def get_today_post_to_bs4():
    detail_req = requests.get(get_today_post_link())
    return BeautifulSoup(detail_req.text, "html.parser")


def internal_parsing(internal_result_dict):
    bs = get_today_post_to_bs4()

    internal_rows = bs.find_all("tbody")[0].find_all("tr")
    internal_title_row = internal_rows[0]
    internal_new_data_row = internal_rows[1]
    internal_total_data_row = internal_rows[2]

    key_data_list = list()
    for i, row in enumerate(internal_title_row):
        if isinstance(row, element.NavigableString) or i == 1:
            continue
        key_data_list.append(row.find("p").text)

    new_data_list = list()
    for i, row in enumerate(internal_new_data_row):
        if isinstance(row, element.NavigableString) or i == 1:
            continue
        new_data_list.append(row.find("p").text.replace("*", "").replace(",", ""))

    total_data_list = list()
    for i, row in enumerate(internal_total_data_row):
        if isinstance(row, element.NavigableString) or i == 1:
            continue
        total_data_list.append(row.find("p").text.replace("*", "").replace(",", ""))

    # Country summary
    for i, key in enumerate(key_data_list):
        internal_result_dict[key] = {
            "new": int(new_data_list[i]),
            "total": int(total_data_list[i])
        }


def oversea_parsing(oversea_result_dict):
    bs = get_today_post_to_bs4()
    oversea_rows = bs.find_all("tbody")[1].find_all("tr")
    oversea_new_data_row = oversea_rows[2]
    oversea_total_data_row = oversea_rows[3]

    oversea_new_data = None
    for i, row in enumerate(oversea_new_data_row):
        if isinstance(row, element.NavigableString) or i == 1:
            continue
        oversea_new_data = int(row.text.replace("\n", "").replace("*", "").replace(",", ""))
        break

    oversea_total_data = None
    for i, row in enumerate(oversea_total_data_row):
        if isinstance(row, element.NavigableString) or i == 1:
            continue
        oversea_total_data = int(row.text.replace("\n", "").replace("*", "").replace(",", ""))
        break

    oversea_result_dict["해외"] = {
        "new": oversea_new_data, "total": oversea_total_data
    }


def definite_mgmt_state(definite_state_dict):
    bs = get_today_post_to_bs4()
    definite_state_rows = bs.find_all("tbody")[2].find_all("tr")
    today_str = date_util.today_date_str("abnormal")

    isolation_clear = None
    isolation_ing = None
    death = None

    for i, row in enumerate(definite_state_rows):
        if isinstance(row, element.NavigableString):
            continue
        if row.find("td").text.find(today_str) > -1:
            data = row.find_all("td")
            isolation_clear = int(data[1].text.replace("\n", "").replace("*", "").replace(",", ""))
            isolation_ing = int(data[2].text.replace("\n", "").replace("*", "").replace(",", ""))
            death = int(data[4].text.replace("\n", "").replace("*", "").replace(",", ""))

    definite_state_dict[K_ISOLATION_CLEAR] = isolation_clear
    definite_state_dict[K_ISOLATION_ING] = isolation_ing
    definite_state_dict[K_DEATH] = death
