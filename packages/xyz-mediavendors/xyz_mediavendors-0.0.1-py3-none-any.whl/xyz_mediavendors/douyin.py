# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals

from six import text_type

from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, json, http_get
from xyz_embedmedia.decorators import register
import time
import js2py

TT_ENC_JS = """function enc(o) {
  var n = function() {
     for (var e = 0, t = new Array(256), n = 0; 256 !== n; ++n)
         e = 1 & (e = 1 & (e = 1 & (e = 1 & (e = 1 & (e = 1 & (e = 1 & (e = 1 & (e = n) ? -306674912 ^ e >>> 1 : e >>> 1) ? -306674912 ^ e >>> 1 : e >>> 1) ? -306674912 ^ e >>> 1 : e >>> 1) ? -306674912 ^ e >>> 1 : e >>> 1) ? -306674912 ^ e >>> 1 : e >>> 1) ? -306674912 ^ e >>> 1 : e >>> 1) ? -306674912 ^ e >>> 1 : e >>> 1) ? -306674912 ^ e >>> 1 : e >>> 1,
         t[n] = e;
     return "undefined" != typeof Int32Array ? new Int32Array(t) : t
  }();
  return function(e) {
                    for (var t, r, i = -1, o = 0, a = e.length; o < a; )
                        (t = e.charCodeAt(o++)) < 128 ? i = i >>> 8 ^ n[255 & (i ^ t)] : t < 2048 ? i = (i = i >>> 8 ^ n[255 & (i ^ (192 | t >> 6 & 31))]) >>> 8 ^ n[255 & (i ^ (128 | 63 & t))] : t >= 55296 && t < 57344 ? (t = 64 + (1023 & t),
                        r = 1023 & e.charCodeAt(o++),
                        i = (i = (i = (i = i >>> 8 ^ n[255 & (i ^ (240 | t >> 8 & 7))]) >>> 8 ^ n[255 & (i ^ (128 | t >> 2 & 63))]) >>> 8 ^ n[255 & (i ^ (128 | r >> 6 & 15 | (3 & t) << 4))]) >>> 8 ^ n[255 & (i ^ (128 | 63 & r))]) : i = (i = (i = i >>> 8 ^ n[255 & (i ^ (224 | t >> 12 & 15))]) >>> 8 ^ n[255 & (i ^ (128 | t >> 6 & 63))]) >>> 8 ^ n[255 & (i ^ (128 | 63 & t))];
                    return -1 ^ i
                }(o) >>> 0;
}"""

XIGUA_EXTRA_COOKIES = dict(
    __ac_nonce='05f96ed3600b14b833e0c',
    __ac_signature='_02B4Z6wo00f01n75M6wAAIBBDTDaVSvvZPp-.DcAAMA073',
    ttwid='1%7C8kLFvORXQQjD8gE5caEDFhLxFjeC3woo12hxxPktDKA%7C1605530741%7C21546b934b32fe6bbda0727f604df7b1b30accee7f2386f520f47f6c43f98b69'
)


def get_toutiao_video(id, proxy=False):
    # url2 = "https://m.toutiaoimg.cn/" + vid + "/info/v2/?_signature=_02B4Z6wo00f01-dkxLQAAIBAlK0tTi-gtbvnccAAAKadNKZT7qz-S5ZncLHBwM3cIL1KkV6WfGCYKH.Tv8x6ypLVbwo1FymlRECfvh-1In2-G0RPLDN6JF1MxA8pmTsVumGhNPtb94RjOLzQba"
    url2 = 'https://m.365yg.com/%s/info/' % id
    d = http_get(url2, proxy=proxy).json()
    if not d['success']:
        return dict(source_vanish=True)
    d = d['data']
    name = d['title']
    cover = d['poster_url']
    vid = d['video_id']
    encryFunc = js2py.eval_js(TT_ENC_JS)
    path = "/video/urls/v/1/toutiao/mp4/" + vid + "?r=9482966687548722"
    sp = encryFunc(path)
    url3 = "https://ib.365yg.com" + path + "&s=" + text_type(sp) + "&aid=1217&nobase64=true&vfrom=xgplayer&_=" + \
           d['publish_time'] + "&callback=axiosJsonpCallback1"
    r3 = http_get(url3, proxy=proxy)
    d3 = json.loads(r3.text[len('axiosJsonpCallback1('): -1])
    vd = d3['data']['video_list']['video_1']
    embed_url = vd['main_url']
    height = vd['vheight']
    width = vd['vwidth']
    duration = d3['data']['video_duration']
    return dict(embed_url=embed_url,
                embed_url_hd='https://api.huoshan.com/hotsoon/item/video/_source/?video_id=' + vid + '&line=0&app_id=0&vquality=normal&watermark=0&sf=5&item_id=' + id,
                name=name,
                cover=cover,
                duration=duration,
                width=width,
                height=height,
                unique_id=d['video_id'],
                publish_time=int(d['publish_time']) * 1000,
                detail=d,
                play_count=d.get('video_play_count'),
                like_count=d.get('digg_count')
                )


@register()
class DouYin(Vendor):
    name = '抖音'
    sub_domains = 'douyin.com'
    type = 'video'
    icon = 'https://www.iesdouyin.com/favicon.ico'
    test_urls = [
        'https://v.douyin.com/JhRxvGR/',
    ]

    def set_video_meta(self, d, a):
        video = a['video']
        d['embed_url'] = video['play_addr']['url_list'][0].replace('/playwm/', '/play/')
        d['cover'] = video['cover']['url_list'][0]
        d['duration'] = int(video['duration'] / 1000)
        d['width'] = video['width']
        d['height'] = video['height']
        d['name'] = a['desc']
        d['detail'] = a
        d['unique_id'] = video['vid']
        d['like_count'] = a.get('statistics', {}).get('digg_count', 0)
        d['publish_time'] = a['create_time'] * 1000

    def get_aweme_list(self, base_url, page_count=10):
        page_size = 10
        for p in range(page_count):
            url = base_url + ('&count=%s&cursor=%s' % (page_size, p * page_size))
            d = http_get(url, proxy=self.proxy).json()
            aws = d['aweme_list']
            if not aws:
                break
            has_more = d.get('has_more')
            c = 0
            ids = [a['aweme_id'] for a in aws if 'video' in a]
            if not ids:
                continue
            url = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=%s" % ','.join(ids)
            d = http_get(url, proxy=self.proxy).json()
            for a in d['item_list']:
                vd = {}
                vd['url'] = 'https://www.iesdouyin.com/share/video/%s/' % a['aweme_id']
                vd['type'] = 'video'
                self.set_video_meta(vd, a)
                yield vd
                c += 1
            if not has_more:
                return
            time.sleep(1)

    def explain_default(self, response):
        super(DouYin, self).explain_default(response)
        if '/share/video/' in response.url:
            id = extract_between(response.url, '/share/video/', '/')
        else:
            id = response.url.split('?')[0].split('/')[-2]
        url2 = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=%s' % id
        d = http_get(url2, proxy=self.proxy).json()
        if d.get('item_list'):
            item = d['item_list'][0]
            self.set_video_meta(self.data, item)
        else:
            self.source_vanish()

    def list_huati(self, response, **kwargs):
        id = extract_between(response.url.split('?')[0], '/challenge/', '/')
        url = 'https://www.iesdouyin.com/web/api/v2/challenge/aweme/?ch_id=' + id
        for rd in self.get_aweme_list(url, page_count=kwargs.get('page_count') or 30):
            yield rd

    list_huati.url_patterns = [r'https://www.iesdouyin.com/share/challenge/(?P<huati>\d+)/']

    def list_mix(self, response, **kwargs):
        id = extract_between(response.url, '/share/mix/detail/', '/')
        url = 'https://www.iesdouyin.com/web/api/mix/item/list/?mix_id=' + id
        for i, rd in enumerate(self.get_aweme_list(url, page_count=kwargs.get('page_count') or 100)):
            rd['order_num'] = i + 1
            yield rd

    list_mix.url_patterns = [r'https://www.iesdouyin.com/share/mix/detail/(?P<heji>\d+)/']

    def extract_user_info(self, url, func):
        if func == 'list_mix':
            r = http_get(url, proxy=self.proxy)
            id = extract_between(r.url, '/detail/', '/')
            url2 = 'https://www.iesdouyin.com/web/api/mix/detail/?mix_id=' + id
            r = http_get(url2, proxy=self.proxy)
            d = r.json()['mix_info']['author']
            return dict(
                id=d['uid'],
                avatar=d['avatar_thumb']['url_list'][0],
                name=d['nickname'],
                description=d.get('signature')
            )

    def extract_list_cover(self, url, func):
        if func == 'list_huati':
            r = http_get(url, proxy=self.proxy)
            cid = extract_between(r.url, '/share/challenge/', '/')
            url = 'https://www.iesdouyin.com/web/api/v2/challenge/info/?ch_id=%s' % cid
            d = http_get(url, proxy=self.proxy).json()
            return d['ch_info']['background_image_url']['url_list'][0]
        if func == 'list_mix':
            r = http_get(url, proxy=self.proxy)
            mid = extract_between(r.url, '/share/mix/detail/', '/')
            url = 'https://www.iesdouyin.com/web/api/mix/detail/?mix_id=%s' % mid
            d = http_get(url, proxy=self.proxy).json()
            return d['mix_info']['cover_url']['url_list'][0]


