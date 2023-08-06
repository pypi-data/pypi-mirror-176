import schedule
import time


def run_job(job, num: int, interval="second"):

    if interval == "second":
        schedule.every(num).seconds.do(job)
    elif interval == "minute":
        schedule.every(num).minutes.do(job)
    elif interval == "hour":
        schedule.every(num).hours.do(job)
    elif interval == "day":
        schedule.every(num).days.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
