set today=%date:~0,4%-%date:~5,2%-%date:~8,2%

(echo ---
echo title: 
echo layout: info
echo commentable: true
echo date: %today%
echo mathjax: true
echo mermaid: true
echo tags: [Blog,HTML]
echo categories: Blog
echo description: 
echo ---)>%today%-.md