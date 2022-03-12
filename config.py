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

#os.system("xrandr --output DisplayPort-0 --primary && xrandr --output eDP --below DisplayPort-0")
#os.system('xrandr --output eDP --brightness 0.6')
#os.system("xrandr --output DisplayPort-0 --same-as eDP")
os.system("nitrogen --restore")
#os.system("picom --experimental-backends -b")
#os.system("picom")

mod = "mod4"
terminal = 'alacritty'

keys = [#Move
        Key([mod], "h", lazy.layout.left()),
        Key([mod], "l", lazy.layout.right()),
        Key([mod], "j", lazy.layout.down()),
        Key([mod], "k", lazy.layout.up()),
        #Shift windows
        Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
        Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
        Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
        Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
        #Resize windows
        Key([mod, "control"], "h", lazy.layout.shrink_main()),
        Key([mod, "control"], "l", lazy.layout.grow_main()),
        Key([mod, "control"], "j", lazy.layout.grow()),
        Key([mod, "control"], "k", lazy.layout.shrink()),
        #Functions
        Key([mod], "n", lazy.layout.normalize()),
        Key([mod], "g", lazy.window.toggle_floating()),
        Key([mod], "Tab", lazy.next_layout()),
        Key([mod], "q", lazy.window.kill()),
        Key([mod, "control"], "r", lazy.reload_config()),
        Key([mod, "control"], "q", lazy.shutdown()),
        Key([mod], "space", lazy.widget["keyboardlayout"].next_keyboard()),
        #Apps
        Key([mod], 'Return', lazy.spawn('alacritty')),
        Key([mod], "w", lazy.spawn("brave")),
        Key([mod], "f", lazy.spawn("thunar")),
        Key([mod, "shift"], "Return", lazy.spawn('rofi -show run'))
        ]

groups = [
        Group("z", label="  "),
        Group("x", label="  "),
        Group("c", label="  "),    
        Group("v", label="  "),
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
        layout.MonadTall(
            border_focus="#00ffe4",
            margin=9,
            new_client_position = "top"
            ),
        ]


widget_defaults = dict(
        font="Ubuntu Bold",
        fontsize=13,
        padding=3,
        )
extension_defaults = widget_defaults.copy()

screens = [
        Screen(
            top=bar.Bar(
                [   
                    widget.GroupBox(
                        this_current_screen_border = "#3aa69f",
                        other_screen_border = '#283b39',
                        highlight_method='block',
                        block_highlight_text_color='#ffffff',
                        margin_x=4
                        ),

                    widget.Spacer(length=10),

                    #widget.CurrentLayoutIcon(scale=0.8),

                    widget.TextBox(text='|',font='sans', fontsize=33),

                    widget.WindowName(
                        foreground='#3aa69f',
                        fontsize='14',
                        padding=8
                        ),
                    
                    widget.TextBox(text='|',font='sans', fontsize=33),

                    widget.Systray(),

                    widget.Spacer(length=5),

                    widget.Net(format='{down} {up}'),

                    widget.Spacer(length=14),

                    widget.Memory(
                        measure_mem='G',
                        format='{MemUsed: .2f}{mm}',
                        update_interval=1.5,
                        mouse_callbacks={'Button1': lazy.spawn('alacritty -e htop')}
                        ),

                    widget.Spacer(length=10),

                    widget.CPU(
                        format=' {load_percent}%',
                        update_interval=2,
                        mouse_callbacks={'Button1': lazy.spawn('alacritty -e htop')}
                        ),


                widget.Spacer(length=14),

                widget.TextBox(text=""),
                
                widget.Volume(),

                widget.Spacer(length=14),

                widget.TextBox(
                        text="",
                        mouse_callbacks={'Button1': lazy.widget["keyboardlayout"].next_keyboard()}
                        ),

                widget.KeyboardLayout(
                        configured_keyboards=['us', 'ara']
                        ),

                widget.Spacer(length=14),


                widget.Battery(
                        full_char='',
                        empty_char='',
                        charge_char='',
                        discharge_char='',
                        format='{char} {percent:2.0%}',
                        update_interval=30
                        ),

                widget.Spacer(length=14),

                widget.Clock(
                        format="%d/%m %a  %I:%M %p",
                        mouse_callbacks={'Button1':lazy.spawn('alacritty --hold -e cal')},
                        padding = 0
                        ),

                widget.Spacer(length=6)
            ],
            24,
             background= "#1b1c1c"
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
follow_mouse_focus = True
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

wmname = "LG3D"
