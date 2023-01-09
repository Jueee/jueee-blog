---
title: Vue中的el-table实现拖拽排序
layout: info
commentable: true
date: 2022-12-15
mathjax: true
mermaid: true
tags: [Vue]
categories: Vue
description: 
---

element ui 表格没有自带的拖拽排序的功能，只能借助第三方插件 Sortable.js 来实现。

<!--more-->

### Sortable.js

- 官网：http://www.sortablejs.com/
- 配置项：http://www.sortablejs.com/options.html
- GitHub：https://github.com/SortableJS/Sortable

### 实现步骤

#### 安装 Sortable.js

```javascript
npm install --save sortablejs
```

#### 引入依赖

在当前  Vue 中JS代码中引入：

```vue
import Sortable from "sortablejs";
```

#### 配置 el-table

在当前 vue文件 template 的 el-table中 **指定 row-key，row-key必须是唯一的**，如ID，不然会出现排序不对的情况。

【注意】row-key不可用 index，因为拖拽后index会变，会有问题。

```vue
<el-table
          ref="table"
          :data="apiObj"
          row-key="id"
          @selection-change="selectionChange"
          :paginationLayout="'prev, pager, next'" >
```

#### 项目完整代码

```vue
<template>
  <div class="dic-data">
    <el-container>
      <el-header>
         <el-button type="primary" @click="saveSortData(apiObjDrag)"
              >排序保存</el-button
            >
      </el-header>
      <el-main class="nopadding">
        <el-table
           stripe
          ref="table"
          :data="apiObj"
          row-key="id"
          @selection-change="selectionChange"
          :paginationLayout="'prev, pager, next'"
        >
          <el-table-column
            label="序号"
            type="index"
            width="50"
          ></el-table-column>
          <el-table-column
            label="字典键"
            prop="dictKey"
            align="left"
          ></el-table-column>
          <el-table-column
            label="字典值"
            prop="dictValue"
            align="left"
          ></el-table-column>
        </el-table>
      </el-main>
    </el-container>
  </div>
</template>
<script>
import Sortable from 'sortablejs'

export default {
  name: 'data',
  data() {
    return {
      dialog: {
        new: false,
      },
      apiObj: [
        {
          dictKey:'你好',
          dictValue:'aa'
        },
        {
          dictKey:'我好',
          dictValue:'bb'
        },
        {
          dictKey:'他好',
          dictValue:'cc'
        }
      ],
      apiObjDrag: [],
    }
  },
  created() {
    this.getDictDatalist()
    this.$nextTick(() => {
      this.rowDrop()
    })
  },
  methods: {    
    //行-拖拽
    rowDrop() {
      const tbody = document.querySelector('.el-table__body-wrapper tbody')
      const _this = this
      Sortable.create(tbody, {
        onEnd({ newIndex, oldIndex }) {
          const currRow = _this.apiObj.splice(oldIndex, 1)[0]
          _this.apiObj.splice(newIndex, 0, currRow)
          //   拖动后获取newIdex
          let arr = Array.from(_this.apiObj)
          _this.apiObjDrag = arr.map((item, index) => {
            return {
              id: item.id,
              dictSort: index,
            }
          })
        },
      })
    },
    // 排序后，把拖动后的结果穿啊给后端
    async saveSortData(apiObjDrag) {
      if (apiObjDrag == '') {
        this.$message.warning("请先拖动字典数据，再点击");
        return
      }
      const {data: res} = await this.$http.post( "sortConfig", apiObjDrag);
      if (res.code === 200) {
        this.$message.success('排序成功')
      } else {
        this.$alert(res.msg, '提示', { type: 'error' })
      }
    },
    //表格选择后回调事件
    selectionChange(selection) {
      this.selection = selection
    },
  },
}
</script>
```

#### 后端代码

Controller 层：

```java
@PostMapping("/sortConfig")
public ResponseBean sortConfig(@RequestBody @Validated Config[] configs) {
    service.sortConfig(configs);
    return ResponseBean.success();
}
```

Service 层：

```java
public void sortConfig(Config[] configs) {
    for (Config config:configs) {
        Config infoConfig = selectById(config.getId());
        if (infoConfig!=null){
            infoConfig.setOrdernum(config.getOrdernum());
            mapper.updateById(infoConfig);
        }
    }
}
```
