---
title: ElementUI实现文件上传下载
layout: info
commentable: true
date: 2021-05-17
mathjax: true
mermaid: true
tags: [Vue,ElementUI]
categories: Vue
description: 
---

通过 ElementUI实现文件上传下载。

<!--more-->

### 文件下载

#### ElementUI

```html
<el-button icon="el-icon-download" @click="downJson" >导出</el-button>
```

#### Vue

```js
downJson() {
    var $this = this;
    const res = axios
    .request({
        url: "/exportJson",
        method: "post",
        responseType: "blob"
    })
    .then(res => {
        const data = res.data;
        let url = window.URL.createObjectURL(data); // 将二进制文件转化为可访问的账号
        var a = document.createElement("a");
        document.body.appendChild(a);
        a.href = url;
        a.download = "XXX.json";
        a.click();
        window.URL.revokeObjectURL(URL);
    });
}, 
```

#### Java接口

```java
@PostMapping("/exportJson")
public void exportJson(HttpServletResponse response) {
    List<Object> infos = service.findAll();
    try {
        ByteArrayOutputStream os = new ByteArrayOutputStream();
        JSONArray jsonArray = JSONArray.parseArray(JSON.toJSONString(infos));
        os.write(jsonArray.toString().getBytes("UTF-8"));
        byte[] content = os.toByteArray();
        InputStream is = new ByteArrayInputStream(content);
        IOUtils.copy(is, response.getOutputStream());
        response.flushBuffer();
    }catch (Exception e){
        log.error(e.getMessage(),e);
    }
}
```

### 文件上传

#### ElementUI

```html
<el-dialog title="上传" :visible.sync="uploadDialogVisible" width="40%" @close="closeUploadDialog">
    <span>
        <el-row>
            	<el-upload
                       class="upload-demo"
                       :auto-upload="false"
                       multiple
                       action
                       :file-list="uploadFileList"
                       :on-change="uploadFileChange"
                       :limit="1">
                <el-button size="small" type="primary">点击上传</el-button>
                <div slot="tip" class="el-upload__tip">只能上传 json 文件，且不超过500kb</div>
            </el-upload>
        </el-row>
    </span>
    <span slot="footer" class="dialog-footer">
        <el-button @click="uploadDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="uploadJson" :disabled="btnDisabled" :loading="btnLoading">确 定</el-button>
    </span>
</el-dialog>
```

注：action属性必须存在，可以为空值。

#### Vue

```js
data() {
    return {
      uploadDialogVisible: false, //添加弹框是否显示
      uploadFileList: []
    }
},
methods: {
    uploadFileChange (file, fileList) {
      this.uploadFileList = fileList;
    },
    uploadJson: async function(){
      let config = {
          headers: {
            'Content-Type': 'multipart/form-data;'
          }
        };
      let letdata = new FormData();
      letdata.append("file", this.uploadFileList[0].raw);
      const {data: res} = await this.$http.post(
              "/uploadJson",
              letdata,config
      );
      if (res.code === 200) {
        this.$message.success("上传成功");
        this.uploadDialogVisible=false
        this.getmetaInfoFeatureList();
      } else {
        return this.$message.error("上传失败:" + res.msg);
      }
    }
}
```

必须使用 `new FormData()` 提交 form 表单，同时携带 `Content-Type` 头信息。

否则加请求头报 no multipart boundary was found，删掉又报 Current request is not a multipart request。

没有设置 boundary 边界，正确的消息头应该是 `'Content-Type':'multipart/form-data;boundary='+随机数`。

如下图所示：

![image-20210518190117832](/images/2021/05/image-20210518190117832.png)

#### Java 接口

```java
@PostMapping("/uploadJson")
@ResponseBody
public ResponseBean uploadJson(@RequestParam(value = "file") MultipartFile file) {
    log.info(file.getOriginalFilename());
    log.info("size:"+file.getSize());
    return ResponseBean.success();
}
```

### 跨域配置

解决跨域上传文件：

```java
@Configuration
public class CrosConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")
                .allowedOrigins("*")
                .allowedMethods("GET", "HEAD", "POST", "PUT", "DELETE", "OPTIONS")
                .allowCredentials(true) //这两句不加不能跨域上传文件，
                .maxAge(3600)   //加上去就可以了
                .allowedHeaders("*");
    }
}
```