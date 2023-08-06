# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, json
from xyz_embedmedia.decorators import register
from xyz_util.datautils import access

@register()
class Ted(Vendor):
    name = 'TED'
    sub_domains = ['ted.com']
    type = 'video'
    test_urls = [
        'https://www.ted.com/talks/steven_johnson_how_humanity_doubled_life_expectancy_in_a_century/up-next'
    ]


    def explain_default(self, response):
        super(Ted, self).explain_default(response)
        s = extract_between(response.text, '"__INITIAL_DATA__":', '})</script>')
        d = json.loads(s)
        d = access(d, 'talks.0')
        vd = access(d, 'player_talks.0')
        self.data['embed_url'] = access(vd, 'resources.hls.stream')
        self.data['cover'] = access(vd, 'thumb')
        self.data['height'] = access(d, 'downloads.videoDownloads.1.height')
        self.data['name'] = vd['title']
        self.data['duration'] = vd['duration']
        self.data['unique_id'] = 'ted_%s' % d['id']
