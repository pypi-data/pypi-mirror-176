# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import extract_between, urlencode, http_post
from xyz_embedmedia.decorators import register
from xyz_util.datautils import str2dict, access
import json

COOKIES = str2dict('shop_version_type=4; anony_token=4ac6afe149e44607784488692857ead3; xenbyfpfUnhLsdkZbX=0; dataUpJssdkCookie={"wxver":"","net":"","sid":""}; sensorsdata2015jssdkcross=%7B%22%24device_id%22%3A%2217fd885501a158-006fe930e2f573-1c3a645d-1296000-17fd885501b199%22%7D; sajssdk_2015_new_user_appf0l7cbhe2203_h5_xiaoeknow_com=1; ko_token=e780c5d65a137911e504a72e42006c5b; sa_jssdk_2015_appf0l7cbhe2203_h5_xiaoeknow_com=%7B%22distinct_id%22%3A%22u_6242dd5fbb315_FbplxpBfU4%22%2C%22first_id%22%3A%2217fd885501a158-006fe930e2f573-1c3a645d-1296000-17fd885501b199%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%7D; logintime=1648605338', key_spliter='=', line_spliter='; ')
@register()
class XiaoEKnow(Vendor):
    name = '小鹅通'
    sub_domains = ['xiaoeknow.com']
    type = 'video'
    test_urls = [
        'https://appf0l7cbhe2203.h5.xiaoeknow.com/v1/course/video/v_61874edfe4b077a2b35efd0d?type=2&pro_id=p_61874a2de4b02561a6ca330a&from_multi_course=1',
    ]

    def request_extra_params(self, f):
        d = super(XiaoEKnow, self).request_extra_params(f)
        d['cookies'] = COOKIES
        return d

    def explain_default(self, response):
        super(XiaoEKnow, self).explain_default(response)
        ps = response.url.split('?')
        vid = extract_between(ps[0], '/video/', '?')
        appid = extract_between(ps[0], '://', '.')
        params = str2dict(ps[1], key_spliter='=', line_spliter='&')
        s = {"pay_info":json.dumps({
                "type": "2",
                "product_id": params['pro_id'],
                "from_multi_course": params["from_multi_course"],
                "resource_id": vid,
                "resource_type": 3,
                "app_id": appid,
                "payment_type": ""
            })
        }
        d = urlencode(s)
        url = 'https://%s.h5.xiaoeknow.com/video/base_info' % appid
        r = http_post(url, data=d, extra_headers={'Content-Type': "application/x-www-form-urlencoded"}, cookies=COOKIES)
        self.data['embed_url'] = v['url']
        self.data['width'] = v['width']
        self.data['height'] = v['height']
        self.data['duration'] = v['duration']
        self.data['cover'] = access(d, 'cover.url')
        self.data['unique_id'] = v['id']
        self.data['data'] = d
