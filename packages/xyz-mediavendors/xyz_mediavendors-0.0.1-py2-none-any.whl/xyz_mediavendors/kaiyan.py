# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals

from xyz_embedmedia.decorators import register
from xyz_embedmedia.helper import extract_between, http_get
from xyz_embedmedia.vendor import Vendor
from xyz_util.datautils import str2dict
import logging

log = logging.getLogger('django')

CATEGORY_MAP = str2dict("""广告	广告
剧情	电影百科
运动	健身
创意	职场
旅行	旅行
影视	电影百科
记录	纪录片
音乐	音乐百科
科技	测评
开胃	美食
游戏	游戏百科
动画	动画电影
搞笑	搞笑
时尚	时尚百科
生活	生活
综艺	综艺百科
萌宠	萌宠""", key_spliter='\t')


@register()
class KaiYan(Vendor):
    name = '开眼'
    sub_domains = ['eyepetizer.net', 'kaiyanapp.com']
    type = 'video'
    test_urls = [
        'https://www.eyepetizer.net/detail.html?vid=209704',
    ]

    def explain_default(self, response):
        super(KaiYan, self).explain_default(response)
        id = self.extract_id(response)
        self.data.update(self.extract_video(id))

    def extract_id(self, target):
        if isinstance(target, int):
            id = target
        elif 'video_id=' in target.url:
            id = extract_between(target.url, 'video_id=', '&')
        else:
            id = extract_between(target.url, 'vid=', '&')
        return id

    def extract_video(self, id):
        url = 'https://baobab.kaiyanapp.com/api/v1/video/%s?f=web' % id
        r = http_get(url)
        if r.text.startswith('"Cannot find resource'):
            raise LookupError('404')
        d = r.json()
        d.pop('tags', None)
        return dict(
            name=d.get('title'),
            description=d.get('description'),
            duration=d.get('duration'),
            embed_url=d.get('playUrl'),
            detail=d,
            unique_id=d.get('id'),
            like_count=d['consumption']['collectionCount'],
            publish_time=d.get('releaseTime'),
            cover=d.get('coverForFeed')
        )

    def category2subject(self, c):
        return CATEGORY_MAP.get(c)

    def list_item(self, response, **kwargs):
        target = int(self.extract_id(response))
        log.info('kaiyan list_item from: %s', target)
        ec = 0
        for i in range(kwargs.get('page_count') or 100):
            try:
                d = self.extract_video(target)
                ec = 0
            except LookupError:
                ec += 1
                if ec > 20:
                    return
                target = target + 1
                log.warn('kaiyan list_item lookupError: %s', target)
                continue
            detail = d['detail']
            id = detail['id']
            d['type'] = 'video'
            d['url'] = 'https://www.eyepetizer.net/detail.html?vid=%s' % id
            subject = self.category2subject(detail['category'])
            if subject:
                d['subject'] = subject
                yield d
            target = id + 1
