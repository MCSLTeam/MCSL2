### 新功能

> 添加 macOS 发行版构建支持，提供 app 与 dmg 安装包
> 添加 macOS Developer ID 签名与公证流程，未配置 secrets 时会自动跳过
> 添加 macOS DMG 自定义背景、卷宗图标和拖拽安装布局
> 添加 Windows arm64 构建尝试
> 新建服务器、管理服务器、监控页面适配窄窗口布局
> 新建服务器类型卡片、管理服务器卡片、Java 选择卡片支持自适应排列

### 改进

> 使用 deploy.py 统一 Nuitka 打包流程
> Nuitka 升级到 4.1.2
> 更新 GitHub Actions 使用的 action 版本
> macOS 打包使用 MCSL2.icns，并设置应用标识 cn.mcslteam.mcsl2
> macOS 应用写入版本号，并禁止多实例启动
> 构建时定期输出 Nuitka 状态，避免 GitHub Actions 因长时间无日志中断
> 保留升级包生成、release 上传、环境变量写入和包体清理流程
> 关于页面声明、按钮区域和多处卡片文本改为自适应高度，避免不同平台字体被裁切
> 关于页面声明下方按钮改为 FlowLayout
> 首页公告功能已移除
> 移除 countUser、checkUpdate、generateUniqueCode 等启动联网功能
> 固定 PyQt-Fluent-Widgets 依赖版本，减少打包环境差异

### 修复

> 修复下载器进度可能一直停在 0% 的问题
> 修复日志 critical 传入字符串时再次抛出异常的问题
> 修复断网时启动流程可能被联网统计阻塞的问题
> 修复 NeoForge 源码安装时 sponge-mixin 等库文件被重复占用的问题
> 修复设置关于页、新建服务器卡片、Java 选择卡片和管理服务器卡片在部分字体下文字被 padding 裁切的问题

___

### 其他下载地址

<https://v2.mcsl.com.cn/download.html>
