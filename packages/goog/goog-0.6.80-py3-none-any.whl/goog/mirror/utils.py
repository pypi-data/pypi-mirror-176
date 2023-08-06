from cloudscraper import create_scraper, User_Agent
from shutil import which
import random


JSONNET = True
NODEJS = True
if not which("node"):
    NODEJS = False
    try:
        import _jsonnet
    except:
        JSONNET = False
if not NODEJS and not JSONNET:
    raise ImportError("js object decoder is required (node.js or jsonnet)")


mirrors = [
    ["https", "lijianm.in"],
    ["https", "xgoogle.xyz"],
    # # ["http", "google.lyz810.com"],
    # ["https", "goo.gle.workers.dev"],
    ["https", "googlehnzyc.azurewebsites.net"],
    # ["https", "g20.i-research.edu.eu.org"],
    # ["http", "google.1qi777.com"],
    # ["https", "s.iit.xyz"],
    # ["https", "fsoufsou.com"],
    # ["https", "xn--flw351e.ml"],
    ["https", "shitu.paodekuaiweixinqun.com"],
]
'''
https://blog.csdn.net/lwdfzr/article/details/124805045


plaintext = "秋葉原冥途戰爭".encode()
iv = b"badassbadassbada"
ciphertext = AESCipherCBCnoHASHwoIV(key=iv, iv=iv).encrypt(plaintext)
from base64 import b64decode
print(plaintext, b64decode(ciphertext).hex())
'''
TBM = {
    "All": "",
    "Applications": "tbm=app",
    "Blogs": "tbm=blg",
    "Books": "tbm=bks",
    "Discussions": "tbm=dsc",
    "Images": "tbm=isch",
    "News": "tbm=nws",
    "Patents": "tbm=pts",
    "Places": "tbm=plcs",
    "Recipes": "tbm=rcp",
    "Shopping": "tbm=shop",
    "Videos": "tbm=vid",
}
search_url = "https://google.com/search?q={}"



def s():
    while True:
        try:
            s = create_scraper(browser={"mobile": False})
            return s
        except:
            continue


def random_mirror():
    # return mirrors[0]
    # return mirrors[1]
    # return mirrors[2] #
    # return mirrors[3]
    # return mirrors[4]
    # return mirrors[5] #
    # return mirrors[6]
    return random.SystemRandom().choice(mirrors)


def transform(url):
    proto, domain = random_mirror()
    url = url.split("/")
    url[0] = proto+":"
    url[2] = domain
    print("/".join(url))
    return "/".join(url)


def get(url, ss={}):
    url = transform(url)
    d = url.split("/")[2]
    if d not in ss:
        ss[d] = s()
    return ss[d].get(url)


def get_raw(url):
    return get(url).content


def post(url, data, ss={}):
    url = transform(url)
    d = url.split("/")[2]
    if d not in ss:
        ss[d] = s()
    return ss[d].post(url, data=data)


def post_raw(url, data):
    return post(url, data=data).content


def search(kw, cat="All", page=1, raw=True):
    # import time
    if cat not in TBM:
        raise KeyError(cat)
    url = search_url.format(kw)
    if cat in [
        "All",
    ]:
        url += "&start={}".format(10*(page-1))
    cat = TBM[cat]
    if cat:
        url += "&{}".format(cat)
    # st = time.time()
    if raw:
        r = get_raw(url)
    else:
        r = get(url)
    # print("_search", time.time()-st)
    return r




#
#
#
#
# def search_videos(kw, page=1, raw=True):
#     return search(kw, cat="Videos", page=page, raw=raw)
#
#
# def search_news(kw, page=1, raw=True):
#     return search(kw, cat="News", page=page, raw=raw)


