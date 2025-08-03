[app]
title = ML Budget App
package.name = mlbudgetapp
package.domain = org.mlbudgetapp
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0

requirements = python3,kivy,numpy,scikit-learn,pandas,matplotlib

orientation = portrait
fullscreen = 0

# Android specific settings
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 29
android.minapi = 21
android.ndk = 23b
android.sdk = 29
android.arch = arm64-v8a

# iOS specific settings (if needed)
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.7.0

[buildozer]
log_level = 2
warn_on_root = 1 