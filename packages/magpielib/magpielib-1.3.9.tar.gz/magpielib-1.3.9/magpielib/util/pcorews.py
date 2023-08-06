from magpielib.util.pcorewait import PatchWaitDealer
from magpielib.util.log import get_logger
logger = get_logger("pcore-ws")


class WsPatchInfo:
    """patch 回调状态等待 针对ws长连接
    """
    def __init__(self, pw_info: dict):
        self.wpid = pw_info.get('wpid')
        self.rpid = pw_info.get('rpid')
        self.redis_host = pw_info.get('redis').get('host')
        self.redis_port = pw_info.get('redis').get('port')
        self.redis_password = pw_info.get('redis').get('password')
        self.redis_db = pw_info.get('redis').get('db')


class PatchWsDealer(PatchWaitDealer):

    def __init__(self, redis_host, redis_port, redis_password, redis_db):
        super().__init__(redis_host, redis_port, redis_password, redis_db)
        self.wpid = None
        self.rpid = None
        self.done_notify_yet = False

    @staticmethod
    def get_instance(ws_info: WsPatchInfo):
        if ws_info is None or ws_info.wpid is None or ws_info.rpid is None \
                or ws_info.redis_db is None or ws_info.redis_host is None \
                or ws_info.redis_password is None:
            raise Exception("ws_info 不合法，没有经过前端框架层校验")
        dealer = PatchWsDealer(ws_info.redis_host, ws_info.redis_port, ws_info.redis_password, ws_info.redis_db)
        dealer.wpid = ws_info.wpid
        dealer.rpid = ws_info.rpid
        return dealer

    def write_to_client(self, msg: str, fail=False):
        """通知长连接client 消息（hcore)
        """
        self.notify(-1 if fail else 0, msg, is_raw=True, forever=True)

    async def receive_from_client(self, callback4client_data, callback4disconnect):
        """长连接从client(hcore)接收消息
        """
        await self.wait4result(callback4client_data, callback4disconnect)

    def get_wpid(self):
        """重写
        """
        return self.wpid

    def get_rpid(self):
        """重写
        """
        return self.rpid
