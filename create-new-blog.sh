#! /bin/bash

today=`date +%Y-%m-%d`
path=./source/_posts/`date +%Y/%m/`

echo $path in $today 

#shell判断文件夹是否存在 
#如果文件夹不存在，创建文件夹
if [ ! -d $path ]; then
  mkdir $path
fi



(echo ---
echo title: 
echo layout: info
echo commentable: true
echo date: $today
echo mathjax: true
echo mermaid: true
echo tags: [Blog]
echo categories: Blog
echo description: 
echo ---)>$path$today-.md