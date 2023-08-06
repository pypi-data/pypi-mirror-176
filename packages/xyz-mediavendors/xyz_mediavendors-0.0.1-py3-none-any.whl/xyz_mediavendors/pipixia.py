# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, http_get
from xyz_embedmedia.decorators import register


@register()
class PiPiXia(Vendor):
    name = '皮皮虾'
    sub_domains = ['h5.pipix.com']
    type = 'video'
    test_urls = [
        'https://h5.pipix.com/item/6802106452602263815',
    ]

    def explain_default(self, response):
        super(PiPiXia, self).explain_default(response)
        id=extract_between(response.url,'/item/', '?')
        url='https://h5.pipix.com/bds/webapi/item/detail/?item_id='+id
        d=http_get(url).json()['data']['item']
        self.data['cover'] = d['share']['large_image_url']
        self.data['name'] = d['share']['title']
        self.data['description'] = ''
        v = d['video']['video_download']
        self.data['detail'] = v
        self.data['embed_url'] = v['url_list'][0]['url']
        self.data['duration'] = v['duration']
        self.data['width'] = v['width']
        self.data['height'] = v['height']
