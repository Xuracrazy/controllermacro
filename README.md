# controllermacro

<!-- latest-update:start -->
## Latest update - v1.2.7 (2026-09-28)

- Fixed: L3-to-R2 game binds could be accompanied by a Windows browser shortcut from another controller mapping layer. ControllerMacro now suppresses browser-key events that arrive immediately around an L3 press while preserving the L3 -> R2 macro.
- New app icon (the controller). The exe file's own icon changes after you rebuild the exe with installer.bat.
- Fixed: the window could not be dragged around the screen. The controller reader no longer interferes with Windows' window moving.
- Removed: the old "Wait for L3 first" arming feature. Macros are active immediately when the app starts or reconnects.
- New: redesigned ControllerMacro UI with a dark gaming dashboard, controller mapping view, profiles, macro cards, and connection status.
- New: long press as a trigger option (choose how many milliseconds to hold). The hold time setting is still there.
- New: "Auto Repeat and Toggle" section in every bind - auto repeat (times per second or seconds per repeat), optional start delay, and toggle ON/OFF.
- Faster and lighter: less CPU while idle, and lower memory use (no audio/video/font startup, tray libraries load only when needed, smaller compiled file).

Earlier versions: [CHANGELOG.md](CHANGELOG.md)
<!-- latest-update:end -->
