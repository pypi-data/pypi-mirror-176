# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, http_get, json, urlsplit
from xyz_embedmedia.decorators import register


@register()
class LiZhiFM(Vendor):
    name = '荔枝FM'
    sub_domains = 'lizhi.fm'
    type = 'audio'
    test_urls = [
        'https://m.lizhi.fm/vod/2447358/2671732355811740166',
        'https://www.lizhi.fm/42784551/5075439394125704326?u=5131148477518480172'
    ]

    def explain_default(self, response):
        super(LiZhiFM, self).explain_default(response)
        id = urlsplit(response.url).path.split('/')[-1]
        url = "https://m.lizhi.fm/vodapi/voice/info/%s" % id
        d = http_get(url).json()['data']['userVoice']
        self.data['cover'] = d['voiceInfo']['imageUrl']
        self.data['embed_url'] = d['voicePlayProperty']['trackUrl']
        self.data['name'] = d['voiceInfo']['name']
        self.data['description'] = ''
        self.data['duration'] = d['voiceInfo']['duration']
        self.data['detail'] = d
