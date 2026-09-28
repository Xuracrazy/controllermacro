# Changelog

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

