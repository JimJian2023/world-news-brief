# World News Brief — Android App

## Build Instructions

### Prerequisites
- Android Studio Hedgehog (2023.1) or later
- JDK 17
- Android SDK 34

### Build APK

**Option 1: Android Studio**
1. Open `android/` folder in Android Studio
2. Wait for Gradle sync to complete
3. Build → Build Bundle(s) / APK(s) → Build APK(s)
4. APK will be at `app/build/outputs/apk/debug/app-debug.apk`

**Option 2: Command line**
```bash
cd android
./gradlew assembleDebug
# APK: app/build/outputs/apk/debug/app-debug.apk
```

### Install
- Transfer APK to your phone
- Enable "Install from unknown sources"
- Open APK file to install

## Features
- Loads the live World News Brief website in a WebView
- Dark-themed native UI shell
- Auto-refresh (pulls latest news from GitHub Pages)
- External links open in browser
- Status bar at top with app title
- Bottom bar with browser shortcut and schedule info

## Tech Stack
- Kotlin + Jetpack Compose
- Material 3 (dark theme)
- WebView for content rendering
- Min SDK: 26 (Android 8.0)
- Target SDK: 34 (Android 14)

## Future Enhancements
- [ ] Offline caching of news
- [ ] Push notifications for breaking news
- [ ] Native article reading view (no WebView)
- [ ] Widget for home screen
