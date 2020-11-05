---
title: 基于Vue组件库Element搭建管理系统
layout: info
commentable: true
date: 2020-11-03
mathjax: true
mermaid: true
tags: [Vue,Element]
categories: Vue
description: 
---

### Element 介绍

Element，一套为开发者、设计师和产品经理准备的基于 Vue 2.0 的桌面端组件库。

Element 提供了配套设计资源，帮助你的网站快速成型。

是由饿了么公司前端团队开源的。

- 官网：https://element.eleme.cn/
- GitHub：https://github.com/ElemeFE/element/

<!--more-->

### 安装 Element

```bash
npm i element-ui -S
```

### 引入 Element

在 main.js 中写入以下内容：

```javascript
import Vue from 'vue';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue';

Vue.use(ElementUI);

new Vue({
  el: '#app',
  render: h => h(App)
});
```

若报错：

![image-20201102153341973](/images/2020/11/image-20201102153341973.png)

原因：缺少匹配规则

解决办法：在webpack.config.js文件中的module中增加如下json

```json
{
   test: /\.(eot|svg|ttf|woff|woff2)(\?\S*)?$/,
   loader: 'file-loader'
}
```

如下图所示：

![image-20201102153601127](/images/2020/11/image-20201102153601127.png)

### Element 警告处理

#### explicit keys

Element for 循环报如下异常：

> component lists rendered with v-for should have explicit keys

处理方案：加上 `:key="index"`

v-for 列表渲染时，组件或元素中还要添加一个 :key="xxx"，这里可以看一下 item 有没有唯一标识 id，如果有，可以设置为 :key="item.id"

如果没有唯一标识，可以考虑 v-for="(item, idx) in items"，然后设置 :key="idx"

### 增删改查示例

```html
<template>
    <div>
      <el-form size="mini" :inline="true" :model="queryMap" class="demo-form-inline">
        <el-form-item label="图书名">
          <el-input clearable @clear="search" v-model="queryMap.name" placeholder="图书名"></el-input>
        </el-form-item>
        <el-form-item label="作者">
          <el-input clearable @clear="search" v-model="queryMap.author" placeholder="作者"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="search">查询</el-button>
          <el-button type="success" icon="el-icon-circle-plus-outline" @click="openAdd">添加</el-button>
        </el-form-item>
      </el-form>
        <el-table
                :data="tableData"
                border
                style="width: 70%">
            <el-table-column 
                    fixed
                    prop="id"
                    label="编号"
                    width="150">
            </el-table-column>
            <el-table-column
                    prop="name"
                    label="图书名"
                    >
            </el-table-column>
            <el-table-column
                    prop="author"
                    label="作者"
                    width="120">
            </el-table-column>
            <el-table-column
                    fixed="right"
                    label="操作"
                    width="100">
                <template slot-scope="scope">
                    <el-button @click="edit(scope.row)" type="text" size="small">修改</el-button>
                    <el-button @click="deleteBook(scope.row)" type="text" size="small">删除</el-button>
                </template>
            </el-table-column>
        </el-table>

        <el-pagination
                background
                layout="prev, pager, next"
                :page-size="pageSize"
                :total="total"
                @current-change="page"
                >
        </el-pagination>

        <el-dialog
        title="添加物资去处"
        :visible.sync="addDialogVisible"
        width="30%"
        @close="closeAddDialog"
      >
        <span>
          <el-form
            :model="addRuleForm"
            :rules="addRules"
            ref="addRuleFormRef"
            label-width="100px"
            class="demo-ruleForm"
          >
            <el-form-item label="图书名称" prop="name">
                <el-input v-model="addRuleForm.name"></el-input>
            </el-form-item>

            <el-form-item label="作者" prop="author">
                <el-input v-model="addRuleForm.author"></el-input>
            </el-form-item>
          </el-form>
        </span>
        <span slot="footer" class="dialog-footer">
          <el-button @click="addDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="add">确 定</el-button>
        </span>
      </el-dialog>
    </div>
</template>

<script>
    export default {
        methods: {
            deleteBook(row){
                const _this = this
                this.$axios.delete('book/deleteById/'+row.id).then(function(resp){
                    _this.$alert('《'+row.name+'》删除成功！', '消息', {
                        confirmButtonText: '确定',
                        callback: action => {
                            window.location.reload()
                        }
                    })
                })
            },
            edit(row) {
                this.$router.push({
                    path: '/update',
                    query:{
                        id:row.id
                    }
                })
            },
            page(currentPage){
                this.queryMap.pageNum = currentPage;
                this.getConsumerList();
            },
            //搜索
            search() {
              this.queryMap.pageNum = 1;
              this.getConsumerList();
            },
            async getConsumerList() {
              const _this = this
              this.$axios.get('book/findAll/'+(_this.queryMap.pageNum-1)+'/6', {
                  params: this.queryMap
                }).then(function(resp){
                  console.log(resp)
                  _this.tableData = resp.data.content
                  _this.pageSize = resp.data.size
                  _this.total = resp.data.totalElements
              })
            },
            openAdd() {
              this.addDialogVisible = true;
            },
            //关闭弹出框
            closeAddDialog() {
              this.$refs.addRuleFormRef.clearValidate();
              this.addRuleForm = {};
            },
            //添加
            add() {
              this.$refs.addRuleFormRef.validate(async valid => {
                if (!valid) {
                  console.log(this.addRuleForm);
                  return;
                } else {
                  const _this = this
                  this.$axios.post('book/save',this.addRuleForm).then(function(resp){
                      if(resp.data == 'success'){
                          _this.addDialogVisible = false;
                          _this.$message.success("添加成功");
                          _this.addRuleForm = {};
                          _this.getConsumerList();
                      } else {
                        return this.$message.error("添加失败:" + res.msg);
                      }
                  })                
                }
              });
            }
        },

        data() {
            return {
                addDialogVisible: false, //添加弹框是否显示
                queryMap: { pageNum: 1, pageSize: 10, name: "" }, //查询对象
                pageSize: 1,
                total: 11,
                tableData: [{
                    id: 1,
                    name: '',
                    author: ''
                }],
                addRuleForm: {
                    name: '',
                    author: ''
                },
                addRules: {
                    name: [
                        { required: true, message: '图书名称不能为空', trigger: 'blur' }
                    ],
                    author:[
                        { required: true, message: '作者不能为空', trigger: 'blur' }
                    ]
                }
            }
        },

        created() {
          this.getConsumerList();
        }
    }
</script>
```

效果如下：

![image-20201104161014813](/images/2020/11/image-20201104161014813.png)