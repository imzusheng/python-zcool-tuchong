import random
import time

from scrapy.http import HtmlResponse


# Selenium中间件
class SeleniumInterceptMiddleware:
    # 注释
    def process_request(self, request, spider):
        dr = spider.browser

        print('打开页面，等待2s...')
        dr.get(request.url)
        time.sleep(2)

        if spider.mdIndex == 1:
            # 找到iframe
            iframes = dr.find_elements_by_tag_name("iframe")

            # 切换到iframe
            dr.switch_to.frame(iframes[0])

            # 切换到账号密码登录
            pwdLoginBtn = dr.find_element_by_xpath(
                '//div[@id="login-box"]//div[@class="l-tab-covers"]//div[text()="密码登录"]')
            pwdLoginBtn.click()

            # 输入账号
            username = dr.find_element_by_css_selector('#username')
            username.click()
            username.send_keys(spider.username)

            # 输入密码
            password = dr.find_element_by_css_selector('#password')
            password.click()
            password.send_keys(spider.password)

            # 登录
            dr.find_element_by_css_selector('#loginbtn').click()

            print('登录成功，等待2s...')
            time.sleep(2)
        elif spider.mdIndex == 2:
            def scrollTop(scrollKey):
                # 脚本跳转到网页中间，不然评论不加载
                dr.execute_script('document.body.scrollTop=' + str(scrollKey * 1000))
                time.sleep(3)
                print('正在加载图片，等待3s...')
                moreStyle = dr.find_element_by_css_selector('.pagelist-load-more').get_attribute("style")
                if moreStyle == 'display: block;':
                    scrollTop(scrollKey + 1)

            # 执行
            scrollTop(1)

        spider.mdIndex += 1

        return HtmlResponse(
            url=request.url,
            body=dr.page_source,
            request=request,
            encoding='utf8'
        )


class BlogworksDownloaderMiddleware:
    # UA池
    USER_AGENT_LIST = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    # 代理ip池 https
    PROXY_LIST = [
        '103.103.3.6:8080',
        '113.237.3.178:9999',
        '118.117.188.171:3256',
        '211.24.95.49:47615',
        '103.205.15.97:8080'
    ]

    # 请求拦截
    def process_request(self, request, spider):
        # UA随机选取
        user_agent_selected = random.choice(self.USER_AGENT_LIST)
        request.headers['User-Agent']: user_agent_selected
        return None

    # 拦截异常
    # def process_exception(self, request):
    #     print('@process_exception')
    #     # 出现异常更换代理
    #     request.meta['proxy'] = 'https://' + random.choice(self.PROXY_LIST)
    #     # 重新发送
    #     return None
