# -*- coding: utf-8 -*-

import requests

from django.http import HttpResponseRedirect, HttpResponseForbidden

OAUTH_BASE_URL = ('https://open.weixin.qq.com/connect/oauth2/authorize?'
                  'appid=%(appid)s&redirect_uri=%(redirect_uri)s'
                  '&response_type=%(response_type)s&scope=%(scope)s&state=%(state)s#wechat_redirect')

EXCHANGE_CODE_FOR_TOKEN_URL = ('https://api.weixin.qq.com/sns/oauth2/'
                               'access_token?appid=%(appid)s&'
                               'secret=%(secret)s&code=%(code)s&'
                               'grant_type=authorization_code')

# WX_DOMAIN = 'http://txu3.sinaapp.com'
# WX_APPID = 'wxc63a79dda7df462b'
# WX_SECRET = '85a55db4fe834c9fdfdfce0128e4e9fe'

WX_DOMAIN = 'http://127.0.0.1'
WX_APPID = 'wx3d4d26f36a9e8f47'
WX_SECRET = '67ab0eb8ae4cb61a5bf31ccdbea3f836'


def _build_oauth_scope_url(request, scope):
    return OAUTH_BASE_URL % {
        'appid': WX_APPID,
        'response_type': 'code',
        'redirect_uri': '%s%s?%s' % (WX_DOMAIN,
                                     request.path, request.META['QUERY_STRING']),
        'scope': scope,
        'state': scope}


def _build_source_url(request):
    source_keys = set(request.GET.keys()) - set(['code', 'state'])
    query_keys = ['%s=%s' % (key, request.GET.get(key)) for key in source_keys]
    query_string = '&'.join(query_keys)
    return '%s%s?%s' % (WX_DOMAIN, request.path,
                        query_string)


def _bind_request_info(request, code, state):
    url = EXCHANGE_CODE_FOR_TOKEN_URL % {
        'appid': WX_APPID,
        'secret': WX_SECRET,
        'code': code}
    ret = requests.get(url, verify=False).json()
    try:
        openid = ret['openid']
        access_token = ret['access_token']
    except Exception as e:
        return None

    request.session['wx_open_id'] = openid

    if state == 'snsapi_userinfo':

        REQUEST_USERINFO_URL = ('http://api.weixin.qq.com/sns/userinfo?'
                                'access_token=%(access_token)s&openid=%(openid)s'
                                '&lang=%(lang)s')
        """
        get info from weixin:
            {"openid":" OPENID",
             "nickname": NICKNAME,
             "sex":"1",
             "province":"PROVINCE"
             "city":"CITY",
             "country":"COUNTRY",
             "headimgurl": head img url like "http://XXXXXXXX"
             "privilege":["PRIVILEGE1", "PRIVILEGE2"]
            }
        """

        url = REQUEST_USERINFO_URL % {
            'access_token': access_token,
            'openid': openid,
            'lang': 'zh_CN'}

        r = requests.get(url)
        r.encoding = 'utf-8'
        user_info = r.json()

        print user_info
        print user_info.get('nickname')

    return openid


def need_wechat_oauth_login_if_open_in_wechat():
    def wrapper(func):
        def decorator(request, *args, **kwargs):
            ua = request.META.get('HTTP_USER_AGENT', '')
            if 'MicroMessenger' in ua:
                # TODO: protect openid in session
                wx_open_id = request.session.get('wx_open_id', None)
                state = request.GET.get('state', None)
                code = request.GET.get('code', None)

                print '======================================'
                print wx_open_id, state, code

                # pre login check
                if not wx_open_id and not state:
                    return HttpResponseRedirect(_build_oauth_scope_url(request, 'snsapi_base'))

                # oauth login status check
                if state and not code:
                    # cancel to confirm oauth
                    return HttpResponseForbidden()
                elif state and code:
                    wx_open_id = _bind_request_info(request, code, state)

                print '-----------------'
                print wx_open_id

                # check oauth require type
                return HttpResponseRedirect(_build_oauth_scope_url(request, 'snsapi_userinfo'))
            else:
                return func(request, *args, **kwargs)

        return decorator
    return wrapper
