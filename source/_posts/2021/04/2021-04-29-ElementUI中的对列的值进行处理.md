---
title: ElementUI中的对列的值进行处理
layout: info
commentable: true
date: 2021-04-29
mathjax: true
mermaid: true
tags: [Vue,ElementUI]
categories: Vue
description: 
---

### 超链接

普通超链接

```html
<el-table-column label="URL">
    <template slot-scope="scope">
        <el-link :href="scope.row.urlString" target="_blank" class="buttonText"  type="primary" :underline="false"> {{ scope.row.keyword }}</el-link>
    </template>
</el-table-column>
```

函数超链接

```html
<el-link :href="toConfig(scope.row.name)" target="_blank" > {{ scope.row.name }}</el-link>

    toConfig(name){
      return "XXX?name="+name;
    },
```

### 类型翻译

#### 使用 formatter

```html
<el-table-column prop="anttype" label="类型" width="120" :formatter="anttypeFormat"></el-table-column>
```

以下函数无效：

```js
    anttypeFormat(row, column) {
        this.markerCategorys.forEach(t => {
          if(t.id == row.anttype){
            return t.name;
          }
        })
    },
```

需要修改为：

```js
    anttypeFormat(row, column) {
        for (var i = 0; i < this.markerCategorys.length; i++) {
          if(this.markerCategorys[i].id == row.anttype){
            return this.markerCategorys[i].name;
          }
        }
    },
```

这是由于 Vue 中的 forEach 循环无法终止程序 return 无效。需要改为用for循环即可。

#### 使用 过滤器

##### 普通过滤器

```html
<el-table-column label="日期" width="180">
    <template slot-scope="scope">
        <span>{{ scope.row.date | formatDate('HH:mm:ss') }}</span>
    </template>
</el-table-column>
```

定义函数

```js
    dateFormat(row,column){
      var date = row[column.property];
      if(date === undefined){
        return ''
      }
      var dT=new Date(date);//row 表示一行数据, dateTime 表示要格式化的字段名称
      return dT.getFullYear()+"-"+(dT.getMonth()+1)+"-"+dT.getDate()+" "+dT.getHours()+":"+dT.getMinutes()+":"+dT.getSeconds();
    }
```

##### this 过滤器

Vue 局部过滤器获取不到this，可以在data里面加个字段赋值this，然后在过滤器里传入参数。

定义函数

```js
export default {
  data() {
    return {
      that:this
    }
  },
  filters: {
    anttypeFormat(anttype,that) {
        for (var i = 0; i < that.markerCategorys.length; i++) {
          if(that.markerCategorys[i].id == anttype){
            return that.markerCategorys[i].name;
          }
        }
    }
  },
  methods: {}
}
```

所有过滤器

```html
<el-table-column label="备注描述">
    <template slot-scope="scope">
        <div v-if="!scope.row.anttype==''">{{ scope.row.anttype | anttypeFormat(that) }}</div>
    </template>
</el-table-column>
```

### 状态 switch

Java 状态：

```java
@TableField(exist = false)
private Boolean statusVO;

public Boolean getStatusVO() {
    return DisableStatusEnum.getStatusVO(getStatus());
}
```

其中：

```java
public enum DisableStatusEnum {

    DISABLE(0),
    AVAILABLE(1);

    private int statusCode;

    DisableStatusEnum(int statusCode) {
        this.statusCode = statusCode;
    }

    public int getStatusCode() {
        return statusCode;
    }

    public void setStatusCode(int statusCode) {
        this.statusCode = statusCode;
    }

    public static Boolean getStatusVO(Integer status) {
        if (status!=null && status== AVAILABLE.getStatusCode()){
            return false;
        }
        return true;
    }

    public static int getStatus(Boolean status) {
        return status? DisableStatusEnum.DISABLE.getStatusCode() : DisableStatusEnum.AVAILABLE.getStatusCode();
    }
}
```

ElementUI

```html
<el-table-column label="状态" width="80">
    <template slot-scope="scope">
        <el-switch v-model="scope.row.statusVO" @change="changStatus(scope.row)"></el-switch>
    </template>
</el-table-column>
```

Vue

```js
    //改变特征禁用状态
    async changStatus(row) {
      const { data: res } = await this.$http.put(
        "updateStatus/" + row.id + "/" + row.statusVO
      );
      if (res.code !== 200) {
        this.$message.error("更新状态失败:" + res.msg);
        row.statusVO = !row.statusVO;
      } else {
        this.$message.success("更新状态成功");
      }
    },
```

Java 接口

```java
@PutMapping("/updateStatus/{id}/{status}")
public ResponseBean updateStatus(@PathVariable Integer id, @PathVariable Boolean status) {
    service.updateStatus(id, status);
    return ResponseBean.success();
}
```

