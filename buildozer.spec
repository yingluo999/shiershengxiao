[app]

# 应用名称
title = 十二生肖注册机器人

# 包名
package.name = zodiacregister
package.domain = com.qiqi

# 源代码目录
source.dir = .
source.include_exts = py,json,txt

# 版本号
version = 1.0.0

# 依赖
requirements = python3,kivy,requests

# Android 权限
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# API 版本
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

# 允许访问外部存储（Android 10+ 兼容）
android.manifest.application.android:requestLegacyExternalStorage = true

# 屏幕方向
orientation = portrait
fullscreen = 0

# Android 特定
android.accept_sdk_license = True
android.encoding = utf-8
android.release_artifact = apk

[buildozer]
warn_on_root = 0
log_level = 2
