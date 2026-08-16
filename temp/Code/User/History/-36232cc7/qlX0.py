from libqtile.bar import Bar
from libqtile.widget.battery import Battery
from libqtile.widget.clock import Clock
from libqtile.widget.cpu import CPU
from libqtile.widget.currentlayout import CurrentLayout
from libqtile.widget.groupbox import GroupBox
from libqtile.widget.memory import Memory
from libqtile.widget.net import Net
from libqtile.widget.spacer import Spacer
from libqtile.widget.systray import Systray
from libqtile.widget.window_count import WindowCount
from libqtile.widget.windowname import WindowName

from unicodes import left_half_circle, right_arrow, left_arrow, right_half_circle
from colors import gruvbox

BAR_HEIGHT = 20
# sBAR_MARGIN = 5

bar = Bar([
    GroupBox(
        disable_drag=True,
        active=gruvbox['magenta'],
        inactive=gruvbox['dark-gray'],
        highlight_method='line',
        block_highlight_text_color=gruvbox['fg_gutter'],
        borderwidth=0,
        highlight_color=gruvbox['bg'],
        background=gruvbox['bg'],
        # spacing=2
    ),
    left_half_circle(gruvbox['red'], gruvbox['bg']),
    CurrentLayout(
        background=gruvbox['red'],
        foreground=gruvbox['white'],
        margin=10,
    ),

    right_arrow(gruvbox['fg_gutter'], gruvbox['red']),
    WindowCount(
        text_format='缾 {num}',
        background=gruvbox['fg_gutter'],
        foreground=gruvbox['white'],
        show_zero=True,
    ),
    right_half_circle(gruvbox['fg_gutter'], gruvbox['bg']),

    WindowName(
        background=gruvbox['bg'],
        foreground=gruvbox['fg']
    ),

    left_half_circle(gruvbox['black'], gruvbox['bg']),
    CPU(
        format=' {freq_current}GHz {load_percent}%',
        background=gruvbox['black'],
        foreground=gruvbox['pink']
    ),

    Memory(
        format=' {MemUsed: .0f}{mm}/{MemTotal: .0f}{mm}',
        background=gruvbox['black'],
        foreground=gruvbox['cyan']
    ),

    Net(
        background=gruvbox['black'],
        foreground=gruvbox['green']
    ),
    # # Battery(
    # #     background=gruvbox['fg3'],
    # #     format='{char} {percent:2.0%} {hour:d}:{min:02d}'
    # # ),

    left_half_circle(gruvbox['fg_gutter'], gruvbox['black']),
    Systray(
        background=gruvbox['fg_gutter']
    ),
    right_half_circle(gruvbox['fg_gutter'], gruvbox['black']),

    Clock(
        background=gruvbox['black'],
        foreground=gruvbox['white'],
        format=' %Y-%m-%d %a %I:%M %p'
    ),



],
    # background=gruvbox['bg'],
    size=BAR_HEIGHT,
    margin=8,
)
