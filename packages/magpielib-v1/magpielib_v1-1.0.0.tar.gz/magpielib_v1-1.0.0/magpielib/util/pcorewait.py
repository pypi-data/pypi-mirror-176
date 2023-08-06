import asyncio
import json
from magpielib.util.asynredis import AsyncRedisHandler
from magpielib.util.log import get_logger
logger = get_logger("pcore-wait")


class WaitPatchInfo:
    """patch 回调状态等待
    """
    def __init__(self, pw_info: dict):
        self.pid = pw_info.get('pid')
        self.redis_host = pw_info.get('redis').get('host')
        self.redis_port = pw_info.get('redis').get('port')
        self.redis_password = pw_info.get('redis').get('password')
        self.redis_db = pw_info.get('redis').get('db')


class PatchWaitDealer(AsyncRedisHandler):

    def __init__(self, redis_host, redis_port, redis_password, redis_db):
        super().__init__(redis_host, redis_port, redis_password, redis_db)
        self.pid = None
        self.done_notify_yet = False

    @staticmethod
    def get_instance(pw_info: WaitPatchInfo):
        if pw_info is None or pw_info.pid is None \
                or pw_info.redis_db is None or pw_info.redis_host is None \
                or pw_info.redis_password is None:
            raise Exception("pw_info 不合法，没有经过前端框架层校验")
        dealer = PatchWaitDealer(pw_info.redis_host, pw_info.redis_port, pw_info.redis_password, pw_info.redis_db)
        dealer.pid = pw_info.pid
        return dealer

    def notify(self, progress: float, msg: str, is_raw=False, forever=False):
        """通知 订阅者事件执行状态结果
        progress: 0~1，!=1 这时候 可以传process msg 等信息；这个时候忽略success信息; == 1 代表结束
        """
        # logger.info("@@@notify... start publish. progress:%s->%s->pid=%s", progress, msg, self.get_rpid())
        if self.done_notify_yet:
            raise Exception("已完成通知了，不能重复发送...")
        self.bucket.publish(self.get_rpid(), json.dumps({
            "Progress": progress,
            "Ok": progress >= 1,
            "Msg": msg,
            "IsRaw": is_raw
        }))
        if progress >= 1 or progress == -1 and not forever:  # float 类型不能判等于，会出现 1.000000000000001 的情况
            self.done_notify_yet = True

    async def wait4result(self, progress_func, done_func=None):
        """对应关注结果方在这里等待结果
        """
        client = self.bucket.pubsub()
        client.subscribe(self.get_wpid())
        logger.info("@@@-wait4result--->%s", self.get_wpid())
        while True:
            msg = client.get_message(ignore_subscribe_messages=True)
            if msg is None:
                await asyncio.sleep(0.005)
                continue
            # logger.info("@@@ *****patch wait receive--->%s", msg)
            data = json.loads(msg['data'])
            progress = data['Progress']
            ok = data['Ok']
            msg = data['Msg']
            if 1 > progress >= 0:  # -1 的时候也失败
                if progress_func:  # 调用方可能不关注 progress ，大部分可能就没有progress
                    progress_func(progress, msg)
            else:
                if done_func:
                    done_func(ok, msg)  # 一定要都done_func
                break
        logger.info("@@@ *****patch wait done!!!")
        client.unsubscribe(self.get_wpid())
        client.close()

    def get_wpid(self):
        """会被 ws 重写
        """
        return self.pid

    def get_rpid(self):
        """会被 ws 重写
        """
        return self.pid
