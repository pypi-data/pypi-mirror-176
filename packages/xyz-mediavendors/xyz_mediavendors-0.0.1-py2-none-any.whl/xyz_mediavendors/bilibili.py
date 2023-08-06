# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, json, http_get
from xyz_embedmedia.decorators import register
from xyz_util.datautils import access


def trim_name(n):
    return n.replace('_哔哩哔哩 (゜-゜)つロ 干杯~-bilibili', '')


def load_data(text):
    try:
        return json.loads(extract_between(text, 'window.__INITIAL_STATE__=', ';(function'))
    except:
        raise ValueError(text)


@register()
class BiliBili(Vendor):
    name = 'B站'
    sub_domains = ['bilibili.com']
    shorturl_domain = 'b23.tv'
    type = 'video'
    test_urls = [
        'https://b23.tv/9aSrdL',
        'https://m.bilibili.com/bangumi/play/ep204779',
    ]
    image_resize = '@456w_280h_1c.webp'

    def request_extra_params(self, f):
        d = super(BiliBili, self).request_extra_params(f)
        # if f == self.list_search:
        d['mobile_mode'] = False
        return d

    def get_response(self, url, explain_func=None):
        response = super(BiliBili, self).get_response(url, explain_func)
        if '/static/jinkela/long/js/sentry/sentry' in response.text and '__INITIAL_STATE__' not in response.text:
            d = self.request_extra_params(explain_func)
            kwa = {}
            kwa.update(d)
            kwa['mobile_mode'] = False
            response = ScrapyResponse(url, **kwa)
            response = ScrapyResponse(response.url, **d)
        return response

    def is_interactive_video(self, url):
        r = http_get(url, proxy=self.proxy, mobile_mode=False)
        d = load_data(r.text)
        for a in d.get('tags', []):
            if a['tag_name'] == '互动视频':
                return True

    def invalid_video(self, v):
        if v.get('is_steins_gate') or v.get('stein_guide_cid'):  # 互动视频
            return True
        # if v.get('is_union_video'):  # 合作视频
        #     return True

    def extract_video(self, response):
        data = {}
        data['width'] = 414
        data['height'] = 233
        d = load_data(response.text)
        if 'epList' in d:
            e = d['epInfo']
            epid = e['id']
            data['name'] = e.get('toast_title') or e.get('share_copy') or d.get('h1Title')
            url2 = "https://api.bilibili.com/pgc/player/web/playurl/html5?ep_id=%s&bsource=" % epid
            r2 = http_get(url2, proxy=self.proxy, mobile_mode=True)
            d2 = r2.json()
            v = d2['result']['durl'][0]
            data['embed_url'] = v['url']
            data['duration'] = int(v['length'] / 1000)
            data['cover'] = e['cover']
            if 'pub_time' in e:
                data['publish_time'] = int(e['pub_time'] * 1000)
            elif 'mediaInfo' in d:
                data['publish_time'] = int(d['mediaInfo']['episodes'][e['i']]['pub_time'] * 1000)
            data['detail'] = e
            data['unique_id'] = 'ep%s' % e.get('id')
        else:
            p = d.get('p')
            if 'video' in d:
                d = d['video']
            if 'videoData' in d:
                d = d['videoData']
            if 'cid' not in d and 'viewInfo' in d:
                d = d['viewInfo']
            if not hasattr(self, 'nolimit'):
                if d.get('tid') == 21:
                    return None
                if self.invalid_video(d):
                    return None
            pages = d.get('pages')
            data['name'] = d['title']
            data['duration'] = d['duration']
            cid = d['cid']
            if pages and len(pages) > 1:
                p = int(p or d.get('p', 1))
                data['name'] = data['name'] + ' : ' + pages[p - 1]['part']
                cid = pages[p - 1]['cid']
                data['duration'] = pages[p - 1]['duration']
                # data['description'] = view['title']
            # d = json.loads(extract_between(response.text, '"playUrlInfo":', ',"playState"'))[0]
            data['embed_url'] = self.get_play_url(d, cid)
            data['like_count'] = d['stat']['like']
            data['publish_time'] = int(d['pubdate'] * 1000)
            data['favorite_count'] = d['stat']['favorite']
            data['share_count'] = d['stat']['share']
            data['height'] = d['dimension']['height']
            data['width'] = d['dimension']['width']
            data['unique_id'] = d.get('bvid') + str(d.get('p', ''))
            data['cover'] = d['pic']
            data['author_name'] = access(d, 'upInfo.card.name')
            # data['detail'] = d['playUrlInfo']
            data['detail'] = d
        data['name'] = trim_name(data['name'])
        data['type'] = 'video'
        return data

    def get_play_url(self, d, cid):
        url2 = 'https://api.bilibili.com/x/player/playurl?cid=' + str(cid) + '&avid=' + str(d[
            'aid']) + '&platform=html5&otype=json&qn=16&type=mp4&html5=1'
        return http_get(url2, proxy=self.proxy).json()['data']['durl'][0]['url']

    def extra_video_by_bvid(self, bvid):
        url = 'https://api.bilibili.com/x/web-interface/view/detail?aid=&bvid=%s&need_hot_share=1' % bvid
        d = http_get(url, proxy=self.proxy).json()['data']['View']
        rd = dict(
            name=d['title'],
            height=d['dimension']['height'],
            width=d['dimension']['width'],
            duration=d['duration'],
            publish_time=int(d['pubdate'] * 1000),
            favorite_count=d['stat']['favorite'],
            share_count=d['stat']['share'],
            like_count=d['stat']['like'],
            cover=d['pic'],
            unique_id=d.get('bvid') + str(d.get('p', ''))
        )
        rd['embed_url'] = self.get_play_url(d, d['cid'])
        return rd

    def explain_default(self, response):
        super(BiliBili, self).explain_default(response)
        if '啊叻？视频不见了？' in response.text:
            self.source_vanish()
        # bvid = extract_between(response.url, '/video/BV1', '?')
        # self.data.update(self.extra_video_by_bvid(bvid))
        v = self.extract_video(response)
        if not v:
            self.source_vanish()
        self.data.update(v)

    def list_rank(self, response, **kwargs):
        d = load_data(response.text)
        vl = d['rankList']
        for v in vl:
            if v['rights']['pay'] == 1:
                continue
            vd = dict(
                type='video',
                name=trim_name(v['title']),
                publish_time=int(v['pubdate'] * 1000),
                # duration=v['duration'],
                description=v['desc'],
                like_count=v['stat']['like'],
                view_count=v['stat']['view'],
                favorite_count=v['stat']['favorite'],
                url='https://www.bilibili.com/video/%s' % v['bvid']
            )
            yield vd

    def list_user(self, response, **kwargs):
        if '/space/' in response.url:
            uid = extract_between(response.url, '/space/', '?')
        else:
            uid = extract_between(response.url, 'bilibili.com/', '/')
        for p in range(kwargs.get('page_count') or 1):
            url = "https://api.bilibili.com/x/space/arc/search?mid=" + uid + "&ps=30&tid=0&pn=" + str(
                p + 1) + "&keyword=&order=pubdate&jsonp=jsonp"
            d = http_get(url, proxy=self.proxy).json()
            vl = d['data']['list']['vlist']
            if len(vl) < 1:
                break
            for v in vl:
                if self.invalid_video(v):
                    continue
                url = 'https://www.bilibili.com/video/%s' % v['bvid']
                name = trim_name(v['title'])
                publish_time = int(v['created'] * 1000)
                if v['typeid'] == 183:
                    for vd in self.list_heji(self.get_response(url)):
                        vd['name'] = name + ' : ' + vd['name']
                        vd['publish_time'] = publish_time
                        yield vd
                else:
                    vd = dict(
                        type='video',
                        name=name,
                        publish_time=publish_time,
                        order_num=int(v['created']),
                        cover=v['pic'],
                        url=url
                    )
                    yield vd

    list_user.url_patterns = [r'https://space.bilibili.com/(?P<user>\d+)']

    def list_heji(self, response, **kwargs):
        if '啊叻？视频不见了？' in response.text:
            self.source_vanish()
        d = load_data(response.text)
        if 'epList' in d:
            for i, e in enumerate(d['epList']):
                vd = dict(
                    order_num=i + 1,
                    type='video',
                    name=trim_name(e['toast_title']),
                    url=e['link']
                )
                yield vd
        else:
            vid = extract_between(response.url, '/video/', '?')
            ps = access(d, 'video.viewInfo.pages') or access(d, 'videoData.pages')
            for i, p in enumerate(ps):
                vd = dict(
                    order_num=i + 1,
                    type='video',
                    name=trim_name(p['part']),
                    url='https://m.bilibili.com/video/' + vid + '?p=' + str(p['page'])
                )
                yield vd

    list_heji.url_patterns = [r'https://www.bilibili.com/video/(?P<video>\w+)']

    def list_channel(self, response, **kwargs):
        cid = extract_between(response.url, '/channel/', '?')
        offset = None
        for p in range(kwargs.get('page_count') or 10):
            url = "https://api.bilibili.com/x/web-interface/web/channel/featured/list?channel_id=" + cid + "&filter_type=0&page_size=30"
            if offset:
                url = url + '&offset=' + offset
            d = http_get(url, proxy=self.proxy).json()['data']
            for v in d['list']:
                if 'id' not in v:
                    continue
                if self.invalid_video(v):
                    continue
                vd = dict(
                    type='video',
                    name=trim_name(v['name']),
                    author_name=v.get('author_name'),
                    url='https://www.bilibili.com/video/%s' % v['bvid']
                )
                yield vd
            offset = d['offset']

    def list_channel_zonghe(self, response, **kwargs):
        cid = extract_between(response.url, '/channel/', '?')
        url = 'https://api.bilibili.com/x/web-interface/web/channel/multiple/list?channel_id=' + cid + '&sort_type=hot&page_size=1'
        d = http_get(url, proxy=self.proxy).json()['data']['list'][0]
        if d['card_type'] == 'rank':
            for v in d['items']:
                if self.invalid_video(v):
                    continue
                url = 'https://www.bilibili.com/video/%s' % v['bvid']
                vd = self.extract_video(ScrapyResponse(url, mobile_mode=False))
                if vd:
                    vd['url'] = url
                    yield vd

    def list_search(self, response, **kwargs):
        from xyz_util.dateutils import format_the_date
        from xyz_embedmedia.helper import ensure_url_schema
        import time
        burl = response.url.split('&page=')[0]
        for p in range(kwargs.get('page_count') or 1):
            url = burl + '&page=' + str(p + 1)
            response = self.get_response(url, self.list_search)
            for e in response.css('.video-list .video-item'):
                a = e.css('a')[0]
                dt = format_the_date(e.css('.tags .time::text').get().strip())
                ts = int(time.mktime(dt.timetuple())) * 1000
                vd = dict(
                    type='video',
                    url=ensure_url_schema(a.css('::attr(href)').get()),
                    name=a.css('::attr(title)').get(),
                    publish_time=ts
                )
                yield vd

    def search(self, keyword):
        ps = keyword.split('|')
        keyword = ps[-1]
        tab = 'multiple' if ps[-2] == '综合' else 'featured'
        url = 'https://api.bilibili.com/x/web-interface/web/channel/search?keyword=%s&page_size=10&page=1' % keyword
        d = http_get(url, proxy=self.proxy).json()['data']
        for cs in ['archive_channels', 'ext_channels']:
            for c in d[cs]:
                if c['name'] == keyword:
                    return 'https://www.bilibili.com/v/channel/%s?keyword=%s&tab=%s' % (c['id'], keyword, tab)

    def extract_user_info(self, url, func):
        uid = None
        if func == 'list_user':
            uid = url.split('/')[3]
        elif func == 'list_heji':
            d = load_data(http_get(url).text)
            uid = d['video']['viewInfo']['owner']['mid']
        if uid:
            url = 'https://m.bilibili.com/space/%s' % uid
            r = http_get(url)
            d = load_data(r.text)['space']['info']
            return dict(
                id=d['mid'],
                url=url,
                name=d['name'],
                avatar=d['face'],
                introduce=d['sign'],
                gender='m' if d['sex'] == '男' else 'f',
                detail=d
            )
