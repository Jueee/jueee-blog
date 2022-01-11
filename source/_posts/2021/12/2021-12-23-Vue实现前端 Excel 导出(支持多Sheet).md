---
title: Vue 实现前端 Excel 导出(支持多Sheet)
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

<!--more-->

### 安装依赖

`npm install xlsx --save`

### 引入依赖

在组件中导入 xlsx

```html
import XLSX from 'xlsx';
```

### 导出方法

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

### 其他函数

#### openDownloadDialog

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

#### workbook2blob

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

### 压缩包导出

#### 安装依赖

```shell
npm i jszip -S
npm i file-saver -S 
```

#### 增加按钮

实现多选非常简单：手动添加一个`el-table-column`，设`type`属性为`selection`即可

```html
<el-button size="small" type="success" icon="el-icon-circle-plus-outline" @click="batchDownload" >批量下载</el-button>

<el-table
          border
          size="small"
          v-loading="loading"
          stripe
          :data="analysisTaskData"
          style="width: 100%;"
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="50"></el-table-column>
          <el-table-column prop="id" label="ID" width="50"></el-table-column>
          <el-table-column prop="type" label="类型"></el-table-column>
</el-table>
```

对应方法

```js
export default {
  data() {
    return {
      multipleSelection: []
    };
  },
  methods: {
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    async batchDownload(){
      console.log(this.multipleSelection)
      this.$message.success("批量下载成功！");
    }
  }
}
```

#### 下载方法

```vue
import JSZip from 'jszip'
import FileSaver from 'file-saver'
```

下载方法

```js
    async batchDownload(){
      const zip = new JSZip()
      for (var i = 0; i < this.multipleSelection.length; i++) {
        const id = this.multipleSelection[i].id
        const wb = await this.workbookData(id)
        const file_name = this.multipleSelection[i].content+'-任务结果('+id+').xlsx'
        zip.file(file_name, this.workbook2blob(wb), { binary: true })
      }
      let zipName = '批量下载'
      zip.generateAsync({type:"blob"}).then(content => { 
        //生成zip文件包
        FileSaver.saveAs(content, `${zipName}.zip`)
        this.$message.success("批量下载成功！");
      })
    }
```

#### 
