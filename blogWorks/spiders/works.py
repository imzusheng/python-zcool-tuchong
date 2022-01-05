import re
import time

import pymongo
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 初始化webdriver
# @return webdriver.Chrome(...)
from blogWorks.items import BlogworksItem

def webdriver_init():
    chrome_opt = Options()
    # 不加载图片
    prefs = {'profile.managed_default_content_setting.images': 2}
    chrome_opt.add_experimental_option('prefs', prefs)
    # 无头浏览器配置
    chrome_opt.add_argument('log-level=3')
    chrome_opt.add_argument('--headless')
    chrome_opt.add_argument('--disable-gpu')
    # 无头浏览器配置结束
    # chrome_service = Service('./chromedriver')
    # self.browser = webdriver.Chrome(service=chrome_service)
    browser = webdriver.Chrome(executable_path='chromedriver', chrome_options=chrome_opt)
    return browser


class WorksSpider(scrapy.Spider):
    name = 'works'
    # 主页地址
    start_urls = [
        'https://my.zcool.com.cn/works',
        'https://tuchong.com/14082769'
    ]

    def __init__(self):
        print("@_spider_init")
        self.username = '<站酷账号>'
        self.password = '<站酷密码>'
        self.browser = webdriver_init()
        # mongodb uri
        self.client = pymongo.MongoClient('mongodb://localhost:27017')
        # 数据库名
        db = self.client['blog']
        # 集合名
        self.col = db['works']
        # 先删除已有的旧数据
        self.col.drop()
        # 当前进度
        self.mdIndex = 1
        self.spiderIndex = 1
        super().__init__()

    def parse(self, response):
        # 实例化item
        item = BlogworksItem()
        if self.spiderIndex == 1:
            workList = response.xpath(
                '//div[@id="work-list"]//div[@class="work-list-box"]//div[@class="p-relative left hover-show-edit-group sReadOnly-card-box"]')
            for work in workList:
                infoContainer = work.xpath('div[@class="card-box js-card-box"]/div[@class="card-info"]')
                # 标题
                describeTitle = infoContainer.xpath('p[@class="card-info-title"]/a/text()').extract()
                # 类型
                describeContent = infoContainer.xpath('p[@class="card-info-type"]/text()').extract()
                # 热度、点击量
                hot = infoContainer.xpath('p[@class="card-info-item"]/span[@class="statistics-view"]/text()').extract()
                # 喜欢人数
                like = infoContainer.xpath(
                    'p[@class="card-info-item"]/span[@class="statistics-tuijian"]/text()').extract()
                # 发布时间
                describeDate = \
                    work.xpath('div[@class="card-box js-card-box"]/div[@class="card-item"]/span/text()').extract()
                # 封面
                poster = work.xpath('div[@class="card-box js-card-box"]/div[@class="card-img"]/a/img/@src').extract()
                # 源
                src = work.xpath('div[@class="card-box js-card-box"]/div[@class="card-img"]/a/@href').extract()
                # 存储成dirt
                t = time.time()
                # 时间戳作id
                item['_id'] = str(round(t * 1000000))
                item['describeTitle'] = describeTitle[0]
                item['describeContent'] = describeContent[0]
                item['describeDate'] = describeDate[0]
                item['hot'] = hot[0]
                item['like'] = like[0]
                item['src'] = src[0]
                item['poster'] = poster[0]
                item['category'] = 'CINEMA 4D'
                yield item

        elif self.spiderIndex == 2:
            workList = response.xpath(
                '//div[@class="container"]/div[@class="page-content"]/ul[@class="pagelist-wrapper"]/*')
            for work in workList:
                poster = work.xpath('div')[0].xpath('@data-lazy-url').extract()
                colSum = work.xpath('div[@class="post-info"]/p')[0].xpath('span')[1].xpath('text()').extract()
                like = work.xpath('div[@class="post-info"]/p[@class="post-action"]/span')[1].xpath('text()').extract()
                src = work.xpath('@data-url').extract()
                size = work.xpath('@style')[0].extract()
                height = re.findall(r'height: (.*?)px;', size)[0]
                width = re.findall(r'width: (.*?)px;', size)[0]
                # 存储成dirt
                t = time.time()
                # 时间戳作id
                item['_id'] = str(round(t * 1000000))
                item['category'] = 'Photo'
                item['colSum'] = colSum
                item['poster'] = 'https://' + poster[0]
                item['like'] = like[0].replace('喜欢', '')
                item['src'] = src[0]
                item['height'] = height
                item['width'] = width
                yield item
        elif self.spiderIndex == 3:
            with open('index.html', 'wb') as f:
                f.write(response.body)

        self.spiderIndex += 1

    # 结束
    def close(self, reason):
        self.browser.close()
        print('@Spider__close')
