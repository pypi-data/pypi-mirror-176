# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, json
from xyz_embedmedia.decorators import register
import requests

@register()
class FanDengDuShu(Vendor):
    name = '樊登读书'
    sub_domains = ['card.dushu.io']
    type = 'video'
    test_urls = [
        'https://card.dushu.io/sharePage/find.html?id=xu4b9f2447kjij4t&r=zwl3r703lhdih79y&py=1&secondSource=10'
    ]


    def explain_default(self, response):
        super(FanDengDuShu, self).explain_default(response)
        id = extract_between(response.url, 'id=', '&')
        r = requests.post('https://gateway-api.dushu.io//info-system/infoDetail/v100/infoDetailShare',dict(infoId=id, userId='zwl3r703lhdih79y'))
        d = r.json()['data']
        self.data['name'] = d['infoTitle']
        self.data['cover'] = d['shareImgUrl']
        self.data['embed_url'] = d['infoVideoMediaUrl']
        self.data['detail'] = d
        self.data['duration'] =d.get('infoMediaLength')
