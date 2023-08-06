# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, json
from xyz_embedmedia.decorators import register


@register()
class Sohu(Vendor):
    name = '搜狐视频'
    sub_domains = ['tv.sohu.com', '3g.k.sohu.com']
    type = 'video'
    test_urls = [
        'https://m.tv.sohu.com/svs/sv4289454.shtml?channeled=1211160001&sf_atype=apps&sf_pro=1&resorce_click=1&sf_cv=8.3.3&sf_mtype=6',
        'https://m.tv.sohu.com/v/MjAxNzExMDkvbjYwMDI0NzEwMi5zaHRtbA==.html',
        'https://3g.k.sohu.com/t/m476121257',
        'https://m.tv.sohu.com/sugs/sv60412561.shtml?channeled=1211160001&sf_atype=apps&sf_pro=1&resorce_click=&sf_cv=8.3.6&sf_mtype=6'
    ]

    def explain_default(self, response):
        super(Sohu, self).explain_default(response)
        site = '2' if '3g.k.sohu.com' in response.url or '/sugs/' in response.url else '1'
        vid = extract_between(response.text, 'vid:', ',').replace("'", '').strip()
        self.data['description'] = response.css('meta[name="og:desc"]::attr("content")').get()
        url2 = "https://m.tv.sohu.com/phone_playinfo?callback=jsonpx1598704577496_54_4&vid=" + vid + "&site="+site+"&appid=tv&api_key=f351515304020cad28c92f70f002261c&plat=17&sver=1.0&partner=1&uid=1598704577084719&muid=1598704577085312&_c=1&pt=3&qd=680&src=11050001&ssl=1&_=1598704577496"
        r2 = ScrapyResponse(url2)
        s = r2.text[len('jsonpx1598704577496_54_4('):-1]
        d = json.loads(s)['data']
        mp4 = d['urls']['mp4']
        self.data['cover'] = d.get('hor_w8_pic', self.data['cover'])
        self.data['embed_url'] = (mp4.get('nor') or mp4.get('hig') or mp4.get('sup'))[0]
        self.data['duration'] = d.get('duration')
        self.data['detail'] = d
        self.data['width'] = d.get('vWidth', 414)
        self.data['height'] = d.get('vHeight', 233)
