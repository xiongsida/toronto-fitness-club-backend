from apscheduler.schedulers.background import BackgroundScheduler
from . import business_logic


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(business_logic.remove_all_expired_subscriptions,
                      'interval',
                      seconds=60 * 60)
    scheduler.start()
