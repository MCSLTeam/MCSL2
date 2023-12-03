[![MCSL 2 大头图](https://s3.bmp.ovh/imgs/2023/03/21/5afb21934bd980ab.png)](https://www.mcsl.com.cn)

# MCSL2   |   一个简洁全能的 Minecraft 服务器启动器

<right>
——由MCSL Team倾心制作
</right>

___

<div style="text-align: center;">
中文  |  <a href="https://github.com/MCSLTeam/MCSL2/blob/master/README_EN.md" target="_blank">English</a>
</div>

___
[![License](https://img.shields.io/github/license/MCSLTeam/MCSL2?style=for-the-badge "License")](https://github.com/MCSLTeam/MCSL2/blob/master/LICENSE)
[![Star](https://img.shields.io/github/stars/MCSLTeam/MCSL2?style=for-the-badge "Star")](https://github.com/MCSLTeam/MCSL2/stargazers)
[![Fork](https://img.shields.io/github/forks/MCSLTeam/MCSL2?style=for-the-badge "Fork")](https://github.com/MCSLTeam/MCSL2/forks)
[![Actions](https://img.shields.io/github/actions/workflow/status/MCSLTeam/MCSL2/build.yml?label=Build&style=for-the-badge "Actions")](https://github.com/MCSLTeam/MCSL2/actions)  
[![Downloads](https://img.shields.io/github/downloads/MCSLTeam/MCSL2/total?style=for-the-badge "Downloads")](https://github.com/MCSLTeam/MCSL2/releases)
[![Version](https://img.shields.io/github/v/tag/MCSLTeam/MCSL2?label=ver&style=for-the-badge "Version")](https://github.com/MCSLTeam/MCSL2/releases/latest)
[![Issues](https://img.shields.io/github/issues/MCSLTeam/MCSL2?style=for-the-badge "Issues")](https://github.com/MCSLTeam/MCSL2/issues)  
[![Website](https://img.shields.io/badge/offical-website-gray.svg?style=for-the-badge "Website")](https://mcsl.com.cn)
[![LxHTT's Email](https://img.shields.io/badge/%20EMAIL-lxhtt%40vip.qq.com-%2357728B?style=for-the-badge)](mailto:lxhtt@vip.qq.com)  
___

## 他能干什么？  

- **💻 简洁美观的界面**： 采用PyQt5编写，采用Fluent Design设计风格的[PyQt-Fluent-Widgets](https://www.github.com/zhiyiYo/PyQt-Fluent-Widgets)组件库  
- **🎞️ 可管理多服务器**： 多服务器集中管理，运维更高效  
- **⏬ 一站式下载服务**： 使用Aria2从FastMirror、MCSLAPI下载各类常用核心  
- **⚡ 快速新建服务器**： 几个选项，即可快速新建一个新服务器  
- **✅ 自动查找Java**： 自动查找绝大多数Java，无需手动选择。  
- **🔧 自研插件系统**： 丰富MCSL2的功能。  

___

## 用到的开源项目

`Python` 3.8
`Nuitka` 最新版  
`requests` 最新版  
`PyQt5` 5.15.10
`PyQt-Fluent-Widgets` 最新版  
`aria2p` 最新版  
`lib-not-dr` 0.2.x
`loguru` 0.7.2  
`psutil` 5.9.5  
___

## 从源码构建打包版

- `git clone https://github.com/MCSLTeam/MCSL2.git`
- `pip install tomli`
- `python Tools/gen-requirements.py`
- `python -m pip install -U -r requirements.txt`
- `python Tools/update-pyproject.py`
- `python -m lndl_nuitka .`
  - 或者
  - `python -m lndl_nuitka . -y`
  - 又或者通过 `-- --xxx` 添加 / 修改参数
  - `python -m lndl_nuitka . -- --disable-console`

___

## 相关链接

MCSL 2官网：[https://mcsl.com.cn](https://mcsl.com.cn)  
GitHub Issue：[https://github.com/MCSLTeam/MCSL2/issues](https://github.com/MCSLTeam/MCSL2/issues)  
QQ官方群聊：[https://jq.qq.com/?k=b6NlRcJn](https://jq.qq.com/?k=b6NlRcJn)  
GPLv3开源协议：[https://github.com/MCSLTeam/MCSL2/blob/master/LICENSE](https://github.com/MCSLTeam/MCSL2/blob/master/LICENSE)
___

## 鸣谢

- 维度前端: <a href="https://www.df100.ltd" target="_blank">https://www.df100.ltd</a>
- Z_Tsin: <a href="https://github.com/Z_Tsin" target="_blank">https://github.com/Z_Tsin</a>
- FiveCDN公益加速: <a href="https://www.5cdn.com" target="_blank">https://www.5cdn.com</a>
- WB-Block: <a href="https://wb-block.com" target="_blank">https://wb-block.com</a>  
- shenjack: <a href="https://github.com/shenjack" target="_blank">https://github.com/shenjack</a>


还有所有的贡献者们！  

<a href="https://github.com/MCSLTeam/MCSL2/graphs/contributors"><img src="https://contrib.rocks/image?repo=MCSLTeam/MCSL2&anon=1&max=100000000"></a>

还有，赞助者们！  
[赞助者列表](https://github.com/MCSLTeam/MCSL2/blob/master/Sponsors.md)
___

## 声明

本开源项目完全免费，任何倒卖等行为必究。
