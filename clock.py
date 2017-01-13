import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

# TODO: To be added in deploy.rb
# day_of_week=0 sets the clock to be activated weekly on Monday
# @sched.scheduled_job('cron', day_of_week=0)
# def clean_jwt_tokens():
#     subprocess.call('python manage.py clean_old_jwt_tokens', shell=True, close_fds=True)

# Runs from Monday to Friday at 9:30 (am) until 2016-02-24,
# when 101 courses finished
sched.scheduled_job('cron',day_of_week='mon-fri', end_date='2016-02-24')
def calculate_presence_command():
    print("Lqlq")
    subprocess.call('python manage.py calculate_presence', shell=True, close_fds=True)

sched.start()
