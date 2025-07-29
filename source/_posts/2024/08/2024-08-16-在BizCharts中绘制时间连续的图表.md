---
title: 在BizCharts中绘制时间连续的图表
layout: info
commentable: true
date: 2024-08-16
mathjax: true
mermaid: true
tags: [React,BizCharts]
categories: [React,BizCharts]
description: 
---

### 面临问题

在 `BizCharts` 中，如果原始数据的时间不联系，那么绘制的时候这些时间会缺失。

需要在 `BizCharts` 时间数据不足时自动补0确保横坐标时间连续。

data 包含 date、name、count 三个属性，最小日期取 data 的最小 date，最大日期取当天的数据，注意需要区分不同的name进行分组。

<!--more-->

### 解决方案

为了在 `BizCharts` 中绘制时间连续的图表，当数据不足时自动补0，可以使用以下步骤：

1. **组织数据：** 将数据按 `name` 属性分组。

2. **生成日期范围：** 根据数据的最小日期和当天日期生成一个完整的日期范围。

3. **填充缺失数据：** 对每组数据填充缺失的日期，并将计数设为 0。

### 完整代码

如果项目中没有 moment，需要先进行安装：

```
npm install moment --save
```

以下是完整的代码示例，展示了如何实现这一功能：

```javascript
import React from 'react';
import { Chart, Geom, Axis, Tooltip } from 'bizcharts';
import moment from 'moment';

// 示例数据
const data = [
  { date: '2023-08-01', name: 'A', count: 10 },
  { date: '2023-08-03', name: 'A', count: 20 },
  { date: '2023-08-01', name: 'B', count: 15 },
  { date: '2023-08-02', name: 'B', count: 25 },
];

// Step 1: 按 name 分组数据
const groupedData = data.reduce((acc, item) => {
  if (!acc[item.name]) acc[item.name] = [];
  acc[item.name].push(item);
  return acc;
}, {});

// Step 2: 生成日期范围
const minDate = moment.min(data.map(d => moment(d.date)));
const maxDate = moment();

const dateRange = [];
for (let m = moment(minDate); m.isSameOrBefore(maxDate); m.add(1, 'days')) {
  dateRange.push(m.format('YYYY-MM-DD'));
}

// Step 3: 填充缺失数据
const filledData = Object.keys(groupedData).reduce((acc, name) => {
  const nameData = groupedData[name];
  const filledNameData = dateRange.map(date => {
    const foundData = nameData.find(d => d.date === date);
    return foundData ? foundData : { date, name, count: 0 };
  });
  return acc.concat(filledNameData);
}, []);

const scale = {
  date: {
    type: 'timeCat',
    range: [0, 1],
  },
  count: {
    min: 0,
  },
};

const App = () => (
  <Chart height={400} data={filledData} scale={scale} forceFit>
    <Axis name="date" />
    <Axis name="count" />
    <Tooltip crosshairs={{ type: 'y' }} />
    <Geom type="line" position="date*count" color="name" />
    <Geom type="point" position="date*count" color="name" shape="circle" />
  </Chart>
);

export default App;
```

### 代码解释

1. **数据准备**：

   - 示例数据 `data` 包含 `date`、`name` 和 `count` 属性。

2. **按 `name` 分组数据**：

   - 使用 `reduce` 方法将数据按 `name` 属性分组，生成 `groupedData` 对象。

3. **生成日期范围**：

   - 使用 `moment.min` 找到数据中最小的日期。

   - 使用 `moment()` 获取当前日期。

   - 生成从最小日期到当前日期的完整日期范围 `dateRange`。

4. **填充缺失数据**：

   - 遍历每组数据，使用 `map` 方法生成包含完整日期范围且填充缺失数据的数组 `filledData`。

   - 在日期范围内查找匹配的日期，如果找不到则填充计数为 0 的对象。

5. **BizCharts 配置**：

   - 使用 `timeCat` 类型的 `scale` 确保时间轴连续。

   - 使用 `Chart` 组件绘制图表，`Geom` 组件绘制线和点。

6. **渲染图表**：

   - 将 `filledData` 传递给 `Chart` 组件，并配置 `Axis`、`Tooltip` 和 `Geom` 组件来绘制图表。

这样，`BizCharts` 将显示一个时间连续的图表，即使某些日期的数据缺失也会自动补0。