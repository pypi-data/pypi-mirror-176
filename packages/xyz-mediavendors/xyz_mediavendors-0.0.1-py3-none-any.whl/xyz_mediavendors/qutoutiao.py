# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, json, http_get
from xyz_embedmedia.decorators import register


@register()
class QuTouTiao(Vendor):
    name = '趣头条'
    sub_domains = ['new.3qtt.cn']
    type = 'video'
    test_urls = [
        'http://new.3qtt.cn/1nSJK9'
    ]
    icon = 'http://m.qutoutiao.net/favicon.ico'

    def explain_default(self, response):
        super(QuTouTiao, self).explain_default(response)
        cid = extract_between(response.url, 'content_id=', '&')
        n = int(cid)
        import math
        url = 'http://html2.qktoutiao.com/detail/jsonp/%d/%d/%d/%d.js' % (
        math.ceil(n / 1000.), math.ceil(n / 100.), math.ceil(n / 10.), n)
        d = json.loads(http_get(url).text[3:-1])
        self.data['name'] = d['title']
        fd = json.loads(d['detail'].replace('\\"', '"'))
        vd = fd['address'][0]
        self.data['duration'] = int(vd['duration'])
        self.data['embed_url'] = 'http://v4.qutoutiao.net/' + vd['url'].replace('\\/', '/')
        self.data['description'] = ''
        url = 'http://mpapi.qutoutiao.net/video/getAddressByFileId?file_id='+vd['file_id']
        self.data['cover'] = http_get(url).json()['data']['cover_image']['Url']
        self.data['width'] = 414
        self.data['height'] = 233
