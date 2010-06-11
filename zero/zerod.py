from twisted.internet import reactor
from twisted.scheduling.cron import CronSchedule
from twisted.scheduling.task import ScheduledCall
from celery import conf
from celery.registry import tasks
import zero.crontask

def main():
    from celery.loaders import current_loader
    current_loader().init_worker()
    schedule_tasks()
    reactor.run()

def schedule_tasks():
    cron_tasks = tasks.filter_types('cron')
    for task in cron_tasks.itervalues():
        schedule = CronSchedule(task.cron)
        call = ScheduledCall(task.delay, *task.args, **task.kwargs)
        call.start(schedule)
