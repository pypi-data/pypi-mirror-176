# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, json, http_get, urlsplit, UA_PC, html2text
from xyz_embedmedia.decorators import register
from six import string_types

from xyz_util.datautils import str2dict, access


@register()
class XiaoHongShu(Vendor):
    name = '小红书'
    sub_domains = ['www.xiaohongshu.com', 'xhslink.com']
    type = 'video'
    test_urls = [
        'https://www.xiaohongshu.com/discovery/item/61039ee8000000002103897f',
        'http://xhslink.com/ZZUhZd'
    ]

    def request_extra_params(self, f):
        d = super(XiaoHongShu, self).request_extra_params(f)
        cs = 'xhsTrackerId=7a34eadc-cdc2-41a1-c1dc-3f4a7c9c978b; smidV2=20200912182440d819e2f83f2b3413d10fe113927952ba00dea81edfaf66d60; xhsuid=JcxbrVgZiTVkUA52; xhs_spid.5dde=013ac757947c13e7.1599901888.5.1599929895.1599927555.450df93f-7535-4440-b8b1-d93d9596d5c1; xhsTracker=url=noteDetail&xhsshare=WeixinSession; extra_exp_ids=gif_exp1,ques_exp1; timestamp2=20210902020ec76d07c1eb70325a6168; timestamp2.sig=1gcuzqJKF3yzE-LGqQrF792PagK2g1O05vD7t1t3VuM'
        d['cookies'] = str2dict(cs, key_spliter='=', line_spliter='; ')
        return d

    def explain_default(self, response):
        super(XiaoHongShu, self).explain_default(response)
        t = extract_between(response.text, 'window.__INITIAL_SSR_STATE__=', '</script>')
        d = json.loads(t.replace('undefined', 'null'))
        d = access(d, 'NoteView.content')
        v = d['video']
        self.data['embed_url'] = v['url']
        self.data['width'] = v['width']
        self.data['height'] = v['height']
        self.data['duration'] = v['duration']
        self.data['cover'] = access(d, 'cover.url')
        self.data['unique_id'] = v['id']
        self.data['data'] = d
