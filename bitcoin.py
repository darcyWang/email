#https://price.btcfans.com/
import requests
import os
from lxml import etree
from jinja2 import Environment, PackageLoader
max=10000;min=4000
#获取环境变量中的MAX，MIN值
# if 'MAX' in os.environ:
#     max=float(os.getenv('MAX')) 
# if 'MIN' in os.environ:
#     min=float(os.getenv('MIN'))
sendemail=False;strategy="继续持有"
#获取https://price.btcfans.com/上显示的比特币价格
url='https://price.btcfans.com/'
html = etree.HTML(requests.get(url).text)
price = float(html.xpath('//div/text()')[83].replace(',','').strip()[1:])
#根据当前价格选择策略，以及是否发送邮件
if (price>max):
    sendemail=True
    strategy="卖出"
if (price<min):
    sendemail=True
    strategy="买入"
#使用jinja2渲染HTML用于发送邮件
env = Environment(loader=PackageLoader('bitcoin', ''))
template = env.get_template('template.html')
template.stream(price=price,max=max,min=min,strategy=strategy).dump('email.html')
#放弃使用Python脚本发送邮件的方案，选dawidd6/action-send-mail
print("::set-env name=sendemail::{}".format(sendemail))