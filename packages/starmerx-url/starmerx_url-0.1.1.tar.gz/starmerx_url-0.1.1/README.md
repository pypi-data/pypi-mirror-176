# 1、INSTALLED_APPS添加
    'starmerx_url',
# 2、MIDDLEWARE添加
    'starmerx_url.AuthEffectMiddleware',
# 3、settings添加
    WHIIT_URL_LIST = ["/order/record/11314900/"]
    REMOTE_ADDR_REAL = ["118.191.129.34"]
    REFERER_HOST = ".starmerx.com"