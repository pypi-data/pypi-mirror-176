# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, http_post
from xyz_embedmedia.decorators import register


@register()
class SimpleCast(Vendor):
    name = 'SimpleCast'
    sub_domains = ['simplecast.com']
    type = 'audio'
    test_urls = [
        'https://equity.simplecast.com/episodes/finding-fraud-in-a-world-of-fast-moving-deals'
    ]

    def explain_default(self, response):
        super(SimpleCast, self).explain_default(response)
        if 'simplecast.com' in response.url:
            r = http_post('https://api.simplecast.com/episodes/search', data=dict(url=response.url))
            d = r.json()
            self.data['description'] = d['description']
            self.data['icon'] = 'https://image.simplecastcdn.com/assets/simplecast-logo-32.png'
        else:
            url = extract_between(response.text, '<iframe src="', '"')
            id = extract_between(url, 'player.simplecast.com/', '?')
            url = 'https://api.simplecast.com/episodes/%s/player' % id
            r = ScrapyResponse(url)
            d = r.json()
        self.data['duration'] = d['duration']
        self.data['embed_url'] = d['enclosure_url']
        self.data['name'] = d['title']
        self.data['unique_id'] = d['id']
        self.data['detail'] = d


@register()
class TechCrunch(SimpleCast):
    name = 'TechCrunch'
    sub_domains = ['techcrunch.com']
    test_urls = [
        'https://techcrunch.com/2021/10/08/community-is-the-new-ai/'
    ]

@register()
class A16Z(SimpleCast):
    name = 'A16Z'
    sub_domains = ['a16z.com']
    test_urls = [
        'https://future.a16z.com/podcasts/moderna-covid-vaccine-mrna-technology/'
    ]
