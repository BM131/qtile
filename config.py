#.______   .___  ___. 
#|   _  \  |   \/   | 
#|  |_)  | |  \  /  | 
#|   _  <  |  |\/|  | 
#|  |_)  | |  |  |  | 
#|______/  |__|  |__| 
                    

from typing import List  # noqa: F401
import os

from libqtile import bar, layout, widget, extension
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

os.system('xrandr --output eDP --brightness 0.6')
#os.system("xrandr --output DisplayPort-0 --same-as eDP")
os.system("nitrogen --restore")
os.system("picom --experimental-backends -b")
os.system("picom")

mod = "mod4"
terminal = guess_terminal()

keys = [
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "control"], "h", lazy.layout.decrease_ratio()),
    Key([mod, "control"], "l", lazy.layout.increase_ratio()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "g", lazy.window.toggle_floating()),
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "q", lazy.window.kill()),
    Key([mod, "control"], "r", lazy.reload_config()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], 'Return', lazy.spawn('alacritty')),
    Key([mod], "w", lazy.spawn("brave")),
    Key([mod], "f", lazy.spawn("thunar")),
    #Key([mod], "space", lazy.spawn('alacritty -e python3 /home/bm/.key.py')),
    Key([mod], "space", lazy.widget["keyboardlayout"].next_keyboard()),
    Key([mod, "shift"], "Return", lazy.spawn('rofi -show run'))
]

groups = [
    Group("z", label=""),
    Group("x", label=""),
    Group("c", label=""),    
    Group("v", label=""),
]
for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
             Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
                 desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Tile(border_focus="#4fa4e0",
                #border_normal='#ffffff',
                border_width=2,
                border_on_single = True,
                margin=4,
                ratio=0.55,
                shift_windows=True)
]

widget_defaults = dict(
    font="hack",
    fontsize=13,
    padding=3,
)
extension_defaults = widget_defaults.copy()

batt = os.popen("cat /sys/class/power_supply/BAT1/capacity").read()[0:3]
batt_status = os.popen('cat /sys/class/power_supply/BAT1/status').read()[0:3].lower()
battery = ''
for i in batt:
    if i in '1234567890':
        battery += i
battery = int(battery)

batt_icon = 'BAT:'
#if battery >= 90:
#    batt_icon = ''
#elif battery >= 75 and battery < 90:
#    batt_icon = ''
#elif battery >= 50 and battery < 75:
#    batt_icon = ''
#elif battery >= 25 and battery < 50:
#    batt_icon = ''
#elif battery >= 10 and battery < 25:
#    batt_icon = ''
#elif battery < 10:
#    batt_icon = ''
if batt_status == 'cha' or batt_status == 'ful':
    batt_icon = ''

screens = [
    Screen(
        left=bar.Gap(size=5),
        right=bar.Gap(size=5),
        bottom=bar.Gap(size=5),
        top=bar.Bar(
            [   
                widget.GroupBox(this_current_screen_border='#4681ab', highlight_method='block', block_highlight_text_color='#ffffff', margin_x=8),
                #widget.Spacer(length=7),
                widget.Prompt(),
                widget.WindowName(background='#4681ab', fontsize='14', padding=8),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                #widget.TextBox("default config", name="default"),
                #widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                widget.Systray(),

                widget.Spacer(length=5),
                
                widget.Net(format='{down} ↓↑ {up}'),

                widget.Spacer(length=14),

                widget.Memory(measure_mem='G',
                              format=':{MemUsed: .2f}{mm}',
                              update_interval=1.5,
                             mouse_callbacks={'Button1': lazy.spawn('alacritty -e htop')}),

                widget.Spacer(length=10),

                widget.CPU(format=': {load_percent}%',
                           update_interval=2,
                           mouse_callbacks={'Button1': lazy.spawn('alacritty -e htop')}),
                

                widget.Spacer(length=14),
                
                widget.TextBox(text="Vol:"),
                widget.Volume(),
                
                widget.Spacer(length=14),
                
                widget.TextBox(text="",
                               mouse_callbacks={'Button1': lazy.widget["keyboardlayout"].next_keyboard()}),

                widget.KeyboardLayout(configured_keyboards=['us', 'ara']),
                
                widget.Spacer(length=14),
                
                widget.TextBox(text=batt_icon),

                widget.Battery(format='{percent:2.0%}',
                               update_interval=30),
                widget.Spacer(length=14),
                
                widget.Clock(format="%d/%m %a  %I:%M %p",
                             mouse_callbacks={'Button1': lazy.spawn('alacritty --hold -e cal')}),

                widget.Spacer(length=6)
            ],
            24,
             #border_width=[5, 5, 5, 5],  # Draw top and bottom borders
             #border_color=["000000", "000000", "000000", "000000"]  # Borders are magenta
             background='#00000099'
             
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

wmname = "qtile"
