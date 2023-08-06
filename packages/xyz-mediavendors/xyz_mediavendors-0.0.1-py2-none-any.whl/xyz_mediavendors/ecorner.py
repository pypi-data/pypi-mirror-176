# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals, print_function
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, http_post
from xyz_embedmedia.decorators import register
import json
from xyz_util.datautils import access


@register()
class ECorner(Vendor):
    name = 'ECorner'
    sub_domains = ['ecorner.stanford.edu']
    type = 'audio'
    test_urls = [
        'https://ecorner.stanford.edu/podcasts/justin-kan-twitch-finding-fulfillment-in-entrepreneurship/'
    ]

    def explain_default(self, response):
        super(ECorner, self).explain_default(response)
        url = response.css('.article-body>iframe::attr(src)').get()
        r = ScrapyResponse(url)
        s = extract_between(r.text, '{"content":', '}\n')
        d = json.loads(s)
        self.data['description'] = d['episode_description_plain']
        self.data['duration'] = int(d['duration'])
        self.data['embed_url'] = access(d, 'media.mp3.url')
        self.data['name'] = d['episode_title']
        self.data['unique_id'] = d['episode_id']
        self.data['cover'] = d['cover_image']
        self.data['data'] = d
