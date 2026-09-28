# Changelog

## v1.2.8 - 2026-09-28

- Fixed: L3-to-R2 game binds could be accompanied by a Windows browser shortcut from another controller mapping layer. ControllerMacro now suppresses browser-key events that arrive immediately around an L3 press while preserving the L3 -> R2 macro.
- New app icon (the controller). The exe file's own icon changes after you rebuild the exe with installer.bat.
- Fixed: the window could not be dragged around the screen. The controller reader no longer interferes with Windows' window moving.
- Removed: the old "Wait for L3 first" arming feature. Macros are active immediately when the app starts or reconnects.
- New: premium neon gaming dashboard UI matching the supplied reference style: dark glass panels, yellow/blue accents, controller-focused mapping view, profile controls, active macro cards, and status footer.
- New: long press as a trigger option (choose how many milliseconds to hold). The hold time setting is still there.
- New: "Auto Repeat and Toggle" section in every bind - auto repeat (times per second or seconds per repeat), optional start delay, and toggle ON/OFF.
- Faster and lighter: less CPU while idle, and lower memory use (no audio/video/font startup, tray libraries load only when needed, smaller compiled file).

## v1.2.7 - 2026-09-28

- Fixed: L3-to-R2 game binds could be accompanied by a Windows browser shortcut from another controller mapping layer. ControllerMacro now suppresses browser-key events that arrive immediately around an L3 press while preserving the L3 -> R2 macro.
- New app icon (the controller). The exe file's own icon changes after you rebuild the exe with installer.bat.
- Fixed: the window could not be dragged around the screen. The controller reader no longer interferes with Windows' window moving.
- Removed: the old "Wait for L3 first" arming feature. Macros are active immediately when the app starts or reconnects.
- New: redesigned ControllerMacro UI with a dark gaming dashboard, controller mapping view, profiles, macro cards, and connection status.
- New: long press as a trigger option (choose how many milliseconds to hold). The hold time setting is still there.
- New: "Auto Repeat and Toggle" section in every bind - auto repeat (times per second or seconds per repeat), optional start delay, and toggle ON/OFF.
- Faster and lighter: less CPU while idle, and lower memory use (no audio/video/font startup, tray libraries load only when needed, smaller compiled file).

## v1.2.6 - 2026-09-28

- Fixed: L3-to-R2 game binds could be accompanied by a Windows browser shortcut from another controller mapping layer. ControllerMacro now suppresses browser-key events that arrive immediately around an L3 press while preserving the L3 -> R2 macro.
- New app icon (the controller). The exe file's own icon changes after you rebuild the exe with installer.bat.
- Fixed: the window could not be dragged around the screen. The controller reader no longer interferes with Windows' window moving.
- Fixed: buttons doing things before you pressed L3. Macros now wait for your first L3 press after the app starts or the controller reconnects (untick "Wait for L3 first" to turn this off). Held or queued outputs are cleared on start.
- New: long press as a trigger option (choose how many milliseconds to hold). The hold time setting is still there.
- New: "Auto Repeat and Toggle" section in every bind - auto repeat (times per second or seconds per repeat), optional start delay, and toggle ON/OFF.
- Faster and lighter: less CPU while idle, and lower memory use (no audio/video/font startup, tray libraries load only when needed, smaller compiled file).

## v1.2.5 - 2026-09-28

- Updated the app.

## v1.2.4 - 2026-09-28

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

## v1.2.3 - 2026-09-28

- New: keyboard keys can now be bound as macro inputs for virtual controller buttons. Keyboard detection works globally, even when Controller Macro is minimized or another app has focus.
- Changed: removed the "Wait for L3 first" option. Macros now simply wait for each bind's configured "When I press" input, with no startup or reconnect arming step.
- New app icon (the controller). The exe file's own icon changes after you rebuild the exe with installer.bat.
- Fixed: the window could not be dragged around the screen. The controller reader no longer interferes with Windows' window moving.
- New: long press as a trigger option (choose how many milliseconds to hold). The hold time setting is still there.
- New: "Auto Repeat and Toggle" section in every bind - auto repeat (times per second or seconds per repeat), optional start delay, and toggle ON/OFF.
- Faster and lighter: less CPU while idle, and lower memory use (no audio/video/font startup, tray libraries load only when needed, smaller compiled file).

## v1.2.2 - 2026-09-27

- Changed: removed the "Wait for L3 first" option. Macros now simply wait for each bind's configured "When I press" input, with no startup or reconnect arming step.
- New app icon (the controller). The exe file's own icon changes after you rebuild the exe with installer.bat.
- Fixed: the window could not be dragged around the screen. The controller reader no longer interferes with Windows' window moving.
- New: long press as a trigger option (choose how many milliseconds to hold). The hold time setting is still there.
- New: "Auto Repeat and Toggle" section in every bind - auto repeat (times per second or seconds per repeat), optional start delay, and toggle ON/OFF.
- Faster and lighter: less CPU while idle, and lower memory use (no audio/video/font startup, tray libraries load only when needed, smaller compiled file).

## v1.2.1 - 2026-09-27

- Rebuilt the app (no code changes).

## v1.2.0 - 2026-09-27

- New app icon (the controller). The exe file's own icon changes after you rebuild the exe with installer.bat.
- Fixed: the window could not be dragged around the screen. The controller reader no longer interferes with Windows' window moving.
- Fixed: buttons doing things before you pressed L3. Macros now wait for your first L3 press after the app starts or the controller reconnects (untick "Wait for L3 first" to turn this off). Held or queued outputs are cleared on start.
- New: long press as a trigger option (choose how many milliseconds to hold). The hold time setting is still there.
- New: "Auto Repeat and Toggle" section in every bind - auto repeat (times per second or seconds per repeat), optional start delay, and toggle ON/OFF.
- Faster and lighter: less CPU while idle, and lower memory use (no audio/video/font startup, tray libraries load only when needed, smaller compiled file).

## v1.1.8 - 2026-09-27

- Fixed: pressing L3 again while R2 was still being held from the last press was ignored, so it sometimes seemed not to go through. Now the press restarts the hold (R2 lets go for a split second so the game sees a fresh press, then holds again).
- Fixed: a controller that disconnected while a bind was held could leave that bind stuck and stop it from firing again.
- Fixed: trigger/stick inputs could stop responding after a controller disconnect and reconnect.

## v1.1.7 - 2026-09-27

- Rebuilt the app (no code changes).

## v1.1.6 - 2026-09-27

- Updated the app.

