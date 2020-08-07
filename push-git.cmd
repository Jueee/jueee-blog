backtime=`date +%Y%m%d%H%M%S`
git add .
git commit -m update_${backtime}
git push origin master

pause