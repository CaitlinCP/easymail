from tkinter import *
from tkinter import ttk


class textFrame(ttk.Frame):
    def __init__(self, parent, row, column, sticky):
        ttk.Frame.__init__(self, parent)
        self.grid(row=row, column=column, sticky=sticky)
        self.columnconfigure(column, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.y_scrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        self.y_scrollbar.grid(column=2, row=3, sticky=(N, S))
        ttk.Label(self, text='Input Text Below').grid(column=1, row=1)
        self.text_input = Text(self, width=40, height=10, wrap=WORD,
                               yscrollcommand=self.y_scrollbar.set, exportselection=True, undo=True)
        self.text_input.grid(column=1, row=3, sticky=(W, E))
        self.button_row = ttk.Frame(self)
        self.button_row.grid(row=2, column=1)
        self.hero_button = ttk.Button(self.button_row, text='Hero', command=lambda: self.add_tag('%%HERO%%'))
        self.hero_button.grid(row=1, column=1)
        self.bold_button = ttk.Button(self.button_row, text='Bold', command=lambda: self.add_tag('%%BOLD%%'))
        self.bold_button.grid(row=1, column=2)
        self.italic_button = ttk.Button(self.button_row, text='Italic', command=lambda: self.add_tag('%%ITALIC%%'))
        self.italic_button.grid(row=1, column=3)
        self.underline_button = ttk.Button(self.button_row, text='Underline', command=lambda: self.add_tag('%%UNDERLINE%%'))
        self.underline_button.grid(row=1, column=4)
        self.red_button = ttk.Button(self.button_row, text='Red', command=lambda: self.add_tag('%%RED%%'))
        self.red_button.grid(row=1, column=5)
        self.link_button = ttk.Button(self.button_row, text='Link', command=lambda: self.add_tag('%%LINK%%'))
        self.link_button.grid(row=1, column=6)
        self.name_button = ttk.Button(self.button_row, text='First Name', command=lambda: self.add_merge_field('%%FNAME%%'))
        self.name_button.grid(row=1, column=7)

    def add_tag(self, tag):
        if self.text_input.selection_get:
            self.text_input.insert(self.text_input.index(SEL_FIRST), tag)
            self.text_input.insert(self.text_input.index(SEL_LAST), tag)

    def add_merge_field(self, field):
        try:
            self.text_input.replace(self.text_input.index(SEL_FIRST), self.text_input.index(SEL_LAST), field)
        except TclError:
            self.text_input.insert(self.text_input.index(INSERT), field)

