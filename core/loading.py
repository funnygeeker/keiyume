#!/usr/bin/python3
# -*- coding: utf-8 -*-
# keiyume_2.0.0-beta.2
# 溪梦框架信息加载
# 作者：稽术宅（funnygeeker）
# 溪梦框架项目交流QQ群：332568832
# 作者Bilibili：https://b23.tv/b39RG2r
# Github：https://github.com/funnygeeker
import sys
import time

# 生成控制台上符号组成的字母 http://patorjk.com/software/taag/#p=display&h=1&f=Slant&t=Keiyume
# http://patorjk.com/software/taag/#p=display&h=1&f=Ivrit&t=Keiyume


class Loading():
    def Start():
        print(r'''
=======================【正在初始化】=======================

      _  __      _                                
     | |/ / ___ (_) _   _  _   _  _ __ ___    ___ 
     | ' / / _ \| || | | || | | || '_ ` _ \  / _ \
     | . \|  __/| || |_| || |_| || | | | | ||  __/
     |_|\_\\___||_| \__, | \__,_||_| |_| |_| \___|
                    |___/                         

    欢迎使用：溪梦框架 v2.0.0-beta.2 20221123

============================================================
''')

    def Info():
        time.sleep(1)
        print('''  在爱发电中支持一下作者：https://afdian.net/@funnygeeker
  Github地址：https://www.github.com/funnygeeker/keiyume
  Bilibili主页：https://b23.tv/b39RG2r
  溪梦社区：https://keiyume.com

  Python小白练手作品，大佬轻喷！
  框架交流QQ群：332568832

============================================================''')
        time.sleep(2)
        print('''
  【感谢捐助】
  无

  【特别致谢】
  QQ：98252***0（技术指导）

============================================================\n''')
# 进度条，只是为了视觉效果
        for i in range(1, 51):
            print("\r", end="")
            print(f"{i*2}%: ", "▋" * (i // 2), end="")
            sys.stdout.flush()
            time.sleep(0.01)
        print('\n\n============================================================\n')
