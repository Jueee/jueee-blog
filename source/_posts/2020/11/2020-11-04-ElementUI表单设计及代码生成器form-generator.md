---
title: Element UI表单设计及代码生成器form-generator
layout: info
commentable: true
date: 2020-11-03
mathjax: true
mermaid: true
tags: [Vue,Element]
categories: Vue
description: 
---

### form-generator

Element UI表单设计及代码生成器，可将生成的代码直接运行在基于Element的vue项目中；也可导出JSON表单，使用配套的解析器将JSON解析成真实的表单。

**源码：**

- GitHub：https://github.com/JakHuang/form-generator
- Gitee：https://gitee.com/mrhj/form-generator

**在线地址**：

- 国内预览地址：https://mrhj.gitee.io/form-generator/#/
- vscode 插件：https://github.com/JakHuang/form-generator-plugin

<!--more-->

### form-generator-plugin

- GitHub：https://github.com/JakHuang/form-generator-plugin

#### 安装插件

使用 vscode 搜索插件 `Form Generator Plugin`，并点击 install 进行安装。

![image-20201103100725339](/images/2020/11/image-20201103100725339.png)

#### 使用插件

选择 vue 文件，邮件选择 “打开表单设计器”。

![image-20201103100909195](/images/2020/11/image-20201103100909195.png)

拖动控件进行布局：

![image-20201103193921825](/images/2020/11/image-20201103193921825.png)

导出或者复制代码，如下所示：

```vue
<template>
  <div>
    <el-form ref="elForm" :model="formData" :rules="rules" size="medium" label-width="100px">
      <el-form-item label="单行文本" prop="field101">
        <el-input v-model="formData.field101" placeholder="请输入单行文本" clearable :style="{width: '100%'}">
        </el-input>
      </el-form-item>
      <el-form-item label="时间范围" prop="field104">
        <el-time-picker v-model="formData.field104" is-range format="HH:mm:ss" value-format="HH:mm:ss"
          :style="{width: '100%'}" start-placeholder="开始时间" end-placeholder="结束时间" range-separator="至"
          clearable></el-time-picker>
      </el-form-item>
      <el-form-item label="多选框组" prop="field103">
        <el-checkbox-group v-model="formData.field103" size="medium">
          <el-checkbox v-for="(item, index) in field103Options" :key="index" :label="item.value"
            :disabled="item.disabled">{{item.label}}</el-checkbox>
        </el-checkbox-group>
      </el-form-item>
      <el-form-item label="评分" prop="field105">
        <el-rate v-model="formData.field105"></el-rate>
      </el-form-item>
      <el-form-item label="上传" prop="field106" required>
        <el-upload ref="field106" :file-list="field106fileList" :action="field106Action"
          :before-upload="field106BeforeUpload">
          <el-button size="small" type="primary" icon="el-icon-upload">点击上传</el-button>
        </el-upload>
      </el-form-item>
      <el-form-item size="large">
        <el-button type="primary" @click="submitForm">提交</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
export default {
  components: {},
  props: [],
  data() {
    return {
      formData: {
        field101: undefined,
        field104: null,
        field103: [],
        field105: 0,
        field106: null,
      },
      rules: {
        field101: [{
          required: true,
          message: '请输入单行文本',
          trigger: 'blur'
        }],
        field104: [{
          required: true,
          message: '时间范围不能为空',
          trigger: 'change'
        }],
        field103: [{
          required: true,
          type: 'array',
          message: '请至少选择一个field103',
          trigger: 'change'
        }],
        field105: [{
          required: true,
          message: '评分不能为空',
          trigger: 'change'
        }],
      },
      field106Action: 'https://jsonplaceholder.typicode.com/posts/',
      field106fileList: [],
      field103Options: [{
        "label": "选项一",
        "value": 1
      }, {
        "label": "选项二",
        "value": 2
      }, {
        "label": "选项三",
        "value": ""
      }, {
        "label": "选项四",
        "value": ""
      }, {
        "label": "选项五",
        "value": ""
      }],
    }
  },
  computed: {},
  watch: {},
  created() {},
  mounted() {},
  methods: {
    submitForm() {
      this.$refs['elForm'].validate(valid => {
        if (!valid) return
        // TODO 提交表单
      })
    },
    resetForm() {
      this.$refs['elForm'].resetFields()
    },
    field106BeforeUpload(file) {
      let isRightSize = file.size / 1024 / 1024 < 2
      if (!isRightSize) {
        this.$message.error('文件大小超过 2MB')
      }
      return isRightSize
    },
  }
}

</script>
<style>
.el-rate {
  display: inline-block;
  vertical-align: text-top;
}

.el-upload__tip {
  line-height: 1.2;
}

</style>

```

