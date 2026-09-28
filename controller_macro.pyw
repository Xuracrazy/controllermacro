"""
Controller Macro  -  PS5 / Xbox controller binds with profiles
---------------------------------------------------------------
Setup (once):  py -m pip install pygame vgamepad      (ViGEmBus must be installed)
Run:           py controller_macro.py

Reads your real controller (any SDL-supported PS5/Xbox pad) and, when a chosen
input is pressed, presses something on a virtual Xbox 360 controller.
Profiles are saved as .json files in a "profiles" folder next to this script.
"""

import json
import os
import queue
import sys
import time
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import webbrowser

VERSION = "1.1.1"      # bump this number every time you publish a new version

LINKS = {
    "vigem": "https://github.com/nefarius/ViGEmBus/releases",       # required driver
    "hidhide": "https://github.com/nefarius/HidHide/releases",      # optional
    "vcredist": "https://aka.ms/vs/17/release/vc_redist.x64.exe",   # Microsoft C++ runtime
}
HIDHIDE_DIR = r"C:\Program Files\Nefarius Software Solutions\HidHide"


def offer(title, msg, url):
    if messagebox.askyesno(title, msg + "\n\nOpen the download page now?"):
        webbrowser.open(url)


os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"  # work while a game has focus
try:
    import pygame
    from pygame._sdl2 import controller
    import vgamepad as vg
    import pystray
    from PIL import Image, ImageDraw
except Exception as e:
    err = f"{type(e).__name__}: {e}"
    if "VIGEM" in err.upper():
        offer("Driver missing",
              "The virtual controller driver (ViGEmBus) is not installed.\n\n"
              "Install it (restart your PC if the installer asks), then open this app again.",
              LINKS["vigem"])
    elif "DLL" in err.upper():
        offer("Windows component missing",
              f"{err}\n\nThis usually means the Microsoft Visual C++ Redistributable is missing.",
              LINKS["vcredist"])
    else:
        messagebox.showerror("Missing library",
                             f"{err}\n\nIf you run the .pyw directly, open Command Prompt and run:\n"
                             "py -m pip install pygame-ce vgamepad pystray pillow")
    raise SystemExit

# Profiles, settings and error.log live next to THIS script (the "app" folder),
# whether it is run directly or loaded by ControllerMacro.exe.
BASE = os.path.dirname(os.path.abspath(__file__))
PROFILE_DIR = os.path.join(BASE, "profiles")
ACTIVE_FILE = os.path.join(PROFILE_DIR, "_active.txt")
GEO_FILE = os.path.join(PROFILE_DIR, "_window.txt")
VPAD_FILE = os.path.join(PROFILE_DIR, "_virtual.txt")      # auto / xbox / ps
os.makedirs(PROFILE_DIR, exist_ok=True)

# ---- Standard layout (SDL "game controller"), same names for PS5 and Xbox ----
BUTTONS = {
    0: "A (Cross)", 1: "B (Circle)", 2: "X (Square)", 3: "Y (Triangle)",
    4: "Back (Create/View)", 5: "Guide (PS/Xbox)", 6: "Start (Options/Menu)",
    7: "L3", 8: "R3", 9: "LB (L1)", 10: "RB (R1)",
    11: "DPad Up", 12: "DPad Down", 13: "DPad Left", 14: "DPad Right",
    15: "Mute/Share", 16: "Paddle 1", 17: "Paddle 2", 18: "Paddle 3", 19: "Paddle 4",
    20: "Touchpad",
}
TRIGGERS = {4: "LT (L2)", 5: "RT (R2)"}
STICK_DIR = {
    0: ("Left Stick Left", "Left Stick Right"), 1: ("Left Stick Up", "Left Stick Down"),
    2: ("Right Stick Left", "Right Stick Right"), 3: ("Right Stick Up", "Right Stick Down"),
}
INPUTS = (list(BUTTONS.values()) + list(TRIGGERS.values())
          + [n for pair in STICK_DIR.values() for n in pair])

