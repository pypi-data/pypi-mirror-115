from tkinter import  *
from tkinter.ttk import *


class ScrollableFrame(Frame):
    '''
    It's no different from tkinter's Frame.
    orient(The orient of scroolbar): 0 -> VERTICAL(default), 1->HORIZONTAL, 
    2->both
    '''
    def __init__(self, container, orient=0, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        top_frame =Frame( self)
        bottom_frame = Frame( self )
        self.canvas = Canvas(top_frame)
        self.frame =Frame(self.canvas)

        self.canvas['width'] = kwargs['width']
        self.canvas['height'] = kwargs['height']

        scrollbar = Scrollbar(top_frame if orient==0 else bottom_frame, \
        command=self.canvas.yview if orient==0 else self.canvas.xview, orient=VERTICAL \
        if orient== 0 else HORIZONTAL)
        if orient == 0:
            self.canvas.configure(yscrollcommand=scrollbar.set)
        else:
            self.canvas.configure(xscrollcommand=scrollbar.set)
        if orient == 2:
            _scrollbar = Scrollbar(self,  command=self.canvas.yview, orient=VERTICAL)
            self.canvas.configure(yscrollcommand=_scrollbar.set)
            _scrollbar.pack(side=RIGHT, fill=Y  )

        self.canvas.create_window((0, 0), window=self.frame, anchor=NW)

        self.frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT if orient==0 else BOTTOM, \
        fill=Y if orient==0 else X )
        top_frame.pack(side=TOP)
        bottom_frame.pack(side=BOTTOM, fill=X)