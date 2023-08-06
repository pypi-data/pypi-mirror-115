#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author: xl
@file: enums.py 
@time: 2021/08/09
@contact: 
@site:  
@software: PyCharm 
"""
import enum


@enum.unique
class WarnningType:
    urgent = "urgent"  # 紧急
    secondary = "secondary"  # 次要
    prompt = "prompt"  # 提示
    normal = "normal"
