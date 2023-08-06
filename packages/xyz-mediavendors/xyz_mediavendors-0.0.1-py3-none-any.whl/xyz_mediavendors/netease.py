# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, json, http_post
from xyz_embedmedia.decorators import register
import requests
from datetime import datetime, timedelta
import time
from .encrypt.netease import encrypted_request


@register()
class NetEaseMusic(Vendor):
    name = '网易云音乐'
    sub_domains = ['music.163.com']
    shorturl_domain = '163.lu'
    type = 'audio'
    test_urls = [
        'https://y.music.163.com/m/song/1369422144/?userid=565926694',
        'https://y.music.163.com/m/song/1468482061/?userid=3869363373',
        'http://163.lu/c5sgf2',
        'http://music.163.com/video/3FD449C6BA273B0B7D9DF5A402DE2745/?userid=3869363373'
    ]
    image_resize = '?param=140y140'

    def get_response(self, url, explain_func=None):
        if url.startswith('https://music.163.com/#/mv'):
            url = url.replace('https://music.163.com/#/mv', 'https://y.music.163.com/m/mv')
        return super(NetEaseMusic, self).get_response(url, explain_func=explain_func)

    def explain_default(self, response):
        if 'music.163.com' not in response.url:
            return
        if '/listen-together/' in response.url:
            id = extract_between(response.url, 'songId=', '&')
            url = 'https://y.music.163.com/m/song/' + id
            response = self.get_response(url)
        if 'video' in response.url:
            return self.explain_video(response)
        if '/mv' in response.url:
            return self.explain_mv(response)
        super(NetEaseMusic, self).explain_default(response)
        id = extract_between(response.url, '/song/', '/')
        if not id:
            id = extract_between(response.url, 'songId=', '&')
        if not id:
            id = response.url.split('id=')[-1]
        self.data['embed_url'] = "http://music.163.com/song/media/outer/url?id=%s.mp3" % id

    def extract_mv(self, response):
        rd = {}
        d = json.loads(extract_between(response.text, 'REDUX_STATE = ', ';\n'))
        d = d['MV']['data']
        rd['name'] = d['name']
        rd['description'] = d['desc']
        rd['cover'] = d['cover']
        rd['duration'] = d['duration'] / 1000
        rd['detail'] = d
        id = extract_between(response.url, 'id=', '&')
        url = 'https://interface.music.163.com/weapi/song/enhance/play/mv/url'
        qd = {'id': id, 'r': '720'}
        r = http_post(url, data=encrypted_request(qd), proxy=self.proxy)
        d = r.json()['data']
        rd['expire_time'] = int(time.mktime((datetime.now() + timedelta(seconds=d['expi'])).timetuple())) * 1000
        rd['embed_url'] = d['url']
        rd['type'] = 'video'
        return rd

    def explain_mv(self, response):
        super(NetEaseMusic, self).explain_default(response)
        self.data.update(self.extract_mv(response))

    def explain_video(self, response):
        super(NetEaseMusic, self).explain_default(response)
        d = json.loads(extract_between(response.text, 'REDUX_STATE = ', ';\n'))
        d = d['Video']['data']
        self.data['name'] = d['name']
        self.data['cover'] = d['coverUrl']
        self.data['detail'] = d
        self.data['width'] = d['width']
        self.data['height'] = d['height']
        id = extract_between(response.url, 'id=', '&')
        url = 'https://interface.music.163.com/weapi/cloudvideo/playurl'
        qd = {'ids': '["' + id + '"]', "resolution": "720", "csrf_token": ""}
        r = http_post(url, data=encrypted_request(qd), proxy=self.proxy)
        d = r.json()
        self.data['embed_url'] = d['urls'][0]['url']
        self.data['type'] = 'video'

    def search_singer(self, name):
        url = 'https://music.163.com/weapi/search/suggest/multimatch'
        r = http_post(url, data=encrypted_request({'s': name}), proxy=self.proxy)
        d = r.json()
        if d.get('code') != 200:
            print(d.get('code'), d.get('result'))
            return
        for a in d.get('result', {}).get('artist', []):
            if a['name'] == name:
                return a

    def get_singer_songs(self, singer_id):
        url = 'https://music.163.com/artist?id=%s' % singer_id
        response = ScrapyResponse(url, mobile_mode=False)
        dl = json.loads(response.css('#song-list-pre-data::text').get())
        for d in dl:
            yield d

    def get_song_lyrics(self, sid):
        url = 'https://music.163.com/weapi/song/lyric'
        r = http_post(url, data=encrypted_request({'id': sid, 'lv': -1, 'tv': -1}), proxy=self.proxy)
        lyric = r.json()['lrc']['lyric']
        if not lyric:
            return
        from ..helper import explain_lyrics, get_lyrics_text
        return get_lyrics_text(explain_lyrics(lyric))

    def get_song_comment_count(self, sid):
        url = 'https://music.163.com/weapi/comment/resource/comments/get'
        r = http_post(url, data=encrypted_request({'rid': sid, 'threadId': sid}), proxy=self.proxy)
        d = r.json()
        c = d['data']['totalCount']
        return c


@register()
class NetEaseVideo(Vendor):
    name = '网易视频'
    sub_domains = {'m.163.com': 'default', 'open.163.com': 'open'}
    shorturl_domain = '163.lu'
    type = 'video'
    test_urls = [
        'https://c.m.163.com/news/v/VIKEDEB08.html?spss=newsapp',
        'https://c.m.163.com/news/v/VUKJC0UII.html?spss=newsapp',
        'http://163.lu/jBa060'
    ]

    def explain_default(self, response):
        super(NetEaseVideo, self).explain_default(response)
        vid = extract_between(response.url, '/news/v/', '.html')
        url2 = "https://gw.m.163.com/nc-gateway/api/v1/video/detail/%s" % vid
        r = ScrapyResponse(url2)
        d = json.loads(r.text)['data']
        self.data['name'] = d['title']
        self.data['cover'] = d['cover']
        self.data['embed_url'] = d['mp4_url']
        self.data['description'] = d['desc']
        self.data['duration'] = d['video_data'].get('duration')
        self.data['detail'] = d
        self.data['width'] = 414
        self.data['height'] = 233

    def explain_open(self, response):
        response = ScrapyResponse(response.url, mobile_mode=False)
        super(NetEaseVideo, self).explain_default(response)
        self.data['name'] = response.css('.i-container__title::text').get().strip()
        self.data['cover'] = extract_between(response.text, 'imgPath:"', '"').replace('\\u002F', '/')
        self.data['embed_url'] = (
                extract_between(response.text, 'mp4ShdUrl:"', '"') or extract_between(response.text, 'm3u8SdUrl:"',
                                                                                      '"')).replace('\\u002F', '/')
        self.data['duration'] = int(extract_between(response.text, 'mLength:', ','))
        self.data['width'] = 414
        self.data['height'] = 240
