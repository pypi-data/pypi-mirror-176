# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, json
from xyz_embedmedia.decorators import register

@register()
class Youku(Vendor):
    name = '优酷视频'
    sub_domains = ['youku.com']
    type = 'video'
    test_urls = [
        'https://v.youku.com/v_show/id_XNDY4MDQwMjY0MA==.html?x&sharefrom=android&sharekey=82e4be7b8ffa844372309d11e50b7b096',
        'https://v.youku.com/v_show/id_XNDAwNDUxMzUyOA==.html?sharefrom=iphone&sharekey=c3572866a3aeff6dbb4b1beb1f0ed1429',
        'http://m.youku.com/v_show/id_XMzM1ODE5MzQ2NA==.html?pgcpgcid=UNDY1NzU5NjM2MA=='
    ]
    image_resize = '?x-oss-process=image/resize,m_fill,w_480,h_480/quality,q_100'


    def explain_default(self, response):
        url = response.url
        if '/v_show/id_' in url:
            vid = extract_between(url, '/id_', '.html')
            url = "https://m.youku.com/video/id_%s.html" % vid
        response = ScrapyResponse(url)
        super(Youku, self).explain_default(response)
        s = extract_between(response.text, '<script>window.__INITIAL_DATA__ =', ';window.__PLATOCONFIG__')
        d = json.loads(s)['videoMap']
        self.data['name'] = d['pageTitle']
        self.data['cover'] = d['videoImg']
        self.data['description'] = d['showName']
        vid = d['videoId']
        url2 = "https://ups.youku.com/ups/get.json?vid=" + vid + "&ccode=0501&client_ip=0.0.0.0&app_ver=1.0.0&client_ts=1598426860&fu=0&vr=0&rst=mp4&dq=mp4&os=ios&bt=phone&bd=&tict=0&d=0&needbf=1&site=1&aw=w&vs=1.0&pver=1&wintype=xplayer_m3u8&play_ability=1024&utid=OfDMFwoNkDUCAXFo1%2FV3SYhO&ckey=134%23ba6IWgXwXGfa5xbOZJh0eX0D3QROwKOlAOzBtZ26EXkEXX%2B%2B4YHOn8ORZbV6IGnFujt%2BiX7YDahsFjOd8ToirxtGgGDeZsLUj6owqqX3Ikud%2B4qAqqqqZjXxzsefqc77oXowqTVF94PU%2BXd8hQMKhF1IXJyXLR%2F5Utf359Lv02SUW6x4a8huyZ6lVP7kdiw6zw3F7JY2SPSziBGFqCfTQXbKZKwo8o0EXW9tn8Tv1QuG2LomjCqEckM%2FnEA4rEhCYsPCxui28CXaKsmo1U%2FbW72RSds%2B1QOnYcWSBGsy9Qdj1lAN6E1TuieNAd785zx6iFUKxI43BiT3CyfjBxlrJ0XZ5%2FNo1Zb2cLkTrKYKLpK3R2ce3Qay99MGG1G%2Bo7fXKMVe9LPlQWKtWIHmLtYm7QrnuI29u6GRvBYXXT%2F5UANPhQabpfREBa8lZaxb3XNbB3Nk7rzHTkTo%2BN8IZAojYigqRqvjVsprMfmZMws2LzxvLVbJoWJRCeTIvlaNGwgm1UnSjbP2LBj682fBpfswpK0adonKD0YINxgbfJ0HKjnaTnNgtK28n1oYI%2BsngX5Cr4mbBEhuGAE9sL9e1WyXqPwODnq%2F0O4TKfQvxEpFrOBITTaI0lAVT8L9%2FhW3meEreKUyWW1%2FPB8DItJwCbGcIk6CA8bC7zGt%2Fxwbfgguc5l4RJov%2Fzbuw8hxoExfWYqahBm3yaCPUODXMYjI9FLKO5JYveE3qnzmxdCZhKVcK6m%2BV49qeiK3ph8x4kXscX%3D%3D&callback=json84268607100755295"
        r2 = ScrapyResponse(url2, referer=url)
        s = r2.text[len('json84268607100755295('):-1]
        d2 = json.loads(s)
        self.data['embed_url'] = d2['data']['stream'][0]['m3u8_url']
        self.data['detail'] = d
        self.data['duration'] =d.get('duration')
        self.data['width'] = 414
        self.data['height'] = 233
