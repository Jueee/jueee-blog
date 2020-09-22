import os,re,shutil,sys
import fileinput

def getBlogAddress():
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
    print(images)
    return images

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
        #replaceFile(blog,"/assets/images/","/images/")
        #replaceFile(blog,"mathjax: false","mathjax: false")
        replaceFile(blog,"assets/1","/images/"+YEAR_NUM+"/"+MONTH_NUM+"/1")
        replaceFile(blog,"assets/image-","/images/"+YEAR_NUM+"/"+MONTH_NUM+"/image-")

def moveImages():
    if not os.path.exists(NEW_IMAGES_PATH):
        os.mkdir(NEW_IMAGES_PATH)
        print("new mkdir:"+NEW_IMAGES_PATH)
    for image in getImages(OLD_IMAGES_PATH):
        full_path = OLD_IMAGES_PATH+image
        despath = NEW_IMAGES_PATH+image
        shutil.move(full_path, despath)
        print(full_path," -> ",despath)
    if os.path.exists(OLD_IMAGES_PATH):
        os.rmdir(OLD_IMAGES_PATH)
        print('rmdir:'+OLD_IMAGES_PATH)

if __name__ == '__main__':
    THIS_MONTH="2020-08"
    if len(sys.argv) > 1:
        monthParam = sys.argv[1]
        if monthParam is not None:
            print("monthParam:",monthParam)
            THIS_MONTH = monthParam
    YEAR_NUM=THIS_MONTH.split("-")[0]
    MONTH_NUM=THIS_MONTH.split("-")[1]
    BLOG_PATH = os.path.dirname(__file__)+"/../_posts"+"/"+YEAR_NUM+"/"+MONTH_NUM
    OLD_IMAGES_PATH = BLOG_PATH+"/"+"assets/"
    NEW_IMAGES_PATH= os.path.dirname(__file__)+"/../images/"+YEAR_NUM+"/"+MONTH_NUM+"/"
    blogs = getBlogAddress()   
    replaceBolgs(blogs)
    moveImages()