# controllermacro

<!-- latest-update:start -->
## Latest update - v1.2.4 (2026-09-28)

- Fixed: rebuilt executables now force-refresh the Windows Explorer icon cache after the build so the new controller icon is visible instead of a cached old icon.
- Changed: installer explicitly validates and applies ControllerMacro.ico to the PyInstaller build.
- Changed: replaced the application icon with the supplied DualSense-style controller artwork. The same icon is embedded in the Windows executable and the app window.
- New: keyboard keys can now be bound as macro inputs for virtual controller buttons. Keyboard detection works globally, even when Controller Macro is minimized or another app has focus.
- Changed: removed the "Wait for L3 first" option. Macros now simply wait for each bind's configured "When I press" input, with no startup or reconnect arming step.
- New app icon (the controller). The exe file's own icon changes after you rebuild the exe with installer.bat.
- Fixed: the window could not be dragged around the screen. The controller reader no longer interferes with Windows' window moving.
- New: long press as a trigger option (choose how many milliseconds to hold). The hold time setting is still there.
- New: "Auto Repeat and Toggle" section in every bind - auto repeat (times per second or seconds per repeat), optional start delay, and toggle ON/OFF.
- Faster and lighter: less CPU while idle, and lower memory use (no audio/video/font startup, tray libraries load only when needed, smaller compiled file).

Earlier versions: [CHANGELOG.md](CHANGELOG.md)
<!-- latest-update:end -->
