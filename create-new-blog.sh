#! /bin/bash

today=`date +%Y-%m-%d`
path=./source/_posts/`date +%Y/%m/`

echo $path in $today 

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