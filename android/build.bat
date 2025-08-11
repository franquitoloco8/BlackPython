@echo off
kotlinc android/payload.kt -include-runtime -d android/payload.jar
d8 android/payload.jar --output android/
move android\classes.dex android\payload.apk
echo [+] APK generado: android\payload.apk
