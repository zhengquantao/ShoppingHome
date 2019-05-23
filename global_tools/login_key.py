def proxy_urls():
    url = {
        "qq": "https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=101576925&redirect_uri=http://127.0.0.1:8000/login/qq&scope=get_user_info",
        "weibo": "https://api.weibo.com/oauth2/authorize?client_id=3214515364&redirect_uri=http://127.0.0.1:8000/login/weibo/",
        "weixin": "https://open.weixin.qq.com/connect/qrconnect?appid={}&redirect_uri={}&response_type={}&scope=snsapi_login&state=STATE#wechat_redirect"
    }
    return url
    

def weibo():
    client_id = 3214515364
    client_secret = "1b9b415350019674abfda80d0ef24cca"
    return client_id, client_secret


def qq():
    client_id = 101576925
    client_secret = '95bfd07354fcd7188507b8bea4ff679a'

    return client_id, client_secret


def weixin():
    client_id = 125
    client_secret = '4fsf4s6f46s4fs6'
    return client_id, client_secret