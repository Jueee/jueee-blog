---
title: Excel文件导入导出工具ExcelKit
layout: info
commentable: true
date: 2020-11-25
mathjax: true
mermaid: true
tags: [Java,JavaJar,Excel]
categories: [Java,JavaJar]
description: 
---

### ExcelKit 介绍

ExcelKit 是简单、好用且轻量级的海量Excel文件导入导出解决方案。

- GitHub：https://github.com/wenzewoo/ExcelKit
- Gitee：https://gitee.com/wuwenze/ExcelKit/

<!--more-->

#### ExcelKit 引入

```xml
<dependency>
    <groupId>com.wuwenze</groupId>
    <artifactId>ExcelKit</artifactId>
    <version>2.0.72</version>
</dependency>
```

### ExcelKit 示例

#### ExcelMapping 

ExcelMapping (配置Excel与实体之间的映射关系)

```java
@Data
@Excel("user")
@Table(name = "tb_user")
public class User {
    @Id
    @ExcelField(value = "编号", width = 50)
    private Long id;

    @ExcelField(value = "用户名", width = 100)
    private String username;

    @ExcelField(value = "昵称", width = 100)
    private String nickname;

    @ExcelField(value = "邮箱", width = 150)
    private String email;

    @ExcelField(value = "电话号码", width = 100)
    private String phoneNumber;

    private Integer status;

    @ExcelField(value = "创建时间", dateFormat = "yyyy年MM月dd日 HH:mm:ss", width = 180)
    private Date createTime;

    @ExcelField(value = "修改时间", dateFormat = "yyyy年MM月dd日 HH:mm:ss",width = 180)
    private Date modifiedTime;

    @ExcelField(//
            value = "性别",
            readConverterExp = "男=1,女=0",
            writeConverterExp = "1=男,0=女"
            ,width = 50
    )
    private Integer sex;

    @ExcelField(value = "密码盐值", width = 100)
    private String salt;

    @ExcelField(//
            value = "用户类型",
            readConverterExp = "超级管理员=0,普通用户=1",
            writeConverterExp = "0=超级管理员,1=普通用户"
            ,width = 80
    )
    private Integer type;

    @ExcelField(value = "用户密码", width = 100)
    private String password;

    @ExcelField(value = "出生日期", dateFormat = "yyyy/MM/dd",width = 100)
    private Date birth;

    private Long departmentId;

    @ExcelField(value = "头像url", width = 200)
    private String avatar;

    private Integer is_corp;
}
```

#### 下载 Controller

使用 ExcelKit 提供的API 构建导入模板, 会根据配置生成批注, 下拉框等

```java
@RestController
@RequestMapping("/user")
@Slf4j
public class UserController {

    @Autowired
    private UserService userService;
    
    @PostMapping("/excel")
    public void export(HttpServletResponse response) {
        List<User> users = this.userService.findAll();
        ExcelKit.$Export(User.class, response).downXlsx(users, false);
    }
}
```

#### 下载 HEML

```html
<el-button @click="downExcel" icon="el-icon-download">导出</el-button>
```

#### 下载 Script

```javascript
downExcel() {
    var $this = this;
    const res = axios
    .request({
        url: "/user/excel",
        method: "post",
        responseType: "blob"
    })
    .then(res => {
        if (res.headers["content-type"] === "application/json") {
            return $this.$message.error(
                "Subject does not have permission [user:export]"
            );
        }
        const data = res.data;
        let url = window.URL.createObjectURL(data); // 将二进制文件转化为可访问的url
        var a = document.createElement("a");
        document.body.appendChild(a);
        a.href = url;
        a.download = "用户列表.xls";
        a.click();
        window.URL.revokeObjectURL(url);
    });
}
```

#### 下载效果

下载文件：

![image-20201124114137155](/images/2020/11/image-20201124114137155.png)

打开效果：

![image-20201124114254144](/images/2020/11/image-20201124114254144.png)