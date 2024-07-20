# Android

### generate apk self signing keystore and use it

```
# gen it once
keytool -genkey -v -keystore my-release-key.keystore -alias alias_name -keyalg RSA -keysize 2048 -validity 10000

# use it often
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore /home/ellcs/ui-experiments/test/my-release-key.keystore dist/APKey.apk alias_name
```

### use apktool to decompile apk to smali and recompile it again

```
# decompile; source code in smali folder
apktool d -o out2 -r -f APKey.apk

# recompile; self sign it to install it
apktool b .
```

### setup and start avd 

```
./cmdline-tools/latest/bin/sdkmanager --install 'system-images;android-23;google_apis;x86_64'

./cmdline-tools/latest/bin/avdmanager create avd -n test --abi google_apis/x86_64 --package 'system-images;android-23;google_apis;x86_64'

./emulator/emulator @test
```
