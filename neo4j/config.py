#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#配置文件
import os
SECRET_KEY=os.urandom(24)        #生成密钥
CSRF_ENABLED=True                #开启CSRF保护