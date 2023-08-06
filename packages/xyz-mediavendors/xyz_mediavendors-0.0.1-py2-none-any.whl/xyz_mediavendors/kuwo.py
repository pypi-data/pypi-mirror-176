# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, http_get
from xyz_embedmedia.decorators import register
import requests, time, json
try:
    from django.utils.six.moves.urllib.parse import urlsplit
except:
    from urllib.parse import urlsplit

try:
    from urllib import unquote
except:
    from urllib.parse import unquote

from six import text_type

def trim_name(name):
    return name.replace('在线试听', '')


def date2timestamp(d):
    if not d:
        return
    import re
    r = re.compile('[/-]')
    try:
        ps = [int(a) for a in r.split(d)]
        if len(ps) != 3:
            return
        t = int(time.mktime(ps + [0, 0, 0, 0, 0, 0])) * 1000
        if t > 0:
            return t
    except:
        pass


@register()
class KuWo(Vendor):
    name = '酷我音乐'
    sub_domains = ['kuwo.cn']
    type = 'audio'
    test_urls = [
        'http://m.kuwo.cn/newh5app/play_detail/6728930?f=arphone&t=usercopy&isstar=0',
        'https://mobile.kuwo.cn/mv/222914?from=ar&t=plantform&type=7'
    ]

    def request_extra_params(self, func):
        d = super(KuWo, self).request_extra_params(func)
        if func in [self.list_mv, self.list_music]:
            d.update(mobile_mode=False, extra_headers=dict(csrf='572P4YUJ5BU'),
                     cookies=dict(kw_token='572P4YUJ5BU'), referer='http://www.kuwo.cn')
        return d

    def extract_music(self, id):
        # url2 = 'https://www.kuwo.cn/url?format=mp3&rid='+id+'&response=url&type=convert_url3&br=128kmp3&from=web'
        # d = requests.get(url2).json()
        url2 = 'http://m.kuwo.cn/newh5app/api/mobile/v1/music/src/' + id
        d = requests.get(url2).json()['data']
        return dict(embed_url=d['url'], duration=d['duration'], type='audio')

    def explain_default(self, response):
        if '/mv/' in response.url:
            return self.explain_mv(response)
        super(KuWo, self).explain_default(response)
        id = extract_between(response.text, 'songInfo:{id:', ',')
        if not id:
            id = urlsplit(response.url).path.split('/')[-1]
        d = self.extract_music(id)
        self.data['name'] = trim_name(self.data['name'])
        self.data.update(d)

    def explain_mv(self, response):
        super(KuWo, self).explain_default(response)
        id = extract_between(response.url, '?id=', '&')
        url = 'http://antiserver.kuwo.cn/anti.s?rid=MUSIC_' + id + '&response=res&format=mp4|mkv&type=convert_url'
        self.data['embed_url'] = url
        self.data['type'] = 'video'
        self.data['width'] = 414
        self.data['height'] = 243

    def search(self, keyword):
        mtype = 'Mv' if 'MV' in keyword else 'Music'
        ps = keyword.split('|')
        keyword = ps[-1]
        url = 'https://www.kuwo.cn/api/www/search/search' + mtype + 'BykeyWord?key=' + keyword + '&pn=1&rn=30&httpsStatus=1'
        response = self.get_response(url, self.list_mv)
        r = response.r
        d = r.json()['data']
        if d['total'] == 0:
            return
        return url

    def list_music(self, response, **kwargs):
        furl = response.url
        key = text_type(unquote(str(extract_between(furl, 'key=', '&'))))
        for p in range(kwargs.get('page_count') or 30):
            r = response.r
            d = r.json()
            if d['code'] != 200:
                return
            vl = d['data']['list']
            if len(vl) == 0:
                return
            for v in vl:
                if v['artist'] != key:
                    continue
                if v['payInfo'].get('play') == '1111':
                    continue
                id = str(v['rid'])
                yield dict(
                    url='http://m.kuwo.cn/newh5app/play_detail/' + id,
                    name=trim_name(v['name']),
                    type='audio',
                    cover=v['pic'],
                    duration=v['duration'],
                    publish_time=date2timestamp(v.get('releaseDate'))
                )
            url = furl.replace('&pn=1&', '&pn=' + str(p + 2) + '&')
            response = self.get_response(url, self.list_music)

    def list_mv(self, response, **kwargs):
        furl = response.url
        key = text_type(unquote(str(extract_between(furl, 'key=', '&'))))
        for p in range(kwargs.get('page_count') or 30):
            r = response.r
            d = r.json()['data']
            vl = d['mvlist']
            if len(vl) == 0:
                return
            for v in vl:
                if v['artist'] != key:
                    continue
                id = str(v['id'])
                yield dict(
                    url='https://www.kuwo.cn/mvplay/' + id,
                    name=trim_name(v['name']),
                    type='video',
                    cover=v['pic'],
                    embed_url='http://antiserver.kuwo.cn/anti.s?rid=MUSIC_' + id + '&response=res&format=mp4|mkv&type=convert_url',
                    duration=v['duration'],
                    publish_time=date2timestamp(v.get('releaseDate'))
                )
            url = furl.replace('&pn=1&', '&pn=' + str(p + 2) + '&')
            response = self.get_response(url, self.list_mv)

    def extract_person(self, response):
        import js2py
        js = extract_between(response.text, 'window.__NUXT__=', ';</script>')
        return js2py.eval_js(js).to_dict()['data'][0]['person']

    def list_playlist(self, response, **kwargs):
        pid = extract_between(response.url, '/playlist_detail/', '/')
        for p in range(kwargs.get('page_count') or 30):
            url = 'http://m.kuwo.cn/newh5app/api/mobile/v1/music/playlist/%s?pn=%s&rn=20' % (pid, p+1)
            r = http_get(url, proxy=self.proxy)
            vl = r.json()['data']['musicList']
            if not vl:
                break
            for v in vl:
                yield dict(
                    url='http://m.kuwo.cn/newh5app/play_detail/%s' % v['id'],
                    name=trim_name(v['name']),
                    type='audio',
                    cover=v['pic']
                )

    list_playlist.url_patterns = [r'https://kuwo.cn/playlist_detail/(?P<playlist>\d+)']


    def extract_user_info(self, url, func):
        if func == 'list_playlist':
            d = self.extract_person(http_get(url))
            d.pop('musicList', None)
            avatar = d['user_pic']
            id = extract_between(avatar, '_', '.')
            return dict(
                id=id or d['user_name'],
                url=url,
                name=d['user_name'],
                avatar=avatar,
                detail=d
            )
