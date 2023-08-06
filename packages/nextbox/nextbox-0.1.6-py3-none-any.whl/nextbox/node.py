import asyncio
import nats
import abc
from loguru import logger
import time
from nats.aio.msg import Msg
from nats.js import api
from nats.js.kv import KeyValue
from .module.los import los
from .conf import BaseNodeConf


class Node(metaclass=abc.ABCMeta):
    def __init__(self, conf: BaseNodeConf = None, conf_fp: str = None):
        logger.info("---NextBox---")
        if conf is None:
            conf = BaseNodeConf.load(conf_fp)
        self.conf = conf
        self._fps = 0
        self.js = None
        self.kv: KeyValue = None
        self.los = los(**conf.nats.los_conf)

    @property
    def fps(self):
        return self._fps

    @abc.abstractmethod
    async def process(self, msg: Msg = None):
        return

    async def _callback(self, msg: Msg = None):
        # if msg: logger.info(f'Received: {msg}')
        if msg:
            await msg.ack()
        _tic = time.time()
        pmsg = await self.process(msg)
        cost = time.time() - _tic
        self._fps = 1 / cost

        # 发送消息
        if self.conf.nats.pub_conf.subject and pmsg is not None:
            _pmsg = bytes('{}'.format(pmsg), 'utf-8')
            ack = await self.js.publish(
                self.conf.nats.pub_conf.subject,
                payload=_pmsg,
                timeout=self.conf.nats.pub_conf.timeout,
                stream=self.conf.nats.pub_conf.stream,
                headers=self.conf.nats.pub_conf.headers
            )
            logger.debug(f"Pub[{ack}]: {pmsg}")

    async def async_start(self):
        # 建立链接
        nc = await nats.connect(servers=self.conf.nats.conn_conf.servers, **self.conf.nats.conn_conf.options)
        self.js = nc.jetstream(**self.conf.nats.stream_opts)
        logger.debug("connect success!")

        # 构建kv
        self.kv = await self.js.create_key_value(config=self.conf.nats.kv_conf.config, **self.conf.nats.kv_conf.params)

        if self.conf.nats.sub_conf and self.conf.nats.sub_conf.subject:
            logger.debug("sub>>>")
            config = api.ConsumerConfig(**self.conf.nats.sub_conf.config)
            osub = await self.js.subscribe(
                self.conf.nats.sub_conf.subject,
                queue=self.conf.nats.sub_conf.queue,
                durable=self.conf.nats.sub_conf.durable,
                stream=self.conf.nats.sub_conf.stream,
                config=config,
                manual_ack=self.conf.nats.sub_conf.manual_ack,
                ordered_consumer=self.conf.nats.sub_conf.ordered_consumer,
                idle_heartbeat=self.conf.nats.sub_conf.idle_heartbeat,
                flow_control=self.conf.nats.sub_conf.flow_control,
                pending_msgs_limit=self.conf.nats.sub_conf.pending_msgs_limit,
                pending_bytes_limit=self.conf.nats.sub_conf.pending_bytes_limit
            )

            while True:
                try:
                    msg = await osub.next_msg()
                    await self._callback(msg)
                except TimeoutError:
                    break
        else:
            # 没订阅任何主题时
            while True:
                await self._callback()

    def start(self):
        asyncio.run(self.async_start())
