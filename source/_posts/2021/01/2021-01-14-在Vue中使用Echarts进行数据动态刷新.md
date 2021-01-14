---
title: 在Vue中使用Echarts进行数据动态刷新
layout: info
commentable: true
date: 2021-01-14
mathjax: true
mermaid: true
tags: [Vue,Echarts]
categories: 
- [Vue]
- [Apache,Echarts]
description: 
---

### 出现问题

在Vue使用Echarts时，可能会遇到这样的问题，就是直接刷新浏览器，或者数据变化时，Echarts不更新?

这是因为Echarts是数据驱动的，这意味着只要我们重新设置数据，那么图表就会随之重新渲染，这是实现本需求的基础。

<!--more-->

### watch 监听

如果想要支持数据的自动刷新，必然需要一个监听器能够实时监听到数据的变化然后告知Echarts重新设置数据。

此时，可以用 watch 监听 data 的变化，数据发生变化时重新初始化Echarts图。

```js
watch:{
   option:function(newvalue,oldvalue){   
     //侦听相对应的属性
     //判断echarts对象是否存在存在 if(charts),charts为定义的echarts对象,
     //若存在， 则继续判断属性是否发生变化 if(newvalue)，发生变化重新设置echarts的option, charts.setOption(newvalue),没发生变化则 charts.setOption(loldvalue)
     //若charts对象不存在，则直接初始化echarts
   } 
}
```

### 示例

```js
  watch:{
    ratio:function(newvalue,oldvalue){  
      if (oldvalue != newvalue) {
        var echarts = require('echarts');
        var myChart = echarts.init(document.getElementById("ratioId"));
        var option = {
            tooltip: {
                formatter: '{a} <br/>{b} : {c}%',
            },
            series: [
                {
                    type: 'gauge',
                    startAngle: 210,
                    endAngle: -30,
                    splitNumber:10,
                    radius: '100%',
                    axisLabel:{
                        show:false
                    },
                    axisLine:{
                        lineStyle:{
                            width: 4
                        }
                    },
                    pointer:{
                        width: 3
                    },
                    detail:{
                        fontSize: 18,
                        padding:[20,0,0,0]
                    },
                    data: [{value: newvalue}]
                }
            ]
        };
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
      }
    }
  }
```

效果：

![image-20210114101815365](/images/2021/01/image-20210114101815365.png)