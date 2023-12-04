# Conway's Game of Life
Windows implementation of game in Python in which you can
* create and run any game configuration
* move around the field
* start/pause the game
* save the current field as a snapshot
* create a custom brush pattern and draw with it (also you can save your patterns)
* change
  * color of brush (different colors are mixed during the game)
  * the scale
  * game speed
* roll back time  
* do something else

## Now about the controls
| control | action |
| --- | --- |
| LMB | add/remove a living cell |  
| LMB (holding) | draw a line of living ones |  
| RMB (holding) | movement across the field |
| Scrolling the mouse wheel | increase/decrease the field |  
| Spacebar | start/pause Conway's game |  
| Left/right arrow | slow down/speed up the game twice |  
| P or middle mouse button | toggle pattern mode on/off |
| Upper/lower arrow | switch between patterns |
| R | rotate the pattern 90 degrees clockwise | 
| E or button on the top right | toggle eraser mode on/off |  
| G | toggle grid mode on/off | 
| 1, 2, 3, 4, 5, 0 | drawing colors (0 is false: i.e. does not participate in the game) |
| K , CTRL+K | clear living / false cells |
| I or the button on the top right | inventory with your patterns (the last one opened is used) |
| CTRL+S or the button on the top right | save the field and patterns | 
| CTRL+Z | roll back to the last save |
| V, B | time travel (note: it's not saved) |  
| H | change the hiding mode of icons (in the field) |  
| ESC | exit the current window (in the field: exit the application) |
### Notes
This implementation is only for Windows, but it doesn’t seem to take much time to adapt to other platforms. 

You can download EXE file from Releases or run main.py after installing the necessary libraries by this command:
```bash
pip install pygame; pip install pypiwin32
```
I used pyinstaller to create the main.exe file by main.spec and following commands:
```bash
pip install pyinstaller
```
```bash
pyinstaller -F main.spec
```

Also just saying that the \_\_parameters\_\_ file is a save file, it is created and then overwritten every time you save.
