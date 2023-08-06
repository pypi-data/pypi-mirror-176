# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_embedmedia.vendor import Vendor
from xyz_embedmedia.helper import ScrapyResponse, extract_between, json
from xyz_embedmedia.decorators import register
from xyz_util.datautils import str2dict
@register()
class MangoTV(Vendor):
    name = '芒果TV'
    sub_domains = ['mgtv.com']
    type = 'video'
    test_urls = [
        'https://m.mgtv.com/b/338481/9708940.html?fpa=hotpage&fpa=4&fpt=1&lastp=v_play&ftl=1',
        'https://m.mgtv.com/b/338497/8437644.html?t=videoshare'
    ]
    
    def get_response(self, url, explain_func=None):
        url = url.replace('/l/', '/b/')
        return super(MangoTV, self).get_response(url, explain_func=explain_func)

    def explain_default(self, response):
        super(MangoTV, self).explain_default(response)
        id = response.url.split('.html')[0].split('/')[-1]
        s = extract_between(response.text, '<script>window.__INITIAL_STATE__=', '</script>')
        d = json.loads(s)['playPage']
        v = d['videoinfo']
        self.data['name'] = v['title']
        self.data['cover'] = v['image']
        self.data['description'] = v['description']
        self.data['duration'] = v['time']
        url2 = "https://v5m.api.mgtv.com/remaster/uc/v0/getSource?did=8741f771-9902-41a8-8dba-48a7cb08543f&suuid=E57F2576-AD1B-48A9-8303-077AE96C14BA&t=1598432609548&abroad=0&partId=%s&clipId=338497&plId=0&pm2=9tvX8_nUwAw0z2VFkZEv5TSyFU5BTXNpUvWuxbTPthnCM6O_WMkGGi5jZSd_raBMeAbF2bf9ER3bMUucUBmvViw3uvhL8X35CWkoQMd2ir0JWZrkuZ5Tz9ucAGsY7pZbf6o0H7OusH70SBf6etcyqlx6IR8jvu0KrB7OiW8WVfyWwW7upoj8nkS7fIXPTw7_RC20u9uyrfGySj4M1UmKDh~x_tCYEYZ~RYaUxB6GbcMSDeFV44ywIvuL5i0Pmu81&tk2=5AjNyMDN4kTNx0Ddpx2Y&_support=10000000&callback=jsonp_3fhca4775x08vvs" % id
        cookies = str2dict('locale=CHN; _source_=B; __STKUUID=356ba34f-48a6-429c-9bd9-e5ffc8933c22; PLANB_FREQUENCY=X0YgrEAgZQ_MF-c0; MQGUID=1298541000721158144; __MQGUID=1298541000721158144; mba_deviceid=23d9bc13-2c21-dba9-4e23-69cb6c052582; pc_v6=v6; PM_CHKID=098f2c55291040b0; mg_uuid=8741f771-9902-41a8-8dba-48a7cb08543f; fcid=001e1fdfba814e9f82769ca7b6e12790;', ';', '=')
        r = ScrapyResponse(url2, cookies=cookies)
        # print url2, r.text
        s = r.text[len('jsonp_3fhca4775x08vvs('):-1]
        d2 = json.loads(s)['data']['stream']
        url3 = "%s%s" % (d2['retryUrl'][0], d2['mp4Url'][0])
        r3 = ScrapyResponse(url3, cookies=cookies)
        # print r3.text
        d3 = json.loads(r3.text)
        self.data['embed_url'] = d3['info']
        self.data['detail'] = v
        self.data['width'] = 414
        self.data['height'] = 233
