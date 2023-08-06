# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import http_get, extract_between, json
from xyz_embedmedia.decorators import register


@register()
class MiaoPai(Vendor):
    name = '秒拍'
    sub_domains = ['miaopai.com']
    type = 'video'
    test_urls = [
        'http://n.miaopai.com/media/vHGgUe5ReOoOp3yTtiYCGKjwJ1MxYDxY.htm'
    ]

    def explain_default(self, response):
        super(MiaoPai, self).explain_default(response)
        id = extract_between(response.url, '/media/', '.htm')
        url='http://n.miaopai.com/api/aj_media/info.json?smid='+id+'&appid=530&_cb=_jsonp2bjz1a0ih2y'
        s = http_get(url, referer=response.url).text
        d = json.loads(s[len('window._jsonp2bjz1a0ih2y && _jsonp2bjz1a0ih2y(') : -2])['data']
        pics = d['meta_data'][0]['pics']
        self.data['cover'] = pics['l'] or pics['interlace']
        self.data['name'] = d['description']
        self.data['embed_url'] = d['meta_data'][0]['play_urls']['l']
        self.data['description'] = ''
        self.data['detail'] = d
        ud = d['meta_data'][0]['upload']
        self.data['duration'] = ud['length']
        self.data['width'] = ud['width']
        self.data['height'] = ud['height']
