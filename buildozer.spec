[app]

# 应用名称 (显示在手机上的名字)
title = 十二生肖注册机器人

# 包名 (唯一标识)
package.name = zodiacregister
package.domain = com.qiqi

# 源代码目录
source.dir = .
source.include_exts = py,json,txt

# 版本号
version = 1.0.0

# 依赖 (添加了requests)
requirements = python3,kivy,requests

# Android 配置
android.permissions = android.permission.INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

# 屏幕方向
orientation = portrait
fullscreen = 0

# Android 特定
android.accept_sdk_license = True
android.encoding = utf-8
android.release_artifact = apk

# 日志级别
android.logcat_filters = *:S python:D

[buildozer]
# 关键配置：不警告 root 用户
warn_on_root = 0
log_level = 2
