# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, json
from xyz_embedmedia.decorators import register


@register()
class VUE(Vendor):
    name = 'VUE'
    sub_domains = ['v.vuevideo.net']
    type = 'video'
    test_urls = [
        'https://v.vuevideo.net/share/post/-2849956594155498392'
    ]

    def explain_default(self, response):
        super(VUE, self).explain_default(response)
        self.data['embed_url'] = response.css('video::attr(src)').get()
        self.data['width'] = 414
        self.data['height'] = 233
