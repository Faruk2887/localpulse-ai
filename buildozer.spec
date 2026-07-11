[app]
title = LocalPulse AI
package.name = localpulseai
package.domain = com.localpulseai
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 1.0.0
requirements = python3,kivy,kivymd,requests,pillow,android
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE,VIBRATE,BILLING
android.api = 33
android.minapi = 26
android.ndk = 25b
android.allow_backup = True
android.presplash_color = #4F46E5

[buildozer]
log_level = 2
warn_on_root = 1
