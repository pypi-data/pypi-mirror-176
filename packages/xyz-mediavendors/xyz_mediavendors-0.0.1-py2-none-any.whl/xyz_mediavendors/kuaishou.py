# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, json
from xyz_embedmedia.decorators import register


@register()
class KuaiShou(Vendor):
    name = '快手'
    sub_domains = ['kuaishou.com']
    type = 'video'
    test_urls = [
        'https://v.kuaishou.com/6hylHB'
    ]

    def request_extra_params(self, f):
        hs = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive"
        }
        return dict(extra_headers=hs)

    def explain_default(self, response):
        super(KuaiShou, self).explain_default(response)
        s = extract_between(response.text, 'window.pageData= ', '</script>')
        d = json.loads(s)
        self.data['duration'] = int(d['rawPhoto']['ext_params']['video'] / 1000)
        d = d['video']
        self.data['name'] = d['caption']
        self.data['cover'] = d['shareCover']
        self.data['embed_url'] = d['srcNoMark']
        self.data['description'] = ''
        self.data['detail'] = d
        lc = d.get('likeCount', '0')
        if lc.endswith('w'):
            lc = int(float(lc[:-1])*10000)
        else:
            lc = int(lc)
        self.data['like_count'] = lc
        self.data['width'] = d['width']
        self.data['height'] = d['height']


@register()
class KuaiShouApp(Vendor):
    name = '快手极速版'
    sub_domains = ['v.kuaishouapp.com']
    type = 'video'
    test_urls = [
        'https://v.kuaishouapp.com/s/ZhyaLdxg'
    ]

    def request_extra_params(self, f):
        return dict(mobile_mode=False)

    def explain_default(self, response):
        super(KuaiShouApp, self).explain_default(response)
        s = extract_between(response.text, 'window.__APOLLO_STATE__=', ';(')
        d = json.loads(s)
        pid = extract_between(s, '\\"photoId\\":\\"', '\\"')
        d = d['clients']['graphqlServerClient']['VideoFeed:%s' % pid]
        self.data['name'] = d['caption']
        self.data['cover'] = d['thumbnailUrl']
        self.data['embed_url'] = d['playUrl']
        self.data['description'] = ''
        self.data['detail'] = d
