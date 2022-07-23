#! /bin/bash


python3 .\source\bin\move-blog-images.py

today=`date +%Y-%m-%d`

git add .
git commit -m update_$today
git push origin master

pause