---
title: Vue之ElementUI动态创建输入框
layout: info
commentable: true
date: 2021-05-13
mathjax: true
mermaid: true
tags: [Vue,ElementUI]
categories: Vue
description: 
---

### 动态添加属性

#### 示例代码

```html
<template>
    <div>
        <el-form :model="dataForm" label-width="100px">
            <el-form-item 
                v-for="(domain, index) in dataForm.domains"
                :label=domain.key
                :key="domain.key"
                :prop="'domains.' + index + '.value'"
                :rules="{ required: true, message: '属性不能为空', trigger: 'blur'}">
                <el-row>
                    <el-col :span="6">
                            <el-input v-model="domain.value"></el-input>
                    </el-col>
                    <el-col :span="4">
                            <el-button @click.prevent="removeDomain(domain)">删除</el-button>
                    </el-col>
                </el-row>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitForm('dataForm')">提交属性 </el-button>
                <el-button @click="addDomain">新增属性</el-button>
            </el-form-item>
        </el-form>
     </div>
</template>
<script>
  export default {
    data() {
      return {
        dataForm: {
          domains: [{
            key: '属性a',
            value: 'aaa'
          }, {
            key: '属性b',
            value: 'bbb'
          }]
        }
      }
    },
    methods: {
      removeDomain(item) {
        var index = this.dataForm.domains.indexOf(item)
        if (index !== -1) {
          this.dataForm.domains.splice(index, 1)
        }
      },
      addDomain() {
        this.$prompt('请输入属性', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消'
        }).then(({ value }) => {
          this.dataForm.domains.push({
            value: '',
            key: value
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入'
          })
        })
      }
    }
  }
</script>
```

#### 实现效果

默认：

![image-20210513153916188](/images/2021/05/image-20210513153916188.png)

增加属性：

![image-20210513153943479](/images/2021/05/image-20210513153943479.png)

增加后：

![image-20210513153956956](/images/2021/05/image-20210513153956956.png)

删除：

![image-20210513154011220](/images/2021/05/image-20210513154011220.png)

### 动态添加输入框

#### 示例代码

```html
<template>
    <div>
        <el-form :model="dataForm" label-width="100px" size="small">
            <el-form-item label="名称匹配" prop="name">
              <el-row >
                <span v-for="(domain, index) in dataForm.domains">
                  <el-col :span="5">
                    <el-input v-model="domain.value"></el-input>
                  </el-col>
                  <el-col :span="2">
                    <el-button  @click="removeDomain(index)">删除</el-button>
                  </el-col>
                </span>
                <el-col :span="2">
                  <el-button  @click="addDomain">新增</el-button>
                </el-col>
              </el-row>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitForm('dataForm')">提交属性 </el-button>
            </el-form-item>
        </el-form>
     </div>
</template>
<script>
  export default {
    data() {
      return {
        dataForm: {
          domains: [{value:"aaa"},{value:"bbb"},{value:"ccc"}]
        }
      }
    },
    methods: {
      removeDomain(index) {
        this.dataForm.domains.splice(index, 1)
      },
      addDomain() {
        this.dataForm.domains.push({value:""})
      }
    }
  }
</script>
```

#### 实现效果

![image-20210513170442637](/images/2021/05/image-20210513170442637.png)

#### 优化效果

通过 `clearable @clear=''` 来实现删除效果。

```html
<template>
    <div>
        <el-form :model="dataForm" label-width="100px" size="small">
            <el-form-item label="名称匹配" prop="name">
              <el-row >
                <el-col :span="3" v-for="(domain, index) in dataForm.domains" >
                  <el-input v-model="domain.value" clearable @clear="removeDomain(index)"></el-input>
                </el-col>
                <el-col :span="2">
                  <el-button  @click="addDomain">新增</el-button>
                </el-col>
              </el-row>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitForm('dataForm')">提交属性 </el-button>
            </el-form-item>
        </el-form>
     </div>
</template>
```

![image-20210513171431164](/images/2021/05/image-20210513171431164.png)