from apscheduler.schedulers.blocking import BlockingScheduler

from data_processing import send_telegram_message, crawling_start, parsing_data_to_db

sched = BlockingScheduler()


@sched.scheduled_job('cron', hour=9)
def main_job():
    crawling_start()

    parsing_data_to_db()

    send_telegram_message()


if __name__ == '__main__':
    sched.start()
