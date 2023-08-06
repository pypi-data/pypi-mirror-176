# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import urlsplit, http_get
from xyz_embedmedia.decorators import register


@register()
class TieBa(Vendor):
    name = '贴吧'
    sub_domains = ['tieba.baidu.com']
    type = 'video'
    test_urls = [
        'https://tieba.baidu.com/p/7152451641#/'
    ]

    def explain_default(self, response):
        super(TieBa, self).explain_default(response)
        id = urlsplit(response.url).path.split('/')[-1]
        url = 'https://tieba.baidu.com/mo/q/pb/page/m?kz='+id+'&fr=newshare&r=2&m=11'
        d = http_get(url).json()['data']
        vd = d['video_info']
        if not vd:
            return
        self.data['cover'] = vd['thumbnail_url']
        self.data['embed_url'] = vd['video_url']
        self.data['name'] = response.css('title::text').get()
        self.data['description'] = d['meta']['description']
        self.data['detail'] = vd
        self.data['duration'] =vd['video_duration']
        self.data['width'] = vd['video_width']
        self.data['height'] = vd['video_height']
