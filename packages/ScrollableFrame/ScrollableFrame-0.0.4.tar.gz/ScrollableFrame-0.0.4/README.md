# ScrollableFrame
Your tkinter ScrollableFrame

```python
from tkinter import *
from ScrollableFrame import *

root = Tk()
# It's no different from tkinter's Frame,
# orient(The orient of scroolbar): 0 -> VERTICAL, 1->HORIZONTAL, 2->both
sf = ScrollableFrame(root, orient = 2 , height=180, width=360) # :-)
Label(sf.frame, text=("(^_^)"*20+'\n')*20).pack()
sf.pack()
root.mainloop()
```
