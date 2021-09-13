# Starbot

![尘宝最棒了！](http://175.24.71.180/wp-content/uploads/2021/09/01acb54d-c8f9-4b07-bd28-65369dce49c3.jpg "尘宝最棒了！🌟")

基于go-cqhttp的QQ机器人，使用Python编写。

---

## 目录
### · 简介
### · 自行编译

---

## 简介

Starbot诞生的初衷是方便我工作，维护工作的QQ客服群每天重复的问题太多了，脚本/程序的自动回复减少很多不必要的重复工作。完成了基础的工作所需内容，经过一定的扩展以后，它成了现在这个样子。

参考项目：[Yang9999999大佬的 Yes酱](https://github.com/Yang9999999/Go-CQHTTP-YesBot)

### 目前实现了以下功能：

* 常规功能
  * 色图发送
  * 群关键词回复
  * 私聊关键词回复
  * 快捷添加回复内容
  
* 管理功能（机器人账号需要是群管理）
  * 群踢人
  * 群单人禁言
  * 群全体禁言
  * 设置群管理员（需要是群主）
  * 设置群名片
  * 修改群名
  * 设置群专属头衔（需要是群主） *pre*
  * 群文件上传 *pre*
  * 发送群公告
  
### 下个版本会加/完善的功能：

* 常规功能
  * 定时消息
  * 事件检测式群回复
  * 群文件直链获取
  * 群文件上传

### 不知道哪个版本会加的功能：

* 常规功能
  * 合并转发
  * 根据规则自动设置精华消息
  * 设置Bot在线机型
  * 退群（？没太懂这个接口有什么用）
  
* 管理功能  
  * 匿名用户禁言
  * 移除精华消息
  * 按规则处理加群申请
  * 按规则处理好友申请
  
### 其他

消息匹配和回复，使用的是SQLite/MySQL。master分支为SQLite Ver，MySQL在隔壁分支。没有特殊需求的话使用master分支就行了。

代码写的很屎，别骂，只是出于爱好学编程，接受批评但不接受阴阳怪气或者出口成脏。

---

## 自行编译

很显然，你可以下载源码自行修改，这个项目是基于GPL3协议的，请遵守协议。

修改编译需要注意以下内容：

如果你仅仅只是修改源码，直接使用.py文件，那么没有什么问题。如果你需要将它自行打包，请记得分词使用的jieba库在使用Pyinstaller打包时会出现问题，你需要修改tfidf源码，请自己百度。