@register()
class TouTiao(Vendor):
    name = '头条'
    sub_domains = ['m.toutiaoimg.cn', 'm.toutiao.com']
    type = 'video'
    test_urls = [
        'https://m.toutiaoimg.cn/a6866082028811452935/?app=news_article&is_hit_share_recommend=0'
    ]

    def explain_default(self, response):
        super(TouTiao, self).explain_default(response)
        vid = extract_between(response.url, 'toutiaoimg.cn/', '/')
        vd = get_toutiao_video(vid, proxy=self.proxy)
        self.data.update(vd)


@register()
class XiGua(Vendor):
    name = '西瓜视频'
    sub_domains = ['v.ixigua.com', 'm.ixigua.com']
    type = 'video'
    test_urls = [
        'https://v.ixigua.com/JkNfjXQ/',
        'https://m.ixigua.com/video/6797540332163564040/'
    ]

    def request_extra_params(self, f):
        d = super(XiGua, self).request_extra_params(f)
        d['cookies'] = XIGUA_EXTRA_COOKIES
        return d

    def explain_default(self, response):
        if '内容可能已删除' in response.text:
            self.source_vanish()
        super(XiGua, self).explain_default(response)
        vid = extract_between(response.url, '/video/', '/').split('?')[0]
        vd = get_toutiao_video('i' + vid, proxy=self.proxy)
        self.data.update(vd)

    def get_video_list(self, vl):
        for v in vl:
            d = {}
            d['type'] = 'video'
            d['url'] = 'https://m.ixigua.com/video/%s/' % v['item_id']
            d['name'] = v['title']
            d['duration'] = v['video_duration']
            d['unique_id'] = v['item_id']
            if v.get('publish_time'):
                d['publish_time'] = v.get('publish_time') * 1000
            yield d

    def load_heji_data(self, url):
        r = http_get(url, proxy=self.proxy, mobile_mode=False, cookies=XIGUA_EXTRA_COOKIES)
        s = extract_between(r.text, 'window._SSR_HYDRATED_DATA=', '</script>')
        d = json.loads(s.replace('undefined', 'null'))
        return d['anyVideo']['gidInformation']['packerData']

    def list_heji(self, response, **kwargs):
        series = self.load_heji_data(response.url).get('pSeries')
        if not series:
            return
        sc = series['seriesInfo']['item_num']
        ic = 0
        burl = 'https://www.ixigua.com/api/videov2/pseries_more_v2?pSeriesId=' + series['id']
        while ic < sc:
            url = burl + '&rank=%s&tailCount=30&newVersion=1' % ic
            r = http_get(url, referer=response.url)
            vl = r.json()['data']
            for i, rd in enumerate(self.get_video_list(vl)):
                rd['order_num'] = ic + i + 1
                yield rd
            ic += 30
            time.sleep(3)

    list_heji.url_patterns = [r'https://www.ixigua.com/(?P<video>\d{18,})']

    def list_user(self, response, **kwargs):
        max_time = 0
        check_exists = kwargs.get('check_exists')
        if 'to_user_id=' in response.url:
            uid = extract_between(response.url, 'to_user_id=', '&')
        elif 'm.ixigua.com' in response.url:
            uid = extract_between(response.url, '/user/', '/').split('?')[0]
        else:
            uid = extract_between(response.url, '/home/', '/')
        for p in range(kwargs.get('page_count') or 10):
            url = 'https://www.ixigua.com/api/videov2/author/video?author_id=' + uid + '&type=video&max_time=' + str(
                max_time)
            r = http_get(url, proxy=self.proxy, referer=response.url)
            d = r.json()['data']
            vl = d['data']
            for rd in self.get_video_list(vl):
                if check_exists and check_exists(rd['url']):
                    continue
                rd.update(get_toutiao_video('i%s' % rd['unique_id'], proxy=self.proxy))
                yield rd
            if not d.get('has_more'):
                return
            max_time = vl[-1].get('publish_time')

    list_user.url_patterns = [r'https://v.ixigua.com/(?P<short>\w+)/', r'https://www.ixigua.com/home/(?P<user>\w+)',
                              r'https://m.ixigua.com/user/(?P<user>\w+)']

    def extract_user_info(self, url, func):
        if func == 'list_user':
            response = self.get_response(url)
            if 'to_user_id=' in response.url:
                uid = extract_between(response.url, 'to_user_id=', '&')
                return dict(
                    id=uid,
                    url='https://www.ixigua.com/home/%s/' % uid,
                    name=response.css('.user .info .name::text').get(),
                    avatar=response.css('.user .logo .img::attr(src)').get(),
                    introduce=response.css('.user-desc .desc::text').get(),
                )
            elif '/user/' in response.url or '/home/' in response.url:
                uid = extract_between(response.url, '/user/', '/')
                return dict(
                    id=uid,
                    url=response.url,
                    name=response.css('.userinfo-detail-name::text').get(),
                    avatar=response.css('.userinfo-header-avatar::attr(src)').get(),
                    introduce=response.css('.userinfo-detail-desc .text::text').getall()[-1],
                )
        elif func == 'list_heji':
            d = self.load_heji_data(url)['video']['user_info']
            uid = d['user_id']
            return dict(
                id=uid,
                url='https://www.ixigua.com/home/%s/' % uid,
                name=d['name'],
                avatar=d['avatar_url'],
                introduce=d['description'],
                detail=d
            )


@register()
class HuoShan(Vendor):
    name = '火山视频'
    sub_domains = 'share.huoshan.com'
    type = 'video'
    test_urls = [
        'https://share.huoshan.com/hotsoon/s/P8vwvaPMGd8/'
    ]

    def explain_default(self, response):
        if '/error/404/' in response.text:
            self.source_vanish()
        super(HuoShan, self).explain_default(response)
        id = extract_between(response.url, 'item_id=', '&')
        vd = get_toutiao_video('i' + id, proxy=self.proxy)
        self.data.update(vd)
