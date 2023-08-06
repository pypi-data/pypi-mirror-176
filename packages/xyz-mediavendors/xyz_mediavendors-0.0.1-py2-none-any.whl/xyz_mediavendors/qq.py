# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, http_get
import json
from xyz_embedmedia.decorators import register
import requests
from xyz_util.datautils import access

try:
    from urllib import unquote, quote
except:
    from urllib.parse import unquote, quote


def get_qqvideo_url(vid):
    url = "https://h5vv6.video.qq.com/getinfo?callback=txplayerJsonpCallBack_getinfo_525940&sdtfrom=v3010&platform=11001&guid=ee995fc72f87d80d9cf02927e7249f63&otype=json&vid=%s" % vid
    r = ScrapyResponse(url)
    s = r.text[len('txplayerJsonpCallBack_getinfo_525940('):-1]
    d2 = json.loads(s)['vl']['vi'][0]
    vkey = d2['fvkey']
    server = d2['ul']['ui'][-1]['url']
    fn = d2['fn']
    return "%s%s?sdtfrom=v3010&platform=11001&guid=ee995fc72f87d80d9cf02927e7249f63&vkey=%s" % (server, fn, vkey)


def get_qqmusic_video_url(vid):
    url = "https://u.y.qq.com/cgi-bin/musicu.fcg?g_tk=5381&uin=0&ct=23&cv=0&format=json&callback=qmv_jsonp_2&data=%7B%22getMVInfo%22%3A%7B%22module%22%3A%22video.VideoDataServer%22%2C%22method%22%3A%22get_video_info_batch%22%2C%22param%22%3A%7B%22vidlist%22%3A%5B%22" + vid + "%22%5D%2C%22required%22%3A%5B%22vid%22%2C%22sid%22%2C%22gmid%22%2C%22type%22%2C%22name%22%2C%22cover_pic%22%2C%22video_switch%22%2C%22msg%22%5D%2C%22from%22%3A%22h5.mvplay%22%7D%7D%2C%22getMVUrl%22%3A%7B%22module%22%3A%22gosrf.Stream.MvUrlProxy%22%2C%22method%22%3A%22GetMvUrls%22%2C%22param%22%3A%7B%22vids%22%3A%5B%22" + vid + "%22%5D%2C%22from%22%3A%22h5.mvplay%22%7D%2C%22request_typet%22%3A10001%7D%7D&_=1599037500304&platform=h5"
    r = ScrapyResponse(url)
    s = r.text[len('qmv_jsonp_2('):-1]
    d = json.loads(s)
    urls = d['getMVUrl']['data'][vid]['mp4'][:3]
    urls.reverse()
    for a in urls:
        if a['cn']:
            return a['url'][0] + a['vkey'] + '/' + a['cn']


@register()
class QQVideo(Vendor):
    name = 'QQ视频'
    sub_domains = 'v.qq.com'
    type = 'video'
    test_urls = [
        'http://m.v.qq.com/play.html?cid=mzc00200d8fkodt&vid=w0034gah3qo&url_from=share&second_share=0&share_from=copy&pgid=page_detail&mod_id=mod_toolbar',
        'https://m.v.qq.com/x/m/play?cid=mzc002005vjz76n&vid=e0034ni0zdf'
    ]
    icon = 'http://v.qq.com/favicon.ico'

    def explain_default(self, response):
        if '/x/cover/' in response.url:
            ps = extract_between(response.url, '/x/cover/', '.html').split('/')
            cid = ps[0]
            vid = ps[1] if len(ps) > 1 else ''
            url = 'https://m.v.qq.com/play.html?cid=' + cid + '&vid=' + vid + '&ptag=v_qq_com%23v.play.adaptor%233'
            response = self.get_response(url, self.explain_default)
        super(QQVideo, self).explain_default(response)
        v = response.css('input[id="play_sync"]::attr(value)').get()
        d = json.loads(unquote(str(v)))['playData']
        vd = d['video']
        vid = vd['vid']
        self.data['name'] = vd['title']
        self.data['duration'] = vd['duration']
        self.data['cover'] = d['sharePicture']
        self.data['description'] = ''  # d['cover']['description']
        self.data['embed_url'] = get_qqvideo_url(vid)
        self.data['detail'] = vd
        self.data['width'] = 414
        self.data['height'] = 233