X = vg.XUSB_BUTTON
OUT_BUTTONS = {
    "A (Cross)": X.XUSB_GAMEPAD_A, "B (Circle)": X.XUSB_GAMEPAD_B,
    "X (Square)": X.XUSB_GAMEPAD_X, "Y (Triangle)": X.XUSB_GAMEPAD_Y,
    "Back (Create/View)": X.XUSB_GAMEPAD_BACK, "Guide (PS/Xbox)": X.XUSB_GAMEPAD_GUIDE,
    "Start (Options/Menu)": X.XUSB_GAMEPAD_START,
    "L3": X.XUSB_GAMEPAD_LEFT_THUMB, "R3": X.XUSB_GAMEPAD_RIGHT_THUMB,
    "LB (L1)": X.XUSB_GAMEPAD_LEFT_SHOULDER, "RB (R1)": X.XUSB_GAMEPAD_RIGHT_SHOULDER,
    "DPad Up": X.XUSB_GAMEPAD_DPAD_UP, "DPad Down": X.XUSB_GAMEPAD_DPAD_DOWN,
    "DPad Left": X.XUSB_GAMEPAD_DPAD_LEFT, "DPad Right": X.XUSB_GAMEPAD_DPAD_RIGHT,
}
OUT_TRIGGERS = {"LT (L2)": "left", "RT (R2)": "right"}
OUTPUTS = list(OUT_BUTTONS) + list(OUT_TRIGGERS)

# ---- Same outputs, but for a virtual PlayStation (DualShock 4) pad ----
DPAD_NAMES = ("DPad Up", "DPad Down", "DPad Left", "DPad Right")
VPAD_CHOICES = {"Auto (match my controller)": "auto", "Xbox 360": "xbox",
                "PlayStation (DualShock 4)": "ps"}
SONY_WORDS = ("dualsense", "dualshock", "playstation", "ps5", "ps4", "ps3", "sony", "wireless controller")
try:
    B = vg.DS4_BUTTONS
    DS4_OUT = {
        "A (Cross)": B.DS4_BUTTON_CROSS, "B (Circle)": B.DS4_BUTTON_CIRCLE,
        "X (Square)": B.DS4_BUTTON_SQUARE, "Y (Triangle)": B.DS4_BUTTON_TRIANGLE,
        "Back (Create/View)": B.DS4_BUTTON_SHARE, "Start (Options/Menu)": B.DS4_BUTTON_OPTIONS,
        "L3": B.DS4_BUTTON_THUMB_LEFT, "R3": B.DS4_BUTTON_THUMB_RIGHT,
        "LB (L1)": B.DS4_BUTTON_SHOULDER_LEFT, "RB (R1)": B.DS4_BUTTON_SHOULDER_RIGHT,
    }
    DS4_TRIG_BTN = {"left": B.DS4_BUTTON_TRIGGER_LEFT, "right": B.DS4_BUTTON_TRIGGER_RIGHT}
    DS4_PS = vg.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_PS
    H = vg.DS4_DPAD_DIRECTIONS                    # keys: (up, down, left, right)
    DS4_DPAD_NONE = H.DS4_BUTTON_DPAD_NONE
    DS4_DPAD = {
        (1, 0, 0, 0): H.DS4_BUTTON_DPAD_NORTH, (1, 0, 0, 1): H.DS4_BUTTON_DPAD_NORTHEAST,
        (0, 0, 0, 1): H.DS4_BUTTON_DPAD_EAST, (0, 1, 0, 1): H.DS4_BUTTON_DPAD_SOUTHEAST,
        (0, 1, 0, 0): H.DS4_BUTTON_DPAD_SOUTH, (0, 1, 1, 0): H.DS4_BUTTON_DPAD_SOUTHWEST,
        (0, 0, 1, 0): H.DS4_BUTTON_DPAD_WEST, (1, 0, 1, 0): H.DS4_BUTTON_DPAD_NORTHWEST,
    }
    DS4_OK = True
except Exception:
    DS4_OK = False


