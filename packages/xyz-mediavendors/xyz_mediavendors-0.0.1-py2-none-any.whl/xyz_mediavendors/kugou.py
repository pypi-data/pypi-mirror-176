# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between
from xyz_embedmedia.decorators import register
import json

@register()
class KuGou(Vendor):
    name = '酷狗音乐'
    sub_domains = ['kugou.com']
    type = 'audio'
    test_urls = [
        'https://t3.kugou.com/song.html?id=8MuIe04woV2'
    ]

    def explain_default(self, response):
        super(KuGou, self).explain_default(response)
        s = extract_between(response.text, 'var phpParam = ', '};')+'}'
        d = json.loads(s)['song_info']['data']
        self.data['embed_url'] = d['url']
        self.data['duration'] = d['timeLength']
        self.data['name'] = d['fileName']
        self.data['cover'] = d['album_img'].replace('{size}', '400')