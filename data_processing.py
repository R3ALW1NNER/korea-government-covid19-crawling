import pprint
from collections import OrderedDict

import telegram

import korea_government_covid19_crawler
from constant import *
from database import Database
from date_util import today_date_yyyymmdd

internal_dict = OrderedDict()
oversea_dict = OrderedDict()
definite_dict = OrderedDict()


def parsing_data_to_db():
    today_date_str = today_date_yyyymmdd()
    definite_sql = """
    insert into crawler_kr_covid19_daily_definite(stat_date, gubun, new_definite, total_definite)
    values('%s', '%s', %s, %s)
    """

    detail_sql = """
    insert into crawler_kr_covid19_daily_detail(stat_date, isolation_clear, isolation_ing, death)
    values('%s', %s, %s, %s)
    """

    db = Database()

    print("국내 DB INSERT")
    with db.get_cursor() as cursor:
        try:
            for gubun in internal_dict:
                cursor.execute(definite_sql % (today_date_str, gubun,
                                               internal_dict[gubun]["new"], internal_dict[gubun]["total"]))
            db.commit()
        except BaseException as e:
            cursor.rollback()
            print(e)

    print("해외 DB INSERT")
    with db.get_cursor() as cursor:
        try:
            for gubun in oversea_dict:
                cursor.execute(definite_sql % (today_date_str, gubun,
                                               oversea_dict[gubun]["new"], oversea_dict[gubun]["total"]))
            db.commit()
        except BaseException as e:
            cursor.rollback()
            print(e)

    print("확진자 관리 현황 DB INSERT")
    with db.get_cursor() as cursor:
        try:
            cursor.execute(detail_sql % (today_date_str, definite_dict[K_ISOLATION_CLEAR],
                                         definite_dict[K_ISOLATION_ING], definite_dict[K_DEATH]))

            db.commit()
        except BaseException as e:
            cursor.rollback()
            print(e)


def crawling_start():
    korea_government_covid19_crawler.internal_parsing(internal_dict)
    korea_government_covid19_crawler.oversea_parsing(oversea_dict)
    korea_government_covid19_crawler.definite_mgmt_state(definite_dict)

    pprint.pprint(internal_dict)
    pprint.pprint(oversea_dict)
    pprint.pprint(definite_dict)


def send_telegram_message():
    msg_fmt = """{date} 0시 기준
- 신규 확진자: {total} 명(국내: {internal} 명, 해외: {oversea} 명) 
- 격리해제: {isolation_clear} 명
- 격리중: {isolation_ing} 명
- 누적 사망자: {death} 명

----- 신규 확진자 지역별 발생 현황 -----\n"""

    msg_sub_fmt = "{area}: {new} 명\n"

    token = "telegram token"
    chat_id = "chat ID"

    bot = telegram.Bot(token=token)

    msg = msg_fmt.format(
        date=today_date_yyyymmdd(), total=internal_dict["합계"]["new"] + oversea_dict["해외"]["new"],
        internal=internal_dict["합계"]["new"], oversea=oversea_dict["해외"]["new"],
        isolation_clear=definite_dict[K_ISOLATION_CLEAR], isolation_ing=definite_dict[K_ISOLATION_ING],
        death=definite_dict[K_DEATH]
    )

    del internal_dict["합계"]

    for k in internal_dict:
        if internal_dict[k]["new"] == 0:
            continue
        msg += msg_sub_fmt.format(area=k, new=internal_dict[k]["new"])

    bot.sendMessage(chat_id=chat_id, text=msg)
