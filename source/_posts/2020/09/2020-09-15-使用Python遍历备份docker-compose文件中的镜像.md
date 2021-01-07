---
title: 使用Python遍历备份docker-compose文件中的镜像
layout: info
commentable: true
date: 2020-09-15
mathjax: true
mermaid: true
tags: [Python,Docker]
categories: 
- [Python]
- [Container,Docker]
description: 
---

Python 脚本如下：

```python
import os

def get_images():
    file = open("docker-compose.yml") 
    images = []
    for line in file.readlines():  
         line = line.strip('\n')  
         if "image" in line:
             image = line.replace("image:","").strip()
             images.append(image)
    return images

def pull_images():
    images = get_images()
    for image in images:
        pull_commond = "docker pull " + image
        print(pull_commond)
        os.system(pull_commond)

def save_imaegs():
    images = get_images()
    for image in images:
        sub_name = image.split("/")[-1].replace(":","_") + ".tar"
        if os.path.exists(sub_name):
            print(sub_name,'is exists!')
        else:
            save_commond = "docker save " + image + " -o " + sub_name
            print(save_commond)
            os.system(save_commond)

def load_images():
    files = os.listdir(".")
    for file in files:
        if ".tar" in file:
            print(file)
            load_commond = "docker load -i " + file
            print(load_commond)
            os.system(load_commond)

def start_deal(num):
    if num == 1:
        pull_images()
    elif num == 2:
        save_imaegs()
    elif num == 3:
        load_images()

if __name__=="__main__":
    start_deal(1)
    
```

