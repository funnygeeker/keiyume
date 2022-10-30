import sys
import time

# 生成控制台上符号组成的字母 http://patorjk.com/software/taag/#p=display&h=1&f=Slant&t=XiMeng


class Loading():
    def Xi_Meng():
        print('''
========================【正在初始化】========================

         _  __  _  __  ___                   
        | |/ / (_)/  |/  /___   ____   ____ _
        |   / / // /|_/ // _ \ / __ \ / __ `/
       /   | / // /  / //  __// / / // /_/ / 
      /_/|_|/_//_/  /_/ \___//_/ /_/ \__, /  
                                    /____/   

    欢迎使用：溪梦框架-V2.0.0_BETA1:20221030

============================================================
''')

    def Info():
        time.sleep(0.5)
        print('''  在爱发电中支持一下作者：https://afdian.net/@funnygeeker
  Github地址：https://www.github.com/funnygeeker/qgma
  Bilibili主页：https://b23.tv/b39RG2r
  极客街官网：https://geekjie.com

  Python入门练手作品，不喜勿喷！
  框架交流QQ群：332568832
  系统交流QQ群：759090242

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
