---
title: Intellij IDEA运行前报错Command line is too long
layout: info
commentable: true
date: 2021-04-08
mathjax: true
mermaid: true
tags: [软件,IDE,idea]
categories: [软件,IDE]
description: 
---

### 报错内容

Error running ‘HelloWorld’: Command line is too long. Shorten command line for HelloWorld or also for Application default configuration.

### 解决方法

修改项目下 .idea\workspace.xml，找到标签

```xml
<component name="PropertiesComponent">
```

在标签里加一行

```xml
 <property name="dynamic.classpath" value="true" />
```

如下图所示：

```xml
  <component name="PropertiesComponent">
    <property name="RunOnceActivity.OpenProjectViewOnStart" value="true" />
    <property name="last_opened_file_path" value="$PROJECT_DIR$/src/test/java/com/XXX/util" />
    <property name="project.structure.last.edited" value="Global Libraries" />
    <property name="project.structure.proportion" value="0.0" />
    <property name="project.structure.side.proportion" value="0.2" />
    <property name="dynamic.classpath" value="true" />
  </component>
```

也有可能是以下样式：

```xml
<component name="PropertiesComponent"><![CDATA[{
  "keyToString": {
    "RunOnceActivity.OpenProjectViewOnStart": "true",
    "RunOnceActivity.ShowReadmeOnStart": "true",
    "settings.editor.selected.configurable": "preferences.pluginManager"
  }
}]]></component>
```

添加以下内容即可：

    "dynamic.classpath": "true"

最终展示效果为：

```xml
<component name="PropertiesComponent"><![CDATA[{
  "keyToString": {
    "RunOnceActivity.OpenProjectViewOnStart": "true",
    "RunOnceActivity.ShowReadmeOnStart": "true",
    "settings.editor.selected.configurable": "preferences.pluginManager",
    "dynamic.classpath": "true"
  }
}]]></component>
```
