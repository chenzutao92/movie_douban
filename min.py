from scrapy .cmdline import execute

import os
import sys


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "xici_proxy"])
# execute(["scrapy", "crawl", "movies"])
# execute(["scrapy", "crawl", "lagou"])

# 需要把当前项目目录放到sys.path下，scrapy命令必须在工程目录下运行
# __file__:当前文件（main.py文件）
# os.path.abspath(__file__): 获取main.py的绝对路径
# os.path.dirname(os.path.abspath(__file__)):获取mian.py目录
# scrapy启动命令：scrapy crawl jobbole