class App:
    def __init__(self, root):
        self.root = root
        root.title(f"Controller Macro v{VERSION}")
        root.geometry("640x460")
        try:
            if os.path.exists(GEO_FILE):
                root.geometry(open(GEO_FILE).read().strip())
        except Exception:
            pass
        self.tray = None
        self.tray_q = queue.Queue()   # tray thread -> main thread messages
        root.bind("<Unmap>", self.on_unmap)
        pygame.init()
        controller.init()

        self.pads = {}        # instance_id -> Controller (real pads only)
        self.axis_on = {}     # axis edge detection
        self.holds = {}       # output name -> release time (None = while input held)
        self.listen = None    # callback used by "Detect input"
        self.binds = []
        self.profile = ""
        self.enabled = tk.BooleanVar(value=True)
        self.macros_flag = True
        self.status = tk.StringVar(value="No controller detected yet")
        self.vinfo = tk.StringVar(value="")

        self.vpad = None      # the virtual pad the game sees (Xbox 360 or DualShock 4)
        self.vkind = None     # "x360" or "ds4"
        self.vpad_time = 0    # used to ignore the virtual pad's own "plugged in" event
        self.vpad_error = ""
        self.dpad_held = set()
        self.vsetting = self.read_vsetting()   # auto / xbox / ps
        for i in range(controller.get_count()):
            self.open_pad(i)

        self.build_ui()
        self.load_profiles()
        self.apply_vpad(force=True)
        note = os.environ.get("CM_UPDATE_NOTE")     # set by the launcher after an auto-update
        if note:
            self.status.set(note)
        self.poll()
        root.protocol("WM_DELETE_WINDOW", self.close)
        if not self.vpad:
            root.after(300, lambda: self.show_setup(self.vpad_error))

    # ---------------- UI ----------------
    def build_ui(self):
        top = ttk.Frame(self.root, padding=8)
        top.pack(fill="x")
        ttk.Label(top, text="Profile:").pack(side="left")
        self.combo = ttk.Combobox(top, state="readonly", width=24)
        self.combo.pack(side="left", padx=6)
        self.combo.bind("<<ComboboxSelected>>", lambda e: self.switch(self.combo.get()))
        ttk.Button(top, text="New", command=self.new_profile).pack(side="left")
        ttk.Button(top, text="Delete", command=self.delete_profile).pack(side="left", padx=4)
        ttk.Checkbutton(top, text="Macros ON", variable=self.enabled,
                        command=self.on_toggle).pack(side="right")

        row2 = ttk.Frame(self.root, padding=(8, 0, 8, 4))
        row2.pack(fill="x")
        ttk.Label(row2, text="Virtual pad:").pack(side="left")
        self.vcombo = ttk.Combobox(row2, state="readonly", width=26, values=list(VPAD_CHOICES))
        self.vcombo.pack(side="left", padx=6)
        self.vcombo.set(next(k for k, v in VPAD_CHOICES.items() if v == self.vsetting))
        self.vcombo.bind("<<ComboboxSelected>>", self.on_vpad_choice)
        ttk.Label(row2, textvariable=self.vinfo).pack(side="left", padx=6)
        ttk.Button(row2, text="Setup check", command=self.show_setup).pack(side="right")

        self.tree = ttk.Treeview(self.root, columns=("in", "out", "sec"),
                                 show="headings", height=14)
        for col, title, w in (("in", "When I press", 230), ("out", "Press on virtual pad", 230),
                              ("sec", "Hold", 100)):
            self.tree.heading(col, text=title)
            self.tree.column(col, width=w)
        self.tree.pack(fill="both", expand=True, padx=8)

        bar = ttk.Frame(self.root, padding=8)
        bar.pack(fill="x")
        ttk.Button(bar, text="Add bind", command=lambda: self.bind_dialog()).pack(side="left")
        ttk.Button(bar, text="Edit", command=self.edit_bind).pack(side="left", padx=4)
        ttk.Button(bar, text="Remove", command=self.remove_bind).pack(side="left")
        ttk.Label(self.root, textvariable=self.status, padding=(8, 0, 8, 8)).pack(anchor="w")

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for b in self.binds:
            s = float(b["seconds"])
            self.tree.insert("", "end", values=(b["input"], b["output"],
                                                "while held" if s == 0 else f"{s:g}s"))

    def bind_dialog(self, index=None):
        cur = self.binds[index] if index is not None else {"input": INPUTS[0], "output": OUTPUTS[-1], "seconds": 3}
        d = tk.Toplevel(self.root)
        d.title("Bind")
        d.transient(self.root)
        d.grab_set()
        inp, out = tk.StringVar(value=cur["input"]), tk.StringVar(value=cur["output"])
        sec = tk.StringVar(value=str(cur["seconds"]))
        pad = {"padx": 8, "pady": 5}

        ttk.Label(d, text="When I press:").grid(row=0, column=0, sticky="w", **pad)
        ttk.Combobox(d, textvariable=inp, values=INPUTS, state="readonly", width=26).grid(row=0, column=1, **pad)
        detect = ttk.Button(d, text="Detect input")
        detect.grid(row=0, column=2, **pad)

        def start_detect():
            detect.config(text="Press it now...")
            def got(name):
                inp.set(name)
                detect.config(text="Detect input")
            self.listen = got
        detect.config(command=start_detect)

        ttk.Label(d, text="Press on virtual pad:").grid(row=1, column=0, sticky="w", **pad)
        ttk.Combobox(d, textvariable=out, values=OUTPUTS, state="readonly", width=26).grid(row=1, column=1, **pad)
        ttk.Label(d, text="Hold seconds (0 = while held):").grid(row=2, column=0, sticky="w", **pad)
        ttk.Spinbox(d, from_=0, to=60, increment=0.1, textvariable=sec, width=8).grid(row=2, column=1, sticky="w", **pad)

        def ok():
            try:
                s = float(sec.get())
                assert s >= 0
            except (ValueError, AssertionError):
                messagebox.showerror("Bad value", "Seconds must be a number, 0 or higher.", parent=d)
                return
            b = {"input": inp.get(), "output": out.get(), "seconds": s}
            if index is None:
                self.binds.append(b)
            else:
                self.binds[index] = b
            self.listen = None
            self.save()
            self.refresh()
            d.destroy()
        ttk.Button(d, text="Save", command=ok).grid(row=3, column=1, sticky="e", **pad)

    def selected(self):
        sel = self.tree.selection()
        return self.tree.index(sel[0]) if sel else None

    def edit_bind(self):
        i = self.selected()
        if i is not None:
            self.bind_dialog(i)

    def remove_bind(self):
        i = self.selected()
        if i is not None:
            del self.binds[i]
            self.save()
            self.refresh()

    # ---------------- profiles ----------------
    def ppath(self, name):
        return os.path.join(PROFILE_DIR, name + ".json")

    def profile_names(self):
        return sorted(f[:-5] for f in os.listdir(PROFILE_DIR) if f.endswith(".json"))

    def load_profiles(self):
        if not self.profile_names():
            with open(self.ppath("Default"), "w") as f:
                json.dump([{"input": "L3", "output": "RT (R2)", "seconds": 3}], f, indent=2)
        last = ""
        if os.path.exists(ACTIVE_FILE):
            last = open(ACTIVE_FILE).read().strip()
        names = self.profile_names()
        self.switch(last if last in names else names[0])

    def switch(self, name):
        self.release_all()
        self.profile = name
        with open(self.ppath(name)) as f:
            self.binds = json.load(f)
        with open(ACTIVE_FILE, "w") as f:
            f.write(name)
        self.combo["values"] = self.profile_names()
        self.combo.set(name)
        self.refresh()

    def save(self):
        with open(self.ppath(self.profile), "w") as f:
            json.dump(self.binds, f, indent=2)

    def new_profile(self):
        name = simpledialog.askstring("New profile", "Profile name:", parent=self.root)
        name = "".join(c for c in (name or "") if c.isalnum() or c in " -_").strip()
        if not name:
            return
        if not os.path.exists(self.ppath(name)):
            with open(self.ppath(name), "w") as f:
                json.dump([], f)
        self.switch(name)

    def delete_profile(self):
        if len(self.profile_names()) <= 1:
            messagebox.showinfo("Profiles", "You need at least one profile.")
            return
        if messagebox.askyesno("Delete", f"Delete profile '{self.profile}'?"):
            os.remove(self.ppath(self.profile))
            self.switch(self.profile_names()[0])

    # ---------------- controller input ----------------
    def open_pad(self, index):
        if not controller.is_controller(index):
            return
        c = controller.Controller(index)
        iid = c.as_joystick().get_instance_id()
        if iid not in self.pads:
            self.pads[iid] = c
            self.status.set(f"Connected: {c.name}")

    def poll(self):
        while not self.tray_q.empty():
            getattr(self, "tray_" + self.tray_q.get())()
        for e in pygame.event.get():
            t = e.type
            if t == pygame.CONTROLLERDEVICEADDED:
                if time.time() - self.vpad_time > 2:   # ignore our own virtual pad
                    self.open_pad(e.device_index)
                    if self.vsetting == "auto":
                        self.apply_vpad()
            elif t == pygame.CONTROLLERDEVICEREMOVED:
                self.pads.pop(e.instance_id, None)
            elif getattr(e, "instance_id", None) not in self.pads:
                continue
            elif t in (pygame.CONTROLLERBUTTONDOWN, pygame.CONTROLLERBUTTONUP):
                name = BUTTONS.get(e.button)
                if name:
                    self.changed(name, t == pygame.CONTROLLERBUTTONDOWN)
            elif t == pygame.CONTROLLERAXISMOTION:
                self.on_axis(e.axis, e.value / 32767)

        now = time.time()
        for out, until in list(self.holds.items()):
            if until and now >= until:
                self.output(out, False)
                del self.holds[out]
        self.root.after(5, self.poll)

    def on_axis(self, ax, v):
        if ax in TRIGGERS:
            self.edge((ax, "t"), TRIGGERS[ax], v > 0.5)
        elif ax in STICK_DIR:
            neg, pos = STICK_DIR[ax]
            self.edge((ax, "-"), neg, v < -0.6)
            self.edge((ax, "+"), pos, v > 0.6)

    def edge(self, key, name, on):
        if self.axis_on.get(key, False) != on:
            self.axis_on[key] = on
            self.changed(name, on)

    def changed(self, name, on):
        if on:
            self.status.set(f"Last input: {name}")
            if self.listen:
                cb, self.listen = self.listen, None
                cb(name)
                return
        if not self.enabled.get():
            return
        for b in self.binds:
            if b["input"] != name:
                continue
            out, secs = b["output"], float(b["seconds"])
            if on and out not in self.holds:
                self.output(out, True)
                self.holds[out] = time.time() + secs if secs > 0 else None
            elif not on and secs == 0:
                self.output(out, False)
                self.holds.pop(out, None)

    # ---------------- virtual controller ----------------
    def read_vsetting(self):
        try:
            with open(VPAD_FILE) as f:
                v = f.read().strip()
            if v in ("auto", "xbox", "ps"):
                return v
        except Exception:
            pass
        return "auto"

    def sony_connected(self):
        for c in self.pads.values():
            n = (c.name or "").lower()
            if "xbox" not in n and any(w in n for w in SONY_WORDS):
                return True
        return False

    def choose_kind(self):
        if self.vsetting == "xbox":
            return "x360"
        if self.vsetting == "ps":
            return "ds4"
        return "ds4" if self.sony_connected() else "x360"

    def apply_vpad(self, force=False):
        """(Re)create the virtual pad so the game sees the type we want."""
        kind = self.choose_kind()
        if kind == "ds4" and not DS4_OK:
            kind = "x360"
        if self.vpad is not None and kind == self.vkind and not force:
            return
        self.release_all()
        self.vpad = None                       # drops (unplugs) the old virtual pad
        self.dpad_held.clear()
        try:
            self.vpad = vg.VDS4Gamepad() if kind == "ds4" else vg.VX360Gamepad()
            self.vpad.update()
            self.vkind = kind
            self.vpad_error = ""
        except Exception as e:
            self.vpad = None
            self.vkind = None
            self.vpad_error = f"{type(e).__name__}: {e}"
        self.vpad_time = time.time()
        if self.vpad:
            self.vinfo.set("Game sees: " + ("PlayStation controller (DS4)" if kind == "ds4"
                                            else "Xbox 360 controller"))
        else:
            self.vinfo.set("Virtual pad NOT running - click Setup check")

    def on_vpad_choice(self, _e=None):
        self.vsetting = VPAD_CHOICES[self.vcombo.get()]
        try:
            with open(VPAD_FILE, "w") as f:
                f.write(self.vsetting)
        except Exception:
            pass
        self.apply_vpad(force=True)

    def updates_on(self):
        return os.environ.get("CM_AUTOUPDATE") == "1"      # set by ControllerMacro.exe

    def show_setup(self, problem=None):
        d = tk.Toplevel(self.root)
        d.title("Setup check")
        d.transient(self.root)
        pad = {"padx": 10, "pady": 5}

        def row(r, ok, text, link=None, required=True):
            mark = "OK" if ok else ("MISSING" if required else "Not found")
            ttk.Label(d, text=f"[{mark}]  {text}", wraplength=430, justify="left").grid(
                row=r, column=0, sticky="w", **pad)
            if link and not ok:
                ttk.Button(d, text="Download",
                           command=lambda u=link: webbrowser.open(u)).grid(row=r, column=1, **pad)

        row(0, self.vpad is not None,
            "Virtual controller driver (ViGEmBus) - required. Restart your PC after installing it.",
            LINKS["vigem"])
        if problem:
            ttk.Label(d, text=problem, wraplength=430, foreground="#a00", justify="left").grid(
                row=1, column=0, columnspan=2, sticky="w", **pad)
        names = [c.name for c in self.pads.values()]
        row(2, bool(names), ("Controller: " + ", ".join(names)) if names
            else "No controller detected. Plug it in by USB or pair it by Bluetooth.")
        row(3, os.path.exists(HIDHIDE_DIR),
            "HidHide - optional. Hides your real controller from games so they only see the virtual one.",
            LINKS["hidhide"], required=False)
        upd = ("Auto-update: ON. New versions install when you open the app."
               if self.updates_on() else
               "Auto-update: OFF (only works when started from ControllerMacro.exe).")
        ttk.Label(d, text=f"Version {VERSION}.  {upd}", wraplength=430, justify="left").grid(
            row=4, column=0, columnspan=2, sticky="w", **pad)

        def retry():
            self.apply_vpad(force=True)
            d.destroy()
            if not self.vpad:
                self.show_setup(self.vpad_error)
        bar = ttk.Frame(d)
        bar.grid(row=5, column=0, columnspan=2, sticky="e", **pad)
        ttk.Button(bar, text="Retry", command=retry).pack(side="left", padx=4)
        ttk.Button(bar, text="Close", command=d.destroy).pack(side="left")

    def output(self, name, on):
        if self.vpad is None:
            return
        if self.vkind == "ds4":
            self.output_ds4(name, on)
        else:
            self.output_x360(name, on)
        self.vpad.update()

    def output_x360(self, name, on):
        if name in OUT_TRIGGERS:
            fn = self.vpad.left_trigger if OUT_TRIGGERS[name] == "left" else self.vpad.right_trigger
            fn(value=255 if on else 0)
        elif name in OUT_BUTTONS:
            (self.vpad.press_button if on else self.vpad.release_button)(button=OUT_BUTTONS[name])

    def output_ds4(self, name, on):
        v = self.vpad
        if name in OUT_TRIGGERS:
            side = OUT_TRIGGERS[name]
            (v.left_trigger if side == "left" else v.right_trigger)(value=255 if on else 0)
            (v.press_button if on else v.release_button)(button=DS4_TRIG_BTN[side])
        elif name in DPAD_NAMES:
            (self.dpad_held.add if on else self.dpad_held.discard)(name)
            key = tuple(int(n in self.dpad_held) for n in DPAD_NAMES)
            v.directional_pad(direction=DS4_DPAD.get(key, DS4_DPAD_NONE))
        elif name == "Guide (PS/Xbox)":
            (v.press_special_button if on else v.release_special_button)(special_button=DS4_PS)
        elif name in DS4_OUT:
            (v.press_button if on else v.release_button)(button=DS4_OUT[name])

    def release_all(self):
        for out in list(self.holds):
            self.output(out, False)
        self.holds.clear()

    # ---------------- tray / window ----------------
    def on_toggle(self):
        self.macros_flag = self.enabled.get()
        self.release_all()
        if self.tray:
            self.tray.update_menu()

    def on_unmap(self, e):
        if e.widget is self.root and self.root.state() == "iconic":
            self.root.withdraw()
            self.show_tray()

    def show_tray(self):
        if self.tray:
            return
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((4, 4, 60, 60), radius=14, fill=(40, 44, 52, 255))
        d.ellipse((20, 20, 44, 44), fill=(80, 200, 120, 255))
        menu = pystray.Menu(
            pystray.MenuItem("Open", lambda i, it: self.tray_q.put("open"), default=True),
            pystray.MenuItem("Macros ON", lambda i, it: self.tray_q.put("toggle"),
                             checked=lambda it: self.macros_flag),
            pystray.MenuItem("Quit", lambda i, it: self.tray_q.put("quit")),
        )
        self.tray = pystray.Icon("ControllerMacro", img, "Controller Macro", menu)
        self.tray.run_detached()

    def hide_tray(self):
        if self.tray:
            self.tray.stop()
            self.tray = None

    def tray_open(self):
        self.hide_tray()
        self.root.deiconify()
        self.root.lift()

    def tray_toggle(self):
        self.enabled.set(not self.enabled.get())
        self.on_toggle()

    def tray_quit(self):
        self.close()

    def close(self):
        self.release_all()
        self.hide_tray()
        try:
            if self.root.state() == "normal":
                with open(GEO_FILE, "w") as f:
                    f.write(self.root.geometry())
        except Exception:
            pass
        self.root.destroy()


if __name__ == "__main__":
    try:
        root = tk.Tk()
        App(root)
        root.mainloop()
    except Exception:
        import traceback
        err = traceback.format_exc()
        with open(os.path.join(BASE, "error.log"), "w") as f:
            f.write(err)
        messagebox.showerror("Controller Macro crashed", err[-1500:])
