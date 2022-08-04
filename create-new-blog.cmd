set today=%date:~0,4%-%date:~5,2%-%date:~8,2%
set year=%date:~0,4%
set month=%date:~5,2%
set path=%~dp0source\_posts\%year%\%month%\

echo %path% in %today%


if not exist %path% md %path%


(echo ---
echo title: 
echo layout: info
echo commentable: true
echo date: %today%
echo mathjax: true
echo mermaid: true
echo tags: [Blog]
echo categories: Blog
echo description: 
echo ---)>%path%%today%-.md
