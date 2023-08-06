#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author: xl
@file: conf.py 
@time: 2021/08/09
@contact: 
@site:  
@software: PyCharm 
"""
import os

import attrdict
from loguru import logger

MQ_SERVER = os.environ.get('MQ_SERVER', '')
TOPIC = os.environ.get('TOPIC', '')
FEI_SHU = os.environ.get('FEI_SHU', '')

KAFKA_CONFIG = attrdict.AttrDict({
    'TOPIC': TOPIC,
    'KAFKA_SERVER': MQ_SERVER
})

CONF = attrdict.AttrDict({
    "KAFKA_CONFIG": KAFKA_CONFIG,
    "FEI_SHU": FEI_SHU
})

logger.info(CONF)
