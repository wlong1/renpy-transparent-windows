"""
The following will:
- Add a Window Transparency slider to your preferences
- Allow the user to adjust the transparency of textboxes of your choice
- And also adjust the transprency of the menu window
- Overlays the window
"""


# In script.py
# Replace with your background(s) of choice

init python:
    def update_nvl_transparency():
        style.nvl_window.background = Transform("gui/nvl.png", alpha=persistent.window_transparency)


# In screens.py

# CTRL + F: screen preferences()
# and add this slider somewhere inside your preference window

label _("Window Transparency")

bar value FieldValue(
    persistent,
    "window_transparency",
    range=1.0, step=0.05,
    action=update_nvl_transparency
    ) style "slider_slider"


# Modify the background of your style of choice

style nvl_window:
    xfill True
    yfill True
    background Transform("gui/nvl.png", alpha=persistent.window_transparency) # Use Transform and set the alpha
    padding gui.nvl_borders.padding


# Need to forcibly rebuild the textbox style when exiting the menu
# CTRL + F: screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):
# At the bottom, update action

textbutton _("Return"):
    style "return_button"

    action [Return(), style.rebuild]



## The following is for having an overlay menu and making it translucent also

# CTRL + F: screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):
# and modify gui.main_menu_background so the background now has variable transparency

if main_menu:
    add gui.main_menu_background alpha persistent.window_transparency
else:
    add gui.game_menu_background alpha persistent.window_transparency


# In order to have it overlay instead of replace, the common files must be edited.
# The following goes into a file your RenPy folder, NOT project folder.
# Look for the file \renpy\common\00gamemenu.rpy
# Modify the _game_menu label

label _game_menu(*args, _game_menu_screen=_game_menu_screen, **kwargs):
    if not _game_menu_screen:
        return

    $ renpy.play(config.enter_sound)

    if renpy.has_label("game_menu"):
        jump expression "game_menu"

    if renpy.has_screen(_game_menu_screen):
        $ renpy.show_screen(_game_menu_screen, *args, _layer="screens", _zorder=200, **kwargs) # Show on same layer but higher zorder
        $ renpy.pause(hard=True)
        jump _noisy_return

    jump expression _game_menu_screen
