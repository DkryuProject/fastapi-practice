from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import clean_unused_files, cleanup_expired_refresh_tokens

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(
        cleanup_expired_refresh_tokens,
        "interval",
        # minutes=1,
        hours=1,
        id="cleanup_refresh_tokens",
        replace_existing=True,
    )

    scheduler.add_job(
        clean_unused_files,
        "interval",
        # minutes=1,
        hours=6,
        id="clean_unused_files",
        replace_existing=True,
    )

    scheduler.start()