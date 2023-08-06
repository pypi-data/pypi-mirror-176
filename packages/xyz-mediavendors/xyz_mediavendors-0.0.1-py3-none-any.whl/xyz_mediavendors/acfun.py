# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, json
from xyz_embedmedia.decorators import register


@register()
class ACFun(Vendor):
    name = 'A站'
    sub_domains = ['acfun.cn']
    type = 'video'
    test_urls = [
        'https://m.acfun.cn/v/?ac=15854576&sid=1a11bb9201b030ef'
    ]

    def explain_default(self, response):
        super(ACFun, self).explain_default(response)
        d = json.loads(extract_between(response.text, 'var videoInfo = ', ';\n'))
        p = json.loads(extract_between(response.text, 'var playInfo = ', ';\n'))
        self.data['cover'] = d['cover']
        self.data['name'] = d['title']
        self.data['like_count'] = int(d.get('shareCountShow', 0))
        self.data['description'] = d['des']
        stm = p['streams'][0]
        self.data['embed_url'] = stm['playUrls'][0]
        self.data['width'] = stm['width']
        self.data['height'] = stm['height']
        self.data['duration'] = int(p['durationMillis'] / 1000)
        self.data['detail'] = p
