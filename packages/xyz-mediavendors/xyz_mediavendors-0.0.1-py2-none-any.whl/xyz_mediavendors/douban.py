# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, json, http_get, html2text
from xyz_embedmedia.decorators import register
from xyz_util.datautils import str2dict
import time, random


@register()
class Douban(Vendor):
    name = '豆瓣电影'
    sub_domains = ['douban.com']
    type = 'video'
    test_urls = [
        'https://m.douban.com/movie/trailer/264997',
        'https://m.douban.com/movie/trailer/259258',
    ]

    def explain_default(self, response):
        if '/doubanapp/dispatch' in response.url:  # 此类页面， 厂商是用javascript跳转， 所以这里要进行url转换
            url = extract_between(response.text, "h5url : '", "'").replace('&amp;', '&')
            response = self.get_response(url, 'default')
        if '/movie/trailer/' not in response.url:
            super(Douban, self).explain_default(response)
            self.data['cover'] = response.css('.image-wrapper img[width]::attr(src)').get() or self.data.get('cover')
            return
        super(Douban, self).explain_default(response)
        self.data['name'] = response.css('p[class="trailer-title"]::text').get()
        self.data['cover'] = response.css('video::attr(poster)').get()
        self.data['embed_url'] = response.css('video source::attr(src)').get()
        self.data['description'] = response.css('header[class="trailer-hd"] a::text').get() \
                                   + ' ' + response.css('header[class="trailer-hd"] span::text').get()
        self.data['width'] = 414
        self.data['height'] = 233

    def list_movie_rank(self, response, **kwargs):
        tags = kwargs.get('tags', '电影')
        pstart = kwargs.get('page_start') or 0
        pend = kwargs.get('page_count') or 10
        for p in range(pstart, pend):
            url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=6,10&tags=' + tags + '&start=' + str(
                p * 20)
            for retry in range(5):
                d = http_get(url, proxy=self.proxy).json()
                if 'data' not in d:
                    print(d['msg'])
                    time.sleep(60)
                else:
                    break
            vl = d['data']
            print('page ', p)
            if not vl:
                return
            for vd in vl:
                d = dict(
                    name=vd['title'],
                    url=vd['url'],
                    cover=vd['cover'],
                    rate=vd["rate"],
                    star=vd['star'],
                    rank_page=p
                )
                yield d
            if p < pend - 1:
                time.sleep(random.randint(10, 20))

    def explain_movie(self, response):
        t = extract_between(response.text, '<script type="application/ld+json">', '</script>')
        d = json.loads(t.replace('\n', ' ').replace('\t', ' ').replace('\r', ' '))
        html = '\n'.join(response.css('#info').getall())
        d['detail'] = str2dict(html2text(html))
        desc = response.css('span[property="v:summary"]::text').get()
        roles = []
        for a in response.css('.celebrities-list .celebrity'):
            actor = a.css('.name::text').get()
            role = a.css('.role::text').get()
            if not role:
                continue
            if role.startswith('饰 '):
                roles.append(dict(actor=actor, name=role[2:]))
        d['role'] = roles
        d['description'] = desc and desc.strip()
        return d

    def get_movie_gallery(self, movie_url):
        sid = extract_between(movie_url, '/subject/', '/')
        url = 'https://movie.douban.com/subject/' + sid + '/photos?type=S'
        response = ScrapyResponse(url, proxy=self.proxy, mobile_mode=False)
        for c in response.css('.article li'):
            curl = c.css('.cover img::attr(src)').get()
            size = c.css('.prop::text').get().strip()
            yield dict(url=curl, size=size)

    def list_music_rank(self, response, **kwargs):
        tag = kwargs.get('tag')
        url = 'https://music.douban.com/tag/%s' % tag
        response = ScrapyResponse(url)
        for tr in response.css('tr.item'):
            name = tr.css('.pl2 a::text').getall()
            img = tr.css('img::attr(src)').get()
            url = tr.css('.pl2 a::attr(href)').get()
            author, publish_date, type, material, form = tr.css('p.pl::text').get().split(' / ')
            d = dict(
                url=url,

            )
