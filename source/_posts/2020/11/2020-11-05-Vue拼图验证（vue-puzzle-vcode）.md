---
title: Vue拼图验证（vue-puzzle-vcode）
layout: info
commentable: true
date: 2020-11-05
mathjax: true
mermaid: true
tags: [Vue]
categories: Vue
description: 
---

### 插件介绍

Vue 纯前端的拼图人机验证、右滑拼图验证。

- 插件网站：https://www.npmjs.com/package/vue-puzzle-vcode
- Demo：https://isluo.com/work/vue-puzzle-vcode/#/

### 安装依赖

```bash
npm install vue-puzzle-vcode --save
```

### 使用依赖

```html
import Vcode from "vue-puzzle-vcode";
 
<Vcode :show="isShow" @success="success" @close="close" />
```

### 简单例子

```html
<template>
  <div>
    <Vcode :show="isShow" @success="success" @close="close" />
    <button @click="submit">登录</button>
  </div>
</template>
 
<script>
import Vcode from "vue-puzzle-vcode";
export default {
  data() {
    return {
      isShow: false, // 验证码模态框是否出现
    };
  },
  components: {
    Vcode,
  },
  methods: {
    submit() {
      this.isShow = true;
    },
    // 用户通过了验证
    success(msg) {
      this.isShow = false; // 通过验证后，需要手动隐藏模态框
    },
    // 用户点击遮罩层，应该关闭模态框
    close() {
      this.isShow = false;
    },
  },
};
</script>
```

### 参数

| 字段         | 类型    | 默认值             | 说明                                                         |
| :----------- | :------ | :----------------- | :----------------------------------------------------------- |
| show         | Boolean | false              | 是否显示验证码弹框                                           |
| canvasWidth  | Number  | 310                | 主图区域的宽度，单位 px                                      |
| canvasHeight | Number  | 160                | 主图区域的高度，单位 px                                      |
| puzzleScale  | Number  | 1                  | 拼图块(小的拼图)的大小比例，0.2 ～ 2 ，数字越大，拼图越大    |
| sliderSize   | Number  | 50                 | 左下角用户拖动的那个滑块的尺寸，单位 px                      |
| range        | Number  | 10                 | 判断成功的误差范围，单位 px, 滑动的距离和拼图的距离小于等于此值时，会判定重合 |
| imgs         | Array   | null               | 自定义图片，见下方例子                                       |
| successText  | String  | "验证通过！"       | 验证成功时的提示文字                                         |
| failText     | String  | "验证失败，请重试" | 验证失败时的提示文字                                         |
| sliderText   | String  | "拖动滑块完成拼图" | 下方滑动条里的文字                                           |

### 事件

| 事件名  | 返回值 | 说明                                                         |
| :------ | :----- | :----------------------------------------------------------- |
| success | 偏差值 | 验证通过时会触发，返回值是用户移动的距离跟目标距离的偏差值 px |
| fail    | 偏差值 | 验证失败时会触发，返回值同上                                 |
| close   | null   | 用户点击遮罩层的回调                                         |

### 自定义图片

```html
<template>
  <Vcode :imgs="[Img1, Img2]" />
</template>
 
<script>
import Img1 from "~/assets/img1.png";
import Img2 from "~/assets/img2.png";
 
export default {
  data() {
    return {
      Img1,
      Img2,
    };
  },
};
</script>
```

- 也可以是网络图片完整 URL 路径，但注意图片跨域问题，因为 canvas api 无法调用跨 域的图片

### 说明

- 当不传递 imgs 字段或图片加载出错时，会自动生成随机图片
- 模态框的显示和隐藏完全由父级控制，所以用户通过验证后，需要手动隐藏模态框

### 参考资料

- https://www.npmjs.com/package/vue-puzzle-vcode