<p align="center">
<img width="40%" src="https://summer-publiced.oss-cn-hangzhou.aliyuncs.com/logos/logo_transparent.png"/>
</p>
<h1 align="center">Aestate-Json 一款强大的json解析器</h1>

# 介绍

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;从 `Aestate Framework`分离出来的Json解析器，其强大程度可以让你无限套娃。  
功能：将`object`对象转换成Json字符串的形式。为达到能够像`mybatis`这样的神仙级操作我一直在不断地努力， 也有很多的不足之处 ， 希望各位多多提问题，我会认真看完每一个issues

# 安装

> pip 命令：pip install aestate-json  
> anaconda 安装:conda install aestate-json
>

# 使用教程

与原版的教程一致，你可以使用

```python
from ajson.ajson import Json

# 加载json字符串为dict字典格式
Json.loads()
# 加载数据为json字符串
Json.dumps()
```

拓展的方法：

```python
from ajson import aj

# 将任意对象转换成json字符串
a = aj.parse(obj='任意对象', bf='是否美化json', end_load='是否转成json后再转为dict字典')
# 将json字符串转字典
a = aj.load(a)
```

使用示例的代码你会发现，这个工具类可以无限套娃

# CACode Development Team

> Last edit time:2021/06/01 05:30 Asia/Shanghai   
> [👉 Go to canotf`s homepage on Gitee 👈](https://gitee.com/canotf)