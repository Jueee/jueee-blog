---
title: 纯前端实现支持多Sheet 的 Excel 导出
layout: info
commentable: true
date: 2021-12-23
mathjax: true
mermaid: true
tags: [Vue]
categories: Vue 
description: 
---

实现纯前端的 Excel 导出(支持多 sheet)。

### SheetJS

- GitHub：https://github.com/SheetJS/sheetjs
- 官网：https://sheetjs.com/
- 下载：https://www.cdnpkg.com/xlsx/file/xlsx.core.min.js/?id=78603

<!--more-->

### HTML+JS 导出

依赖：

```html
<script src="https://unpkg.com/xlsx/dist/xlsx.core.min.js"></script>
```

样例：

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>展示 用xlsx库 导出excel，含多个sheet</title>
  </head>
  <body>
    <h1>展示 用xlsx库 导出excel，含多个sheet</h1>

    <button id="export" style="padding:20px;background: #69f;color:#fff;" onclick="downloadExcel()"> 导出excel</button>
   
    <script src="https://unpkg.com/xlsx/dist/xlsx.core.min.js"></script>
	
    <script>
      // 将workbook装化成blob对象
     function workbook2blob(workbook) {
         // 生成excel的配置项
         var wopts = {
             // 要生成的文件类型
             bookType: "xlsx",
             // // 是否生成Shared String Table，官方解释是，如果开启生成速度会下降，但在低版本IOS设备上有更好的兼容性
             bookSST: false,
             type: "binary"
         };
         var wbout = XLSX.write(workbook, wopts);
         // 将字符串转ArrayBuffer
        
         var blob = new Blob([s2ab(wbout)], {
             type: "application/octet-stream"
         });
         return blob;
     }
     function s2ab(s) {
         var buf = new ArrayBuffer(s.length);
         var view = new Uint8Array(buf);
         for (var i = 0; i != s.length; ++i) view[i] = s.charCodeAt(i) & 0xff;
         return buf;
     }
         // 将blob对象创建bloburl，然后用a标签实现弹出下载框
     function openDownloadDialog(blob, fileName) {
         if (typeof blob == "object" && blob instanceof Blob) {
             blob = URL.createObjectURL(blob); // 创建blob地址
         }
         var aLink = document.createElement("a");
         aLink.href = blob;
         // HTML5新增的属性，指定保存文件名，可以不要后缀，注意，有时候 file:///模式下不会生效
         aLink.download = fileName || "";
         var event;
         if (window.MouseEvent) event = new MouseEvent("click");
         //   移动端
         else {
             event = document.createEvent("MouseEvents");
             event.initMouseEvent( "click", true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null );
         }
         aLink.dispatchEvent(event);
     }
	 function downloadExcel(){
	 debugger;
		 // 用的例子
		 let sheet1data = [ { department: "行政部", count: 2 }, { department: "前端部", count: 2 } ];
		 let sheet2data = [ { name: "张三", do: "整理文件" }, { name: "李四", do: "打印" } ];
		 let sheet3data = [ { name: "张大人", do: "vue" }, { name: "李大人", do: "react" } ];
		 var sheet1 = XLSX.utils.json_to_sheet(sheet1data);
		 var sheet2 = XLSX.utils.json_to_sheet(sheet2data);
		 var sheet3 = XLSX.utils.json_to_sheet(sheet3data);
		 
		 /* create a new blank workbook */
		 var wb = XLSX.utils.book_new();
		 XLSX.utils.book_append_sheet(wb, sheet1, "部门统计");
		 XLSX.utils.book_append_sheet(wb, sheet2, "行政部");
		 XLSX.utils.book_append_sheet(wb, sheet3, "前端部");
		 const workbookBlob = workbook2blob(wb);
		 openDownloadDialog(workbookBlob, `部门统计.xlsx`);
	}
    </script>
  </body>
</html>
```

### Vue 导出

#### 安装依赖

`npm install xlsx --save`

参考：https://www.npmjs.com/package/xlsx

#### 引入依赖

在组件中导入 xlsx

```html
import XLSX from 'xlsx';
```

#### 导出方法

```js
async workbookData(id){
    const wb = XLSX.utils.book_new();
    const { data: res } = await this.$http.get("analysisTask/edit/" + id);
    if (res.code == 200) {
        this.res_type = res.data.res_type;
        const accountRes = JSON.parse(res.data.account_res);
        const tradeRes = JSON.parse(res.data.trade_res);
        const operationRes = JSON.parse(res.data.operation_res);
        const sheetData1 = accountRes.map(item => ({
            '登录帐号': item.mainAccount,
            '手机': item.phone,
            '邮箱': item.email,
        }));
        const sheetData2 = tradeRes.map(item => ({
            '登录帐号': item.mainAccount,
            '手机': item.phone,
            '邮箱': item.email,
        }));
        const sheetData3 = operationRes.map(item => ({
            '登录帐号': item.mainAccount,
            '手机': item.phone,
            '邮箱': item.email,
        }));
        const sheet1 = XLSX.utils.json_to_sheet(sheetData1);
        const sheet2 = XLSX.utils.json_to_sheet(sheetData2);
        const sheet3 = XLSX.utils.json_to_sheet(sheetData3);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, sheet1, '账户信息1');
        XLSX.utils.book_append_sheet(wb, sheet2, '账户信息2');
        XLSX.utils.book_append_sheet(wb, sheet3, '账户信息3');
    } else {
        this.$message.error("获取Excel数据失败:" + res.msg);
    }
    return wb;
},
/**
  * 加载菜单表格
  */
async downExcel(id) {
    const wb = await this.workbookData(id)
    const workbookBlob = this.workbook2blob(wb);
    // 导出最后的总表
    this.openDownloadDialog(workbookBlob, '任务结果.xlsx');
},
```

#### 其他函数

##### openDownloadDialog

将blob对象创建bloburl，然后用a标签实现弹出下载框：

```js
openDownloadDialog(blob, fileName) {
    if (typeof blob == "object" && blob instanceof Blob) {
        blob = URL.createObjectURL(blob); // 创建blob地址
    }
    var aLink = document.createElement("a");
    aLink.href = blob;
    // HTML5新增的属性，指定保存文件名，可以不要后缀，注意，有时候 file:///模式下不会生效
    aLink.download = fileName || "";
    var event;
    if (window.MouseEvent) event = new MouseEvent("click");
    //   移动端
    else {
        event = document.createEvent("MouseEvents");
        event.initMouseEvent( "click", true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null );
    }
    aLink.dispatchEvent(event);
},
```

##### workbook2blob

将workbook装化成blob对象：

```js
workbook2blob(workbook){
    // 生成excel的配置项
    var wopts = {
        // 要生成的文件类型
        bookType: "xlsx",
        // // 是否生成Shared String Table，官方解释是，如果开启生成速度会下降，但在低版本IOS设备上有更好的兼容性
        bookSST: false,
        type: "binary"
    };
    var wbout = XLSX.write(workbook, wopts);
    // 将字符串转ArrayBuffer

    var blob = new Blob([this.s2ab(wbout)], {
        type: "application/octet-stream"
    });
    return blob;
},
s2ab(s) {
   var buf = new ArrayBuffer(s.length);
   var view = new Uint8Array(buf);
   for (var i = 0; i != s.length; ++i) view[i] = s.charCodeAt(i) & 0xff;
   return buf;
},
```



