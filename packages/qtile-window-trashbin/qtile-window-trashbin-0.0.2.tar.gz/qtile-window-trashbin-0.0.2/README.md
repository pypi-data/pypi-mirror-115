# qtile-window-trashbin
Qtile Extension to reopen closed windows. Never think "Oh shit" again when you close a window.

## Installation
You can install the package using pip
```bash
pip install qtile-window-trashbin
```

## Usage
This module adds a "Thrashbin" class. Use it in your keybindings instead of kill. The pane will be killed after a given time.

U could put the following in your ~/.config/qtile/config.py
```python
from trashbin import Trashbin

trash_group = ScratchPad("killPane") #We use an invisible Group: A ScratchPad.
groups.extend([trash_group]) # Let's append it to to groups.

trash = Trashbin(trash_group.name, delay=5) # Initialize the Trashbin. Use the newly created Group to store the windows. Kill a Window put to the trashbin afert 5 seconds.

keys.extend([
    Key([mod], "q", lazy.function(trash.append_currend_window)), # move to trash
    Key([mod, "shift"], "q", lazy.window.kill()), # real kill. Sometimes you want to kill insteadly.
    Key([mod, "shift"], "e", lazy.function(trash.pop_to_current_group)) # Restore the last window put to the trashbin.
    ])

```
Afterwards you can hit `Super + q` and the current window be moved to the trash.
Hit `Super + Shift + e` to restore the last window, put to the trashbin.
Sometimes moving a window to the trash is not what you want.
For example when quiting an video player you may want to stop the playing immediately.
Hit `Super + Shift + q` to quit immediatley. Caution: This is not undoable.
