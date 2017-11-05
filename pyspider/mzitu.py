#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-11-05 11:35:50
# Project: test
# Author: wyq

from pyspider.libs.base_handler import *
import re

DIR_PATH = '/home/wyq/python/Pyspider'

class Handler(BaseHandler):
    crawl_config = {
        'headers' : {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
            'Connection': 'Keep-Alive',
            'Referer': 'http://www.mzitu.com/',
        }
    }

    def __init__(self):
        self.root_url = 'http://www.mzitu.com/all/'
        self.deal = Deal()

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(self.root_url, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        # 获取套图url
        for each in response.doc('a[href^="http"]').items():
            if re.match('http://www.mzitu.com/\d.*$', each.attr.href):
                self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        # 获取当前页面图片
        for each in response.doc('p img').items():
            img_url = each.attr.src
        # 获取下一页url
        for each in response.doc('.pagenavi > a:last-child').items():
            self.crawl(each.attr.href, callback=self.detail_page)

        split_url = img_url.split('/')
        dir_name = split_url[-3] + '/' + split_url[-2]
        dir_path = self.deal.mkDir(dir_name)
        file_name = split_url[-1]
        self.crawl_config['headers']['Referer'] = response.url
        self.crawl(img_url, callback=self.save_img, save={'dir_path': dir_path, 'file_name': file_name})

        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }

    # 保存图片
    def save_img(self, response):
        content = response.content
        dir_path = response.save['dir_path']
        file_name = response.save['file_name']
        file_path = dir_path + '/' + file_name
        self.deal.saveImg(content, file_path)


import os


class Deal:
    def __init__(self):
        self.path = DIR_PATH
        if not self.path.endswith('/'):
            self.path = self.path + '/'
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def mkDir(self, path):
        path = path.strip()
        dir_path = self.path + path
        exists = os.path.exists(dir_path)
        if not exists:
            os.makedirs(dir_path)
            return dir_path
        else:
            return dir_path

    def saveImg(self, content, path):
        f = open(path, 'wb')
        f.write(content)
        f.close()

    def saveBrief(self, content, dir_path, name):
        file_name = dir_path + "/" + name + ".txt"
        f = open(file_name, "w+")
        f.write(content.encode('utf-8'))

    def getExtension(self, url):
        extension = url.split('.')[-1]
        return extension