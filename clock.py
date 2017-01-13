import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()


# TODO: To be added in deploy.rb
# day_of_week=0 sets the clock to be activated weekly on Monday
@sched.scheduled_job('cron', day_of_week=0)
def clean_jwt_tokens():
    subprocess.call('python manage.py clean_old_jwt_tokens', shell=True, close_fds=True)

sched.start()
