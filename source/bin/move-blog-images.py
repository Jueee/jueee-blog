#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil
import sys
import datetime
from dateutil.relativedelta import relativedelta


def getBlogAddress(BLOG_PATH):
    blogs = []
    for root, dirs, files in os.walk(BLOG_PATH):
        for f in files:
            if not f.startswith(THIS_MONTH):
                continue
            filename = os.path.join(root, f)
            blogs.append(filename)
    return blogs


def getImages(path):
    images = []
    for root, dirs, files in os.walk(path):
        for f in files:
            images.append(f)
    if len(images) > 0:
        print(images)
    return images


def replaceFile(file, old_str, new_str):
    file_data = ""
    try:
        with open(file, "r", encoding="UTF-8") as f:
            for line in f:
                if old_str in line:
                    line = line.replace(old_str, new_str)
                file_data += line
        with open(file, "w", encoding="utf-8") as f:
            f.write(file_data)
    except Exception as e:
        print('ERROR:'+file)


def replaceBolgs(blogs, YEAR_NUM, MONTH_NUM):
    for blog in blogs:
        replaceFile(blog, "assets/", "/images/"+YEAR_NUM+"/"+MONTH_NUM+"/")


def moveImages(month):
    YEAR_NUM = month.split("-")[0]
    MONTH_NUM = month.split("-")[1]
    BLOG_PATH = os.path.dirname(
        __file__)+"/../_posts"+"/"+YEAR_NUM+"/"+MONTH_NUM
    OLD_IMAGES_PATH = BLOG_PATH+"/"+"assets/"
    NEW_IMAGES_PATH = os.path.dirname(
        __file__)+"/../images/"+YEAR_NUM+"/"+MONTH_NUM+"/"
    blogs = getBlogAddress(BLOG_PATH)
    replaceBolgs(blogs, YEAR_NUM, MONTH_NUM)
    if not os.path.exists(NEW_IMAGES_PATH):
        os.makedirs(NEW_IMAGES_PATH)
        print("new mkdir:"+NEW_IMAGES_PATH)
    for image in getImages(OLD_IMAGES_PATH):
        full_path = OLD_IMAGES_PATH+image
        despath = NEW_IMAGES_PATH+image
        shutil.move(full_path, despath)
        print(full_path, " -> ", despath)
    if os.path.exists(OLD_IMAGES_PATH):
        os.rmdir(OLD_IMAGES_PATH)
        print('rmdir:'+OLD_IMAGES_PATH)


if __name__ == '__main__':
    today = datetime.datetime.today()
    THIS_MONTH = today.strftime('%Y-%m')
    if len(sys.argv) > 1:
        monthParam = sys.argv[1]
        if monthParam is not None:
            print("monthParam:", monthParam)
            THIS_MONTH = monthParam
            moveImages(THIS_MONTH)
    else:
        time = datetime.datetime(year=2020, month=6, day=1)
        for n in range(1000):
            result_date = time + relativedelta(months=n)
            res_month = result_date.strftime('%Y-%m')
            moveImages(res_month)
            if res_month == THIS_MONTH:
                break
