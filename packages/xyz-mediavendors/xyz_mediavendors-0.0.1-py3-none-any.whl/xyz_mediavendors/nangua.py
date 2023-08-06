# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import http_get, http_post, extract_between, json
from xyz_embedmedia.decorators import register
from xyz_util.datautils import str2dict


@register()
class ManGua(Vendor):
    name = '南瓜'
    sub_domains = 'vcinema.cn'
    type = 'video'
    test_urls = [
        'https://h5-common.vcinema.cn/movie/index.html?movie_id=25010&user_id=3242207&share_timestamp=1616205778747&encrypt_key=Je3s9%2BicvYpJ%2F6LvijBwLwqFC80%3D&phone=186****0981&share_key=MD6bfq7Lm%2BPY40CvNibYG4hxKXk%3D'
    ]

    def explain_default(self, response):
        super(ManGua, self).explain_default(response)
        # self.data['name'] = response.css('.video_name span::text').get()
        params = extract_between(response.url, '?', '\n')
        params = str2dict(params, '&', '=')
        d = dict(sign_key=params['encrypt_key'], user_id=params['user_id'], movie_id=params['movie_id'],
                 share_timestamp=params['share_timestamp'])
        url = 'https://o-api.vcinema.cn/v5.0/movie/get_share_movie_url?is_wap=1'
        r = http_post(url, data=d, referer='https://h5-common.vcinema.cn/',
                      extra_headers={'device_info': 'iPhone XR[ios_13.3.1_H5]', 'channel': 'wx1'})
        rd = r.json()
        self.data['embed_url'] = rd['content']['movie_url_list'][0]['media_url']
