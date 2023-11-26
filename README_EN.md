[![MCSL 2 Title Image](https://s3.bmp.ovh/imgs/2023/03/21/5afb21934bd980ab.png)](https://mcsl.com.cn)

# MCSL2 | A simple and multifunctional Minecraft server launcher

<right>
——Made by MCSL Team
</right>

___

<center>
<a href="https://github.com/MCSLTeam/MCSL2" target="_blank">中文</a>  |  English
</center>

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

## What can MCSL2 do?  

- **💻 Simple and beautiful interface**: Written with PyQt5, and a fluent design widgets library[PyQt-Fluent-Widgets](https://www.github.com/zhiyiYo/PyQt-Fluent-Widgets)  
- **🎞️ Multiple servers can be managed**: Multi-server centralized management, more efficient operation and maintenance  
- **⏬ All-in-One download service**: Download a variety of resources from FastMirror and MCSLAPI with Aria2.  
- **⚡ Quickly add a server**: A few options to quickly add a new server!
- **✅ Automatic find Java**: Automatically find the vast majority of Java without manual selection.  
- **🔧 Extended tool system**: Use various kinds of extension to make your MCSL2 more powerful.  

___

## Used open-source project

`Python` 3.8
`Nuitka` Latest  
`requests` Latest  
`PyQt5` 5.15.10
`PyQt-Fluent-Widgets` Latest  
`aria2p` Latest  
`lib-not-dr` 0.2.x
`loguru` 0.7.2  
`psutil` 5.9.5  
___

## Build a packaged version from source code

- git clone
- `pip install tomli`
- `python Tools/gen-requirements.py`
- `python -m pip install -U -r requirements.txt`
- `python Tools/update-pyproject.py`
- `python -m lndl_nuitka .`
  - or
  - `python -m lndl_nuitka . -y`
  - or use `-- --xxx` to add / modify parameters
  - `python -m lndl_nuitka . -- --disable-console`

___

## Related link

MCSL 2 Official Website:[https://mcsl.com.cn](https://mcsl.com.cn)  
GitHub Issue:[https://github.com/MCSLTeam/MCSL2/issues](https://github.com/MCSLTeam/MCSL2/issues)  
QQ Group:[https://jq.qq.com/?k=b6NlRcJn](https://jq.qq.com/?k=b6NlRcJn)  
GNU General Public License v3.0:[https://github.com/MCSLTeam/MCSL2/blob/master/LICENSE](https://github.com/MCSLTeam/MCSL2/blob/master/LICENSE)
___

## Special Thanks

- 维度前端: <https://www.df100.ltd>
- Z_Tsin: <https://ztsin.cn/>
- FiveCDN公益加速: <https://cdn.5-5.site>
- WB-Block: <https://wb-block.top>
- shenjack: <http://shenjack.top:81>

And all the contributors!  

<a href="https://github.com/MCSLTeam/MCSL2/graphs/contributors"><img src="https://contrib.rocks/image?repo=MCSLTeam/MCSL2&anon=1&max=100000000"></a>

And our sponsors!  
[Sponsor List](https://github.com/MCSLTeam/MCSL2/blob/master/Sponsors.md)
___

## Declaration  

This open source project is completely free, and any resale or similar behavior will be held accountable.
