import os,re,shutil
import fileinput

BLOG_PATH = os.path.dirname(__file__)+"/../_posts"

def getBlogAddress():
    blogs = []
    for root, dirs, files in os.walk(BLOG_PATH):
        for f in files:
            if not f.endswith('.md'):
                continue
            filename = os.path.join(root, f)
            print(filename)
            blogs.append(filename)
    return blogs

def replaceFile(file,old_str,new_str):
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str,new_str)
            file_data += line
    with open(file,"w",encoding="utf-8") as f:
        f.write(file_data)

def replaceBolgs(blogs):
    for blog in blogs:
        
        #replaceFile(blog,"categories: [Java,Java诊断,Arthas]","categories: [Java,Arthas]")
        replaceFile(blog,"[Windows,软件]","软件")
        #replaceFile(blog,"assets/1","/images/"+YEAR_NUM+"/"+MONTH_NUM+"/1")

if __name__ == '__main__':
    blogs = getBlogAddress()   
    replaceBolgs(blogs)