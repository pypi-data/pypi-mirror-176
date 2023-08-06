from .utils import search as _search
from subprocess import run, PIPE
from lxml import html, etree
import json
import time
import os


def search(kw, page=1):
    return _search(kw, cat="Images", page=page)


def parse(raw):
    from .utils import NODEJS, JSONNET
    r = html.fromstring(raw.decode())
    rs = [_ for _ in r.xpath("//script[contains(text(), 'AF_initDataCallback')]/text()")]
    if rs:
        r = max(rs, key=len)
        if NODEJS:
            open("tmp.js", "wb").write(("console.log(JSON.stringify("+str(r)[20:-2]+"));").encode())
            r = run("node tmp.js", stderr=PIPE, stdout=PIPE).stdout.decode()
            os.remove("tmp.js")
        elif JSONNET:
            import _jsonnet
            r = _jsonnet.evaluate_snippet("snippet", str(r)[20:-2])
        r = json.loads(r)
        return r["data"][56][1][0][0][1][0]
    else:
        r = [etree.tostring(_, method="html") for _ in r.xpath("//*[@data-ou]")]
        if not r:
            raise ValueError("raw is malformed, try to search and parse again")
        return r


def process(parsed):
    r = []
    if isinstance(parsed[0], bytes):
        for _ in parsed:
            _ = html.fromstring(_.decode())
            r.append([
                _.xpath("//div/@data-ru")[0],
                _.xpath("//div/@data-ou")[0],
            ])
    else:
        for i, _ in enumerate(parsed):
            _ = list(_[0][0].values())[0]
            imgs = []
            urls = []
            if not _[1]:
                continue
            for __ in _[1]:
                if isinstance(__, list):
                    imgs.append(__)
                elif isinstance(__, dict):
                    for ___ in __.values():
                        for ____ in ___:
                            if isinstance(____, str) and ____.startswith("http"):
                                urls.append(____)
            url = urls[0]
            img = imgs[-1][0]
            r.append([
                url,
                img
            ])
    return r


def get(**kwargs):
    for i in range(0, 5):
        try:
            # import time
            # st = time.time()
            # r = search(**kwargs)
            # print("search", time.time()-st)
            # st = time.time()
            # r = parse(r)
            # print("parse", time.time()-st)
            # st = time.time()
            # r = process(r)
            # print("process", time.time()-st)
            # return r
            return process(parse(search(**kwargs)))
        except Exception as e:
            if i == 4:
                raise e
            time.sleep(5)

