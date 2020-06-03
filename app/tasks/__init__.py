# -*- coding: utf-8 -*-

from app.extensions import celery
from celery import platforms, Task
from celery.utils.log import get_task_logger
from celery.schedules import crontab
from datetime import timedelta
from kombu import Exchange, Queue

logger = get_task_logger(__name__)

platforms.C_FORCE_ROOT = True


class CustomerTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        logger.info("task done: {}".format(task_id))
        return super(CustomerTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error("task fail, task_id {}, reason: {}".format(task_id, exc))
        return super(CustomerTask, self).on_failure(exc, task_id, args, kwargs, einfo)


def init():
    celery_redis_db = 5
    url = "redis://{}:6379/{}".format(config.config["redis_ip"], celery_redis_db)
    celery.conf.update(
        CELERY_QUEUES=(
            Queue("celery", Exchange("celery"), routing_key="default"),
            Queue("statistic", Exchange("statistic"), routing_key="default"),
        ),
        CELERY_DEFAULT_QUEUE="celery",
        CELERY_DEFAULT_ROUTING_KEY="default",
        CELERY_DEFAULT_EXCHANGE_TYPE="direct",
        BROKER_URL=url,
        CELERY_RESULT_BACKEND=url,
        CELERY_RESULT_PERSISTENT=True,
        CELERY_TASK_RESULT_EXPIRES=300,
        CELERY_TASKS_SERIALIZER="json",
        CELERY_ACCEPT_CONTENT=["json", "pickle"],
        CELERY_RESULT_SERIALIZER="json",
        CELERY_TIMEZONE="Asia/Shanghai",
        CELERY_ENABLE_UTC=True,
        CELERYD_FORCE_EXECV=True,  # 有些情况可以防止死锁
        CELERYD_CONCURRENCY=10,
        CELERYD_MAX_TASKS_PER_CHILD=100,  # 每个worker最多执行100个任务就会被销毁，可防止内存泄露
        BROKER_TRANSPORT_OPTIONS={
            "visibility_timeout": 86400
        },  # 24 hour之后未被消费成功的数据将被resend
        TOTORO_AMQP_CONNECTION_POOL={
            "max_idle_connections": 1,
            "max_open_connections": 500,
            "max_recycle_sec": 3600,
        },
        CELERYBEAT_SCHEDULE={
            # 更新非小号和其它交易所币价
            "market_price": {
                "task": "market_price",
                "schedule": crontab(minute="*/30"),
                "args": (),
            },
            # 每日9:30
            "wallet_deposit_statistic": {
                "task": "wallet_deposit_statistic",
                "schedule": crontab(minute=30, hour=9),
                # "schedule": crontab(minute='*/1'),
                # 'schedule': timedelta(seconds=1),
                "args": (),
            },
            # 每日凌晨1点
            "data_cleaner": {
                "task": "data_cleaner",
                "schedule": crontab(minute=0, hour=1),
                "args": (),
            },
            # # 每日早上8点
            # "bkbt_daily_statistic": {
            #     "task": "bkbt_daily_statistic",
            #     'schedule': crontab(minute=0, hour=8),
            #     "args": ()
            # },
            # 每日凌晨0点
            "asset_snapshot": {
                "task": "asset_snapshot",
                "schedule": crontab(minute=0, hour=0),
                "args": (),
            },
            # 每日早上8点
            "transfer_statistic": {
                "task": "transfer_statistic",
                "schedule": crontab(minute=0, hour=8),
                "args": (),
            },
            # # 每日早上6点
            # "market_etc_statistic": {
            #     "task": "market_etc_statistic",
            #     'schedule': crontab(minute=0, hour=6),
            #     "args": ()
            # },
            # 每日早上9点
            "doge_send_statistic": {
                "task": "doge_send_statistic",
                "schedule": crontab(minute=0, hour=9),
                "args": (),
            },
            # 每日早上9点
            # "coin_query": {
            #     "task": "coin_query",
            #     'schedule': crontab(minute=0, hour=9),
            #     "args": ()
            # },
            # 每隔一个小时
            "trx_task": {
                "task": "trx_task",
                "schedule": crontab(minute=0, hour="*/1"),
                "args": (),
            },
            # 每隔一个小时
            "newyear_asset_statistic": {
                "task": "newyear_asset_statistic",
                "schedule": crontab(minute=0, hour="*/1"),
                "args": (),
            },
            # # 每天凌晨1点
            # "newyear_coin_send": {
            #     "task": "newyear_coin_send",
            #     'schedule': crontab(minute=0, hour=1),
            #     "args": ()
            # },
            # # 每天2点执行
            # "invite_statistic_task": {
            #     "task": "invite_statistic_task",
            #     'schedule': crontab(minute=0, hour=2),
            #     "args": ()
            # },
            # 每天5点执行
            "atc_giveout_daily_task": {
                "task": "atc_giveout_daily_task",
                "schedule": crontab(minute=0, hour=5),
                "args": (),
            },
            # 每天23:55:00点执行
            "earnings_job_health_task": {
                "task": "earnings_job_health_task",
                "schedule": crontab(minute=5, hour=0),
                "args": (),
            },
            # 每天6点执行
            "atc_unfrozen_daily_task": {
                "task": "atc_unfrozen_daily_task",
                "schedule": crontab(minute=0, hour=6),
                "args": (),
            },
            "eos_balance_check": {
                "task": "eos_balance_check",
                "schedule": crontab(minute=30, hour=6),
                "args": (),
            },
            "amount_check": {
                "task": "amount_check",
                "schedule": crontab(minute=0, hour=7),
                "args": (),
            },
            "monitor_import_addrs": {
                "task": "monitor_import_addrs",
                "schedule": crontab(minute=0, hour="*/2"),
                "args": (),
            },
            "update_eth_tx_fee": {
                "task": "update_eth_tx_fee",
                "schedule": timedelta(seconds=30),
                "args": (),
            },
            "update_btc_tx_fee": {
                "task": "update_btc_tx_fee",
                "schedule": crontab(minute="*/10"),
                "args": (),
            },
            "check_address_and_walletId": {
                "task": "check_address_and_walletId",
                "schedule": crontab(minute="*/10"),
                "args": (),
            },
        },
    )

    from . import market_price


init()
