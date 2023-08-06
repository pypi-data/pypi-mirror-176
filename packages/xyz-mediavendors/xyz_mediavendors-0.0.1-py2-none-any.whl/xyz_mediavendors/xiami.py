# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, json
from xyz_embedmedia.decorators import register

@register()
class MiaMi(Vendor):
    name = '虾米'
    sub_domains = 'xiami.com'
    type = 'audio'
    test_urls = [
        'https://www.xiami.com/song/1805541658'
    ]

    def explain_default(self, response):
        super(MiaMi, self).explain_default(response)
        id = extract_between(response.url, '/song/', '/')
        url = "https://www.xiami.com/webapp/embed-player?autoPlay=1&id=%s" % id
        r = ScrapyResponse(url)
        self.data['embed_url'] = r.css('audio::attr(src)').get()
        self.data['cover'] = r.css('.cover img::attr(src)').get()
        ps = r.css('.songLength::text').get().split(':')
        self.data['duration'] = int(ps[0])*60+int(ps[1])
        self.data['name'] = r.css('p.main a::text').get()

