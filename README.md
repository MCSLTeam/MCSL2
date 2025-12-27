<!-- markdownlint-disable MD033 -->

![Header Image](https://socialify.git.ci/MCSLTeam/MCSL2/image?description=1&descriptionEditable=一个简洁全能的%20Minecraft%20服务器启动器&font=Jost&forks=1&language=1&logo=https%3A%2F%2Fimages.mcsl.com.cn%2Fnew%2FMCSL2.png&name=1&pattern=Circuit%20Board&stargazers=1&theme=Auto)  

# MCServerLauncher 2  

一个简洁全能的 Minecraft 服务器启动器

<div>
    <a href="https://github.com/MCSLTeam/MCSL2/forks">
        <img src="https://img.shields.io/github/forks/MCSLTeam/MCSL2?style=for-the-badge" alt="Fork">
    </a>
    <br>
    <a href="https://github.com/MCSLTeam/MCSL2/releases">
        <img src="https://img.shields.io/github/downloads/MCSLTeam/MCSL2/total?style=for-the-badge" alt="Downloads">
    </a>
    <a href="https://github.com/MCSLTeam/MCSL2/releases/latest">
        <img src="https://img.shields.io/github/v/tag/MCSLTeam/MCSL2?label=ver&style=for-the-badge" alt="Version">
    </a>
    <a href="mailto:services@mcsl.com.cn">
        <img src="https://img.shields.io/badge/%20CONTACT-services%40mcsl.com.cn-%2357728B?style=for-the-badge" alt="Email">
    </a>
</div>

<div style="text-align: right;">
<a href="https://github.com/MCSLTeam/MCSL2/blob/master/README_EN.md" target="_blank">English</a>  |  中文
</div>

___

## 他能干什么？  

- **👨🏻‍💻面向各阶用户**： 提供简易模式、进阶模式、导入模式，满足各阶用户的需求。  
- **💻界面简洁美观**： 以Fluent Design设计语言为基础，提供简洁、美观的界面。  
- **⏬一键下载资源**： 接入FastMirror、MCSL-Sync、极星镜像站，飞速下载所需。  
- **✅自动查找Java**： 开服界首创查找Java算法，在1-2s内即可完成搜索。  
- **🎞️多服务器管理**： 一站式管理服务器，助力高效提升。  
- **🔧自研插件系统**： 利用Python特性实现，无限可能。  

## 用到的开源项目

请查看 [此处](https://github.com/MCSLTeam/MCSL2/blob/master/pyproject.toml)  

## 从源码构建打包版

```bash
git clone https://github.com/MCSLTeam/MCSL2.git
uv sync

uv run python -m lndl_nuitka .
或者
uv run python -m lndl_nuitka . -y
又或者通过 `-- --xxx` 添加 / 修改参数
uv run python -m lndl_nuitka . -- --disable-console
```
## 相关链接

MCSL 2 官网: <https://mcsl.com.cn>  
GitHub Issue: <https://github.com/MCSLTeam/MCSL2/issues>  
QQ 官方群聊: <https://mcsl.com.cn/links/mcsl2-qq-group.html>  
GPLv3 开源协议: <https://github.com/MCSLTeam/MCSL2/blob/master/LICENSE>  
QFluentWidgets: <https://qfluentwidgets.com>

## 鸣谢

请前往<https://mcsl.com.cn/>查看相关链接。

还有所有的贡献者们！  

<a href="https://github.com/MCSLTeam/MCSL2/graphs/contributors"><img src="https://contrib.rocks/image?repo=MCSLTeam/MCSL2&anon=1&max=100000000"></a>

还有，赞助者们！  
[赞助者列表](https://github.com/MCSLTeam/MCSL2/blob/master/Sponsors.md)

## 声明

本开源项目完全免费，任何倒卖等行为必究。
