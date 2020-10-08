import logging

from apscheduler.schedulers.blocking import BlockingScheduler

from data_processing import send_telegram_message, crawling_start, parsing_data_to_db

LOGGING_FORMATTER = '[%(asctime)s] [%(filename)s:%(process)d:%(funcName)s:%(lineno)s|%(levelname)s] %(message)s'

log = logging.getLogger()
log.setLevel(logging.DEBUG)

formatter = logging.Formatter(LOGGING_FORMATTER, datefmt='%Y-%m-%d %H:%M:%S')

fileHandler = logging.FileHandler('./korea-government-covid19-crawling.log')
streamHandler = logging.StreamHandler()

fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

log.addHandler(fileHandler)
log.addHandler(streamHandler)

sched = BlockingScheduler()


@sched.scheduled_job('cron', hour=9)
def main_job():
    crawling_start()

    parsing_data_to_db()

    send_telegram_message()


if __name__ == '__main__':
    sched.start()
