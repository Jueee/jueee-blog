set backtime=`date +%Y-%m-%d~%H:%M:%S`
git add .
git commit -m update_%date +%Y-%m-%d~%H:%M:%S%
git push origin master

pause