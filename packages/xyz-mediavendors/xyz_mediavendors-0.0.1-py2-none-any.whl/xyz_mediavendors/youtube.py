# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, json
from xyz_embedmedia.decorators import register
from xyz_util.datautils import access

@register()
class Youtube(Vendor):
    name = 'youtube'
    sub_domains = ['youtube.com']
    type = 'video'
    test_urls = [
        'https://m.youtube.com/watch?v=y6j49Ew13qM'
    ]


    def request_extra_params(self, f):
        d = super(Youtube, self).request_extra_params(f)
        d['proxy'] = False
        return d


    def explain_default(self, response):
        s = '{"' + extract_between(response.text, 'var ytInitialPlayerResponse = {"', ';</script>')
        d = json.loads(s)
        rd = self.data
        vf = access(d, 'streamingData.formats.-1')
        rd['embed_url'] = vf['url']
        rd['width'] = vf['width']
        rd['height'] = vf['height']
        vd = d['videoDetails']
        rd['name'] = vd['title']
        rd['cover'] = access(vd, 'thumbnail.thumbnails.-1.url')
        rd['duration'] = int(vd['lengthSeconds'])
        rd['description'] = vd['shortDescription']
        rd['detail'] = vd
        rd['unique_id'] = vd['videoId']



@register()
class YCombinator(Youtube):
    name = 'YCombinator'
    sub_domains = ['ycombinator.com']
    test_urls = [
        'https://blog.ycombinator.com/ycs-fall-tour-2021/'
    ]

    def explain_default(self, response):
        url = response.css('iframe::attr(src)').get()
        id = extract_between(url, '/embed/', '?')
        url = 'https://m.youtube.com/watch?v=%s' % id
        response = self.get_response(url)
        super(YCombinator, self).explain_default(response)



@register()
class ThisWeekInStartups(YCombinator):
    name = 'ThisWeekInStartups'
    sub_domains = ['thisweekinstartups.com']
    test_urls = [
        'https://thisweekinstartups.com/how-to-understand-customer-engagement-customer-basics-with-salesforces-tiffani-bova-e1301/'
    ]
