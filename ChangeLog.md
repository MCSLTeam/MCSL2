### 新功能
###### 暂无
### 修复
 - 修复了程序启动时因找不到MCSL2/Logs目录而无法创建日志并无法运行的问题
 - ~~版本更新（假想）~~ 后若添加新的配置文件选项，而旧版的配置文件缺失此项导致无法启动程序，对此进行了修补
 - MCSL2_Dialog修改UI使其自适应，防止对话框内容过多导致的文字溢出或被遮盖
 - 修复程序启动时因找不到MCSL2/MCSL2_Config.json或MCSL2_ServerList.json而无法读取配置并无法运行的问题
 - 修复了设置页UI与实际配置不同的问题
### 优化
 - 采取了[StarryCamile](https://github.com/StarryCamile)的意见，将配置文件的DarkMode修改为ThemeMode较为合理
 - 添加了需要联网的代码的容错机制，防止因网络错误/无网络导致的程序崩溃
 - 在在下载界面刷新时添加ProgressBar和提示防止用户以为卡死了（感谢PyQt-Fluent-Widgets）
