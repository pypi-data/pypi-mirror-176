# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, json, http_get, urlsplit
from xyz_embedmedia.decorators import register
import re

@register()
class XiMaLaYa(Vendor):
    name = '喜马拉雅'
    sub_domains = ['xima.tv', 'ximalaya.com']
    type = 'audio'
    test_urls = [
        'https://m.ximalaya.com/ertong/20855650/154994844',
        'https://m.ximalaya.com/ertong/40557644/',
        'http://xima.tv/ss2YVM?_sonic=0'
    ]

    def explain_default(self, response):
        super(XiMaLaYa, self).explain_default(response)
        # s = extract_between(response.text, 'window.__INITIAL_STATE__ = ', ';</script>')
        # d = json.loads(s)
        ps = urlsplit(response.url).path.split('/')
        RE = re.compile(r'^\d+$')
        ps = [p for p in ps if RE.match(p)]
        if 'sound' in response.url or len(ps) == 2:
            id = ps[-1]
            url = 'https://m.ximalaya.com/mobile/v1/track/share/content?trackId='+id+'&tpName=weixin&device=h5'
            d = http_get(url).json()
            self.data['embed_url'] = d['audioUrl']
            self.data['cover'] = d['weixinPic']
            self.data['detail'] = d
        else:
            id = ps[-1]
            url = "https://m.ximalaya.com/m-revision/common/album/queryAlbumTrackRecordsByPage?albumId="+id+"&page=1&pageSize=10&asc=true&countKeys=play%2Ccomment&v=1599041558260"
            r = ScrapyResponse(url)
            d = json.loads(r.text)['data']['trackDetailInfos'][0]['trackInfo']
            self.data['cover'] = 'http://imagev2.xmcdn.com/' + d['cover']
            self.data['embed_url'] = d['playPath']
            # self.data['name'] = d['title']
            self.data['description'] = ''
            self.data['detail'] = d

