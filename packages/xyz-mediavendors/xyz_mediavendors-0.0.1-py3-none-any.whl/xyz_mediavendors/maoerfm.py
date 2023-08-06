# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, json
from xyz_embedmedia.decorators import register


@register()
class MaoErFM(Vendor):
    name = '猫耳FM'
    sub_domains = 'missevan.com'
    type = 'audio'
    test_urls = [
        'https://m.missevan.com/sound/1165634',
        'https://www.missevan.com/sound/294645'
    ]

    def explain_default(self, response):
        super(MaoErFM, self).explain_default(response)
        id = extract_between(response.url, '/sound/', '?')
        url2 = "https://www.missevan.com/sound/getsound?soundid=%s" % id
        r = ScrapyResponse(url2)
        d = json.loads(r.text)['info']['sound']
        self.data['cover'] = "https://static.missevan.com/coversmini/" + d['cover_image']+"?x-oss-process=style/webp"
        self.data['embed_url'] = d['soundurl']
        self.data['name'] = d['soundstr']
        self.data['description'] = d['intro']
        self.data['detail'] = d
