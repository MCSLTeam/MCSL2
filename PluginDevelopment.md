# <center> 插件编写文档 </center>
## 0. 同意插件eula.txt
#### 条款内容：<font color='#e14242'>如果用户下载恶意插件而造成的后果，MCSL2 不承担责任 </font>
## 1. 插件的基本原理
#### 在 MCSL2 中，插件即是 一个 Plugin 类。MCSL2 会在导入时对这些类做一些特殊的处理使得他们成为一个插件。插件间应尽量减少耦合，可以进行有限制的相互调用 ,使得 MCSL2 能够正确解析插件间的依赖关系。
## 2. 插件的基本实现
#### 下边是一个最简单的Plugin，不过别着急，看完之后我们还要配置文件
```python
#实现一个Plugin类
test = Plugin() 
def load():
    """写你的代码"""
    print("load")
#注册加载代码
test.register_loadFunc(load)
def enable():
    """写你的代码"""
    print("enable")
#注册应用代码
test.register_enableFunc(enable)
def disable():
    """写你的代码"""
    print("disable")
#注册应用代码
test.register_disableFunc(disable)
```
#### MCSL2的 配置文件 使用美观性和易上手性中比较中间的语法 json ，下图是一个较为简单是配置文件，如果想深入了解请 <a href="https://github.com//MCSLTeam//MCSL2">点击这里</a>
#### <font color='#e14242'> 注意！！！ plugin_name 必须与Plugin类所在的py文件名字相同，并且Plugin类的名字也要是 plugin_name </font>
```json
{
  //插件名字 
  "plugin_name": "test",
  //插件版本
  "version": "0.0.0",
  //插件介绍
  "description": "test测试插件",
  //插件的显示图标
  "icon": "Cloth.png",
  //作者
  "author": "rc",
  //作者邮箱
  "author_email": "rc@163.com",
  //是否开启一个新的线程来运行此插件
  "on_new_thread": false
}
```
#### 最后将其放进 Plugins//plugin_name 便可食用了

## 3. 事件系统
咕咕咕
## 4. 调用 MCSL2 内的函数
咕咕咕
