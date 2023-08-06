# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, json, http_get, urlsplit
from xyz_embedmedia.decorators import register

@register()
class LanRenTingShu(Vendor):
    name = '懒人听书'
    sub_domains = ['m.lrts.me']
    type = 'audio'
    test_urls = [
        'https://m.lrts.me/player?entityType=2&id=408205&sonId=4283468',
        'https://m.lrts.me/player?entityType=2&id=408207&sonId=4283468',
    ]

    def explain_default(self, response):
        super(LanRenTingShu, self).explain_default(response)
        bg=response.css('.player-bg-mask::attr(style)').get()
        self.data['cover']=extract_between(bg, 'url(', ');')
        id = extract_between(response.url, '&id=', '&')
        url = "https://m.lrts.me/ajax/getPlayPath?entityId="+id+"&entityType=2&opType=1&sections=[108]&type=0"
        d = http_get(url).json()
        self.data['embed_url'] = d['list'][0]['path']
        #     self.data['cover'] = d['weixinPic']
        #     self.data['detail'] = d
        # else:
        #     id = ps[-1]
        #     url = "https://m.ximalaya.com/m-revision/common/album/queryAlbumTrackRecordsByPage?albumId="+id+"&page=1&pageSize=10&asc=true&countKeys=play%2Ccomment&v=1599041558260"
        #     r = ScrapyResponse(url)
        #     d = json.loads(r.text)['data']['trackDetailInfos'][0]['trackInfo']
        #     self.data['cover'] = 'http://imagev2.xmcdn.com/' + d['cover']
        #     self.data['embed_url'] = d['playPath']
        #     # self.data['name'] = d['title']
        #     self.data['description'] = ''
        #     self.data['detail'] = d

