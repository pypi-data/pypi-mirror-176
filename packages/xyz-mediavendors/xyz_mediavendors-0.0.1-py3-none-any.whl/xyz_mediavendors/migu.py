# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import http_get, extract_between, json
from xyz_embedmedia.decorators import register


@register()
class MiGu(Vendor):
    name = '咪咕'
    sub_domains = 'migu.cn'
    type = 'audio'
    test_urls = [
        'http://c.migu.cn/005jJX?ifrom=ec2c974cb878f4a7ba4307237a3db3d9'
    ]

    def explain_default(self, response):
        super(MiGu, self).explain_default(response)
        id = extract_between(response.url, 'id=', '&')
        url = 'https://c.musicapp.migu.cn/MIGUM2.0/v1.0/content/resourceinfo.do?resourceId=' + id + '&resourceType=2'
        r = http_get(url)
        d = r.json()['resource'][0]
        self.data['embed_url'] = 'https://h5.nf.migu.cn/app/providers/api/v2/song.listen.ask?id=' + id + '&resourceType=2'
        self.data['cover'] = d['albumImgs'][1]['img']
        self.data['name'] = d['songName']
        self.data['detail'] = d
        self.data['description'] = d.get('songDescs')
        ps =d['length'].split(':')
        self.data['duration'] = int(ps[0])*3600+int(ps[1])*60+int(ps[2])
        # url2 = "https://m.music.migu.cn/migu/remoting/cms_detail_tag?pid=%s" % id
        # r = ScrapyResponse(url2, mobile_mode=True)
        # d = json.loads(r.text)['data']
        # self.data['cover'] = d['picM']
        # self.data['embed_url'] = d['listenUrl']
        # self.data['name'] = d['songName']
        # self.data['description'] = "%s  %s" % (','.join(d['singerName']), d.get('songDesc'))
        # self.data['detail'] = d