@register()
class QQKG(Vendor):
    name = '全民K歌'
    sub_domains = 'kg[0-9]*.qq.com'
    type = 'video'
    test_urls = [
        'https://kg3.qq.com/node/play?s=41iDVQ4cpG_HC4bf&shareuid=65949a802029308d32&topsource=a0_pn201001006_z11_u797554766_l1_t1598336304__',
        'https://kg2.qq.com/node/play?s=JrLVZeJ6j04nxJJ5&shareuid=639a95812c24328837&topsource=a0_pn201001006_z11_u178499533_l1_t1598701493__'
    ]

    def explain_default(self, response):
        super(QQKG, self).explain_default(response)
        s = extract_between(response.text, 'window.__DATA__ = ', '; </script>')
        d = json.loads(s)['detail']
        embed_url = d.get('playurl_video')
        if embed_url:
            # embed_url = wrap_h5player(embed_url)
            type = 'video'
            self.data['width'] = 414
            self.data['height'] = 736
        else:
            type = 'audio'
            embed_url = d.get('playurl')
        self.data['embed_url'] = embed_url
        self.data['detail'] = d
        self.data['type'] = type


@register()
class QQMusic(Vendor):
    name = 'QQ音乐'
    sub_domains = 'y.qq.com'
    type = 'audio'
    test_urls = [
        'https://c.y.qq.com/base/fcgi-bin/u?__=KgNHRN9',
        'https://c.y.qq.com/base/fcgi-bin/u?__=KxJXOEN',
        'https://c.y.qq.com/base/fcgi-bin/u?__=kVA1bEr'
    ]
    icon = 'https://i.y.qq.com/favicon.ico'

    def __init__(self, proxy=True):
        Vendor.__init__(self, proxy=proxy)

    def get_response(self, url, explain_func=None):
        if '/n/yqq/mv/v/' in url:
            vid = extract_between(url, '/n/yqq/mv/v/', '.html')
            url = 'https://i.y.qq.com/n2/m/share/details/mv.html?ADTAG=newyqq.mv&vid=%s' % vid
        elif '/n/yqq/song/' in url:
            smid = extract_between(url, '/n/yqq/song/', '.html')
            url = 'https://i.y.qq.com/v8/playsong.html?ADTAG=newyqq.song&songmid=%s#webchat_redirect' % smid
        return super(QQMusic, self).get_response(url, explain_func=explain_func)

    def explain_default(self, response):
        super(QQMusic, self).explain_default(response)
        js = extract_between(response.text, 'window.__ssrFirstPageData__ =', '</script>')
        if js:
            d = json.loads(js)
            m = d['metaData']
            s = d['songList'][0]
            self.data['embed_url'] = s['url']
            self.data['duration'] = s.get('interval')
            self.data['detail'] = d
            self.data['cover'] = m.get('image')
            self.data['name'] = '%s - %s' % (s['name'], s['singer'][0]['name'])
            try:
                self.data['like_count'] = self.get_song_comment_count(s['id']) * 100
            except:
                pass
        else:
            js = extract_between(response.text, 'var firstPageData = ', '</script>')
            self.data.update(self.extract_mv_info(js))

    def get_mv_info(self, url):
        r = http_get(url, proxy=self.proxy)
        s = extract_between(r.text, 'var firstPageData = ', '</script>')
        return self.extract_mv_info(s)

    def extract_mv_info(self, s):
        d = json.loads(s)
        rd = {}
        mv = d['mvInfo']
        vid = mv['vid']
        rd['embed_url'] = get_qqmusic_video_url(vid) if mv['type'] in [0, 1, 2] else get_qqvideo_url(vid)
        rd['detail'] = mv
        rd['type'] = 'video'
        rd['cover'] = mv['cover_pic_medium']
        rd['width'] = 414
        rd['height'] = 233
        rd['duration'] = access(d, 'songList.0.interval') or 0
        rd['like_count'] = self.get_song_star_count(access(d, 'songList.0.mv.id') or access(mv, 'sid'))
        return rd

    def call_musicv(self, d):
        js = json.dumps(d)
        url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?format=json&callback=qmv_jsonp_2&data=%s' % quote(js)
        r = http_get(url, proxy=self.proxy)
        d = json.loads(r.text[len('qmv_jsonp_2('): -1])
        return d

    def get_song_comment_count(self, songid):
        d = {
            'commentList': {
                'method': 'GetNewCommentList',
                'module': 'music.globalComment.CommentReadServer',
                'param': {
                    'BizId': '%s' % songid,
                    'BizType': 1,
                    'FromCommentId': '',
                    'LastCommentId': '',
                    'LastCommentSeqNo': '',
                    'PageNum': 0,
                    'PageSize': 1,
                    'WithHot': 1
                }
            }
        }
        d = self.call_musicv(d)
        return d['commentList']['data']['CommentList2']['Total']

    def get_song_star_count(self, songid):
        songid = str(songid)
        d = {
            'comm': {'format': 'json', 'g_tk': 5381, 'platform': 'h5', 'uin': 0},
            'req_0': {
                'method': 'get_item_star_count',
                'module': 'star.MusicStarServer',
                'param': {'biz_id': 1, 'item_ids': [songid]}
            }
        }
        d = self.call_musicv(d)
        return d['req_0']['data']['item_star_count'][songid]

    def list_singer(self, response, **kwargs):
        params = {"index": -100, "area": -100, 'sex': -100, 'genre': -100, "sin": 0, "cur_page": 1}
        params.update(kwargs.get('params', {}))
        print(params)
        d = {
            'comm': {'ct': 24, 'cv': 0},
            'singerList': {'method': 'get_singer_list',
                           'module': 'Music.SingerListServer',
                           'param': params
                           }
        }
        rd = self.call_musicv(d)
        return rd['singerList']['data']['singerlist']

    def list_singer_mv(self, response, **kwargs):
        mid = kwargs.get('singer')
        d = {
            'comm': {'ct': 24, 'cv': 0},
            'singerSongList': {
                'method': 'GetSingerSongList',
                'module': 'musichall.song_list_server',
                'param': {'begin': 0, 'num': 10, 'order': 1, 'singerMid': mid}
            }
        }
        rd = self.call_musicv(d)
        for s in rd['singerSongList']['data']['songList']:
            song = s['songInfo']
            if song['mv']['id'] <= 0:
                continue
            yield song

    def get_song_lyrics(self, sid):
        url = 'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_yqq.fcg?nobase64=1&musicid=%s' % sid
        r = http_get(url, mobile_mode=False, referer='https://y.qq.com/')
        lyric = extract_between(r.text, '"lyric":"', '"})')
        if not lyric:
            return
        from ..helper import explain_lyrics, get_lyrics_text
        return get_lyrics_text(explain_lyrics(lyric))

    def get_song_detail(self, sid):
        d = {
            'comm': {'ct': 24, 'cv': 0},
            'songinfo': {
                'method': 'get_song_detail_yqq',
                'module': 'music.pf_song_detail_svr',
                'param': {
                    'song_id': sid,
                    'song_type': 0
                }
            }
        }
        rd = self.call_musicv(d)
        return rd['songinfo']['data']['info']


