[![MCSL 2 大头图](https://s3.bmp.ovh/imgs/2023/03/21/5afb21934bd980ab.png)](https://mcsl.netlify.app)
# MCSL2   |   一个简洁全能的 Minecraft 服务器启动器

<div style="text-align: right;">
——由LxHTT倾心制作
</div>

___

<div style="text-align: center;">
中文  |  <a href="https://github.com/LxHTT/MCSL2/blob/master/README_EN.md" target="_blank">English</a>
</div>

___
[![](https://img.shields.io/github/license/LxHTT/MCSL2 "开源协议")](https://github.com/LxHTT/MCSL2/blob/master/LICENSE)
[![](https://img.shields.io/github/stars/LxHTT/MCSL2 "Star")](https://github.com/LxHTT/MCSL2/stargazers)
[![](https://img.shields.io/github/forks/LxHTT/MCSL2 "Fork")](https://github.com/LxHTT/MCSL2/forks)

![](https://repobeats.axiom.co/api/embed/869c25f269efec38ff69088fca0dc7aba2de63bf.svg "仓库分析")
___
### 他能干什么？  
~~可以帮助你非常方便的开启一个Java版Minecraft服务器。（废话文学~~

 - **💻 简洁美观的界面**： 采用Qt编写，配合自己搓的QSS，由圆角强势驱动（
 - **🎞️ 可管理多服务器**： 一个MCSL2，服务器尽在掌控之中！
 - **⏬ 一站式下载服务**： 由MCSLAPI强力驱动，配合Aria2下载引擎，速度飞起！
 - **⚡ 快速配置服务器**： 几个选项，即可快速配置一个新服务器！
 - **✅ 自动查找Java**： 厌倦了手动翻目录？自动查找Java帮你解决！
 - **🔧 拓展工具系统**： 使用各种拓展工具，让你的MCSL2更加强大！
___
### 相关链接
MCSL 2官网：[https://mcsl.netlify.app](https://mcsl.netlify.app)  
MCSL 2 API官网：[https://mcslapi.netlify.app](https://mcslapi.netlify.app/)  
GitHub Issue：[https://github.com/LxHTT/MCSL2/issues](https://github.com/LxHTT/MCSL2/issues)  
QQ官方群聊：[https://jq.qq.com/?k=b6NlRcJn](https://jq.qq.com/?k=b6NlRcJn)  
作者邮箱：[mailto:lxhtz.dl@qq.com](mailto:lxhtz.dl@qq.com)  
GPLv3开源协议：[https://github.com/LxHTT/MCSL2/blob/master/LICENSE](https://github.com/LxHTT/MCSL2/blob/master/LICENSE)
___
### 鸣谢

- [Luoxis 云存储](https://www.df100.ltd) 来自于 **星姮十织**
- [ZCloud](https://ztsin.cn/) 来自于 **Z_Tsin**

还有所有的贡献者们！  

<a href="https://github.com/LxHTT/MCSL2/graphs/contributors"><img src="https://contrib.rocks/image?repo=LxHTT/MCSL2&anon=1&max=100000000"></a>
___
## 帮助文档 
~~其实我就不知道该写啥好~~  
本项目基于Python 3.8.0开发。

### 快速上手

#### 0.依赖

MCSL2 依赖 python3 运行环境。请确保你的 python 版本大于 3.6。

其他的依赖可以通过在本仓库中的requirements来安装，可以使用：
```commandline
pip install -r requirements.txt
```
或者
```commandline
pip3 install -r requirements.txt
```
来安装。

#### 1.安装

有以下两种方法来安装MCSL2:

#### 1.1 通过releases安装

在 [Releases](https://github.com/LxHTT/MCSL2/releases) 中选择最新的 Release 并下载对应系统版本的安装包。

#### 1.2 通过克隆本仓库来安装

可以通过:

```commandline
git clone https://github.com/LxHTT/MCSL2.git
```
来克隆本仓库。

### 2.启动

在 Windows 系统中，将MCSL2.exe放置到拥有可写入权限的文件夹中。

在第一次启动后，会自动生成 MCSL2 与 Servers 文件夹。

### 3.构建服务器

转到配置服务器页面，点击Java部分的自动查找按钮，将自动查找所有可用的 Java 。

点击 Java列表 选择合适的Java版本。

#### 或者

转到下载页面，下载合适的Java版本。

再在下面输入预计分配的最小内存与最大内存。

接下来选择服务器核心（同上，可以在软件中下载）

最后输入服务器名称

再点击存储，即可。


### 好了就是酱紫 直接开始~~摆烂~~**开发**