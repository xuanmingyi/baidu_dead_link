#!/usr/bin/env python
# coding=utf8

import urllib2
import sys
import re


base_url = "http://www.baidu.com/s?wd=site%3A"


def get_page_count(url):
    html = urllib2.urlopen(url).read()
    pages = re.findall(r"<span class=\"pc\">\w</span>", html)
    if pages:
        return len(pages)
    return 0


def get_page_urls(url):
    urls = []
    html = urllib2.urlopen(url).read()
    regex = re.compile(r"href = \"(http://www.baidu.com/link\?url=[\S|-|_]*)\"")
    urls = regex.findall(html)
    return urls


def test_url(url):
    try:
        f = urllib2.urlopen(url)
    except urllib2.URLError as e:
        return e.code, e.url
    return f.code, f.url


def build_xml(urls):
    xml = """<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">"""
    for url in urls:
        xml += "<url><loc>{0}</loc></url>".format(url)
    xml += "</urlset>"
    return xml


def main():
    if len(sys.argv) != 2:
        return 1
    urls = []
    dead_links = []
    for i in range(get_page_count(base_url + sys.argv[1])):
        url = base_url + sys.argv[1] + "&pn={0}".format(i * 10)
        urls.extend(get_page_urls(url))

    for url in urls:
        code, forward_url = test_url(url)
        if code == 404:
            dead_links.append(forward_url)

    print build_xml(list(set(dead_links)))

if __name__ == "__main__":
    main()
