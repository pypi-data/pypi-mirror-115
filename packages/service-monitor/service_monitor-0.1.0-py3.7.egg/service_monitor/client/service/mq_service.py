#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author: xl
@file: mq_service.py 
@time: 2021/08/09
@contact: 
@site:  
@software: PyCharm 
"""
import json

from kafka import KafkaProducer

from service_monitor.client.conf import CONF
from service_monitor.client.enums import WarnningType


class MQService:
    def __init__(self, conf):
        self._topic = conf.KAFKA_CONFIG.TOPIC
        self._server = conf.KAFKA_CONFIG.KAFKA_SERVER
        producer = KafkaProducer(
            bootstrap_servers=self._server,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        )
        self.producer = producer

    def send_mq(self, project_name, err_msg, trace_id, request, warnning_type: WarnningType = WarnningType.normal):
        msg = {
            'project_name': project_name,
            'trace_id': trace_id,
            'reason': err_msg,
            'request': request,
            'stage': warnning_type.value
        }
        future = self.producer.send(
            topic=self._topic,
            value=msg,
        )
        record_metadata = future.get(timeout=10)
        return record_metadata.topic

    def close(self):
        if self.producer is not None:
            self.producer.close()
            self.producer = None


mq_serveice = MQService(conf=CONF)