@register()
class WeiShi(Vendor):
    name = '腾讯微视'
    sub_domains = 'weishi.qq.com'
    type = 'video'
    test_urls = [
        'https://h5.weishi.qq.com/weishi/feed/6YGV3aGiZ1Kb4T2m3/wsfeed?wxplay=1&id=6YGV3aGiZ1Kb4T2m3&spid=1530578021092841',
        'https://h5.weishi.qq.com/weishi/feed/7j050mhRy1K3vxlBD/wsfeed?wxplay=1&id=7j050mhRy1K3vxlBD&collectionid=b408a556dbec3b383bb5e0ae9b571261&spid=8861440615642869760'
    ]

    def explain_default(self, response):
        super(WeiShi, self).explain_default(response)
        vid = extract_between(response.url, '/weishi/feed/', '/wsfeed')
        if not vid:
            vid = extract_between(response.url, '&id=', '&')
        if not vid:
            return {}
        url2 = "https://h5.weishi.qq.com/webapp/json/weishi/WSH5GetPlayPage?t=0.6836771789516459&g_tk="
        r = requests.post(url2, {"feedid": vid})
        d = json.loads(r.text)
        d = d['data']['feeds'][0]
        v = d['video']
        self.data['name'] = d['feed_desc']
        self.data['duration'] = int(v['duration'] / 1000)
        self.data['height'] = v['height']
        self.data['width'] = v['width']
        self.data['embed_url'] = d['video_url']
        self.data['cover'] = d['share_info']['sq_ark_info']['shareBody']['image_url']
        self.data['description'] = ''
        self.data['detail'] = v
