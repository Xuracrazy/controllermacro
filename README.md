# controllermacro

<!-- latest-update:start -->
## Latest update - v1.2.0 (2026-09-27)

- New app icon (the controller). The exe file's own icon changes after you rebuild the exe with installer.bat.
- Fixed: the window could not be dragged around the screen. The controller reader no longer interferes with Windows' window moving.
- Fixed: buttons doing things before you pressed L3. Macros now wait for your first L3 press after the app starts or the controller reconnects (untick "Wait for L3 first" to turn this off). Held or queued outputs are cleared on start.
- New: long press as a trigger option (choose how many milliseconds to hold). The hold time setting is still there.
- New: "Auto Repeat and Toggle" section in every bind - auto repeat (times per second or seconds per repeat), optional start delay, and toggle ON/OFF.
- Faster and lighter: less CPU while idle, and lower memory use (no audio/video/font startup, tray libraries load only when needed, smaller compiled file).

Earlier versions: [CHANGELOG.md](CHANGELOG.md)
<!-- latest-update:end -->
