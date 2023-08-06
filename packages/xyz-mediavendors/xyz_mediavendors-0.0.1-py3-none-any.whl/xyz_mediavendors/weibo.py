# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, json, http_get, urlsplit, UA_PC, html2text
from xyz_embedmedia.decorators import register
from six import string_types
try:
    from urllib.parse import quote
except:
    from urllib import quote

from xyz_util.datautils import access
import logging
from datetime import datetime
import time, requests, re

log = logging.getLogger('django')

SUB = '_2A25yXD83DeRhGeFL61MR8ibNzz6IHXVRv0F_rDV6PUJbktANLXTukW1NQrMrK1VKfBMIRgv92jV634tIeVcfZYGr'


def trim_name(n):
    r = re.compile(r'[^\s,.~）。，！？～\]]*?的微博视频( |$)')
    return r.sub('', n).replace('[超话]#', '#')


@register()
class Weibo(Vendor):
    name = '微博'
    sub_domains = {'m.weibo.cn': 'default', 'h5.video.weibo.com': 'h5video', 'video.weibo.com': 'h5video',
                   'weibo.com': 'h5video'}
    type = 'video'
    test_urls = [
        'https://m.weibo.cn/1618051664/4542522838227884',
        'https://m.weibo.cn/detail/4545154172060507',
        'https://video.weibo.com/show?fid=1034:4557885628416006'
    ]
    icon = 'https://m.weibo.cn/favicon.ico'

    def get_response(self, url, explain_func=None):
        response = super(Weibo, self).get_response(url, explain_func=explain_func)
        NOCONTENT = '"\\u8fd9\\u91cc\\u8fd8\\u6ca1\\u6709\\u5185\\u5bb9"'  # '这里还没有内容'
        if '打开微博客户端，查看全文' in response.text or NOCONTENT in response.text:
            r = response.r
            r.cookies.set('SUB', SUB)
            response = ScrapyResponse(url, cookies=r.cookies, proxy=self.proxy)
        if '由于作者隐私设置，你没有权限查看此微博' in response.text:
            self.source_vanish()
        return response

    def extract_default(self, text):
        s = extract_between(text, 'var $render_data = [', '][0] || {};')
        if not s:
            return
        d = json.loads(s)
        if not d:
            return
        mblog = d['status']
        if 'page_info' not in mblog and 'retweeted_status' in mblog:
            mblog = mblog['retweeted_status']
        return self.extract_video(mblog, list_mode=False)

    def explain_default(self, response):
        super(Weibo, self).explain_default(response)
        d = self.extract_default(response.text)
        if d:
            self.data.update(d)

    def explain_h5video(self, response):
        super(Weibo, self).explain_default(response)
        ps = response.url.split('/')
        vid = ps[-1]
        if ':' in vid:
            d = self.extract_by_object_id(vid)
        else:
            url = 'https://m.weibo.cn/detail/' + vid
            text = http_get(url, proxy=self.proxy).text
            d = self.extract_default(text)
            if not d:
                if (':' in ps[-2]):
                    d = self.extract_by_object_id(ps[-2])
        if d:
            self.data.update(d)

    def extract_video(self, mblog, list_mode=True):
        if 'page_info' not in mblog:
            return
        p = mblog['page_info']
        if p['type'] != 'video':
            return
        if 'media_info' not in p:
            return
        m = p['media_info']
        if not m.get('stream_url'):
            return
        rd = {}
        if 'video_publish_time' in m:
            rd['publish_time'] = m.get('video_publish_time') * 1000
        else:
            pt = datetime.strptime(mblog.get('created_at'), '%a %b %d %H:%M:%S +0800 %Y')
            rd['publish_time'] = int(time.mktime(pt.timetuple())) * 1000
        murl = m.get('stream_url', '')
        finger = extract_between(murl, 'trans_finger=', '&')
        if finger and len(finger) == 32:
            rd['unique_id'] = finger[:16]+murl.split('.mp4')[0][-16:]
        else:
            rd['unique_id'] = m.get('media_id')[-32:] if m.get('media_id') else mblog.get('mid')
        rd['type'] = 'video'
        text = html2text(mblog.get('text').replace('超话</span>','</span>')) if mblog.get('text') else ''
        rd['name'] = text[:255] or access(m, 'titles.0.title') or m.get('next_title') or p.get('content2')
        mid = mblog['mid']
        rd['url'] = 'https://m.weibo.cn/detail/' + mid
        if mblog.get('isLongText'):
            if list_mode:  # 长文本留到发贴时再解释
                return rd
            if mblog.get('text'):
                rd['content'] = trim_name(text)
        rd['embed_url'] = murl
        rd['cover'] = p['page_pic']['url']
        rd['duration'] = int(float(m.get('duration'))) if m.get('duration') else None
        if 'back_paster_info' in m:
            rd['width'] = m['back_paster_info']['request_param']['width']
            rd['height'] = m['back_paster_info']['request_param']['height']
        rd['url'] = 'https://m.weibo.cn/detail/%s' % mblog['mid']
        rd['orientation'] = m.get('video_orientation') or p.get('video_orientation')
        rd['like_count'] = mblog.get('attitudes_count')
        rd['comments_count'] = mblog.get('comments_count')
        rd['reposts_count'] = mblog.get('reposts_count')
        rd['play_count'] = m.get('online_users_number')
        rd['name'] = trim_name(rd['name'])
        return rd

    def extract_videos(self, d):
        for c in d['cards']:
            if 'card_group' in c:
                gs = c['card_group']
            else:
                gs = [c]
            for g in gs:
                if 'mblog' not in g:
                    continue
                rd = self.extract_video(g['mblog'])
                if not rd:
                    continue
                yield rd

    def search(self, name, category=None):
        if category:
            cs = category.split('|')
        else:
            ps = name.split('|')
            cs = ps[:-1]
            name = ps[-1]
        tag = cs[0]
        if tag in ['视频', '热门视频']:
            url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D72%26q%3D' + name + '%26t%3D0&extparam=title%3D%E7%83%AD%E9%97%A8%E8%A7%86%E9%A2%91&luicode=10000011&lfid=100103type%3D64%26amp%3Bq%3D' + name + '%26amp%3Bt%3D0'
            r = http_get(url, proxy=self.proxy, cookies=dict(SUB=SUB))
            return url if r.json()['data'].get('cards') else None
        tag_map = {'超话': 98, '话题': 38, '视频': 72}
        type_map = {'精华': '_-_soul', '热门': 60}
        qs = quote(str('%s&q=%s&t=0' % (tag_map[tag], name)))
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type=' + qs + '&page_type=searchall&page=0'
        if len(cs) < 2:
            return url
        r = http_get(url, proxy=self.proxy, cookies=dict(SUB=SUB))
        d = r.json()['data']
        url2 = None
        for c in d['cards']:
            for g in c['card_group']:
                if g['title_sub'] in [name, '#' + name + '#']:
                    url2 = 'https://m.weibo.cn/api/container/getIndex?' + urlsplit(g['scheme']).query
                    break
            else:
                continue
            break
        if not url2:
            return
        if cs[1] in type_map:
            tc = type_map[cs[1]]
            if isinstance(tc, int):
                url2 = url2.replace('type%3D1%26', 'type%3D' + str(tc) + '%26')
            elif '_-_' in tc:
                url2 = url2.replace('&luicode=', tc + '&luicode=')
        return url2

    def list_page(self, response, **kwargs):
        r = response.r
        try:
            d = r.json()['data']
            for rd in self.extract_videos(d):
                yield rd
        except ValueError:
            import traceback
            log.error('weibo block? status:%s, url: %s, text: %s: %s', r.status_code, r.url, r.text,
                      traceback.format_exc())

    def list_container(self, response, **kwargs):
        cid = extract_between(response.url, '/p/', '?')
        url = 'https://m.weibo.cn/api/container/getIndex?jumpfrom=wapv4&tip=1&containerid=' + cid
        r = http_get(url, proxy=self.proxy)
        d = r.json()['data']
        for rd in self.extract_videos(d):
            yield rd

    def extract_user_page(self, target):
        if isinstance(target, string_types):
            response = self.get_response(target, explain_func=self.list_user)
        else:
            response = target
        r = response.r
        uid = extract_between(r.url, '/u/', '?')
        fid = extract_between(r.cookies['M_WEIBOCN_PARAMS'], 'fid%3D', '%26')
        r.cookies.set('SUB', SUB)
        url2 = 'https://m.weibo.cn/api/container/getIndex?jumpfrom=weibocom&type=uid&value=' + uid + '&containerid=' + fid
        return http_get(url2, proxy=self.proxy, cookies=r.cookies).json()['data']

    def list_user(self, response, **kwargs):
        d = self.extract_user_page(response)
        r = response.r
        uid = str(d['userInfo']['id'])
        if 'tabsInfo' not in d:
            # for rd in self.list_user_pc(uid, **kwargs):
            #     yield rd
            return
        ts = d['tabsInfo']['tabs']
        cid = None
        for t in ts:
            if t['tab_type'] == 'weibo':
                cid = t['containerid']
                break
        if not cid:
            # for rd in self.list_user_pc(uid, **kwargs):
            #     yield rd
            return
        else:
            since_id = None
            for pg in range(kwargs.get('page_count') or 1):
                log.info('page:%s, since_id:%s', pg, since_id)
                url2 = 'https://m.weibo.cn/api/container/getIndex?jumpfrom=weibocom&type=uid&value=' + uid + '&containerid=' + cid
                if since_id:
                    url2 += '&since_id=' + str(since_id)
                d = http_get(url2, proxy=self.proxy, cookies=r.cookies).json()['data']
                for rd in self.extract_videos(d):
                    yield rd
                since_id = d['cardlistInfo'].get('since_id')
                if not since_id:
                    log.info('no more pages')
                    break
    list_user.url_patterns = [r'https://weibo.com/u/(?P<user>\w+)', r'https://m.weibo.cn/u/(?P<user>\w+)']

    def list_user_pc(self, uid, **kwargs):
        url = 'https://weibo.com/' + uid
        r = http_get(url, proxy=self.proxy, mobile_mode=False, cookies=dict(SUB=SUB))
        pid = extract_between(r.text, "$CONFIG['page_id']='", "'")
        url = 'https://weibo.com/p/' + pid + '/photos?type=video#place'
        r = http_get(url, proxy=self.proxy, mobile_mode=False, cookies=dict(SUB=SUB))
        s = extract_between(r.text, 'photo_album_list', '<\\/ul>')
        if not s:
            return
        s = s.replace('\\n', '\n') \
            .replace('\\t', '\t') \
            .replace('\\', '')
        from xyz_embedmedia.helper import HtmlResponse
        from scrapy.utils.python import to_bytes
        res = HtmlResponse(url=r.url, encoding='utf-8', body=to_bytes(s, 'utf-8'))
        check_exists = kwargs.get('check_exists', lambda a: False)
        for d in res.css('li.photo_module'):
            a = d.css('a')[-1]
            aurl = a.css('::attr("href")').get()
            if 'weibo' not in aurl:
                continue
            try:
                r = http_get(aurl, proxy=self.proxy)
                ps = r.url.split('/')
                vid = ps[-1]
                durl = 'https://m.weibo.cn/detail/' + vid
                if check_exists(durl):
                    continue
                text = http_get(durl, proxy=self.proxy).text
                if 'var $render_data =' not in text:
                    continue
                vd = self.extract_default(text)
                if vd.get('embed_url'):
                    yield vd
            except:
                import traceback
                log.error('weibo list_user_pc %s %s error:%s', uid, aurl, traceback.format_exc())

    def extract_by_object_id(self, id):
        url = 'https://video.h5.weibo.cn/s/video/object?object_id=' + id
        d = http_get(url, proxy=self.proxy).json()['data']['object']
        rd = {}
        rd['cover'] = d['image']['url']
        stream = d['stream']
        if d.get('summary'):
            rd['name'] = html2text(d['summary'])
            rd['name'] = trim_name(rd['name'])
        rd['embed_url'] = stream['url']
        if stream.get('duration'):
            rd['duration'] = int(stream['duration'])
        rd['height'] = stream.get('height')
        rd['width'] = stream.get('width')
        if d.get('created_at'):
            rd['publish_time'] = int(
                time.mktime(datetime.strptime(d['created_at'], '%Y-%m-%d').timetuple()) * 1000)
        rd['detail'] = d
        rd['type'] = 'video'
        return rd


    def extract_user_info(self, url, func):
        if func == 'list_user':
            d = self.extract_user_page(url)['userInfo']
            return dict(
                url=d['profile_url'].split('?')[0],
                id=d['id'],
                name=d['screen_name'],
                description=d['description'],
                avatar=d['profile_image_url'],
                gender=d['gender'],
                detail=d
            )

