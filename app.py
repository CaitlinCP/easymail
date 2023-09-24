from tkinter import *
from tkinter import ttk

from generate.format import easyMail
from interface.input_options import inputFrame
from interface.input_text import textFrame


class App(ttk.Frame):
    def __init__(self):
        self.root = Tk()
        self.root.title("EasyMail")
        self.entered_text = ''
        self.formatted_text = ''
        self.signature_file = ''
        self.display_state = 0
        self.warning_label_text = StringVar()
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=1)
        self.inputFrame = inputFrame(parent=self.mainframe, row=1, column=1, sticky=(W, E))
        self.textFrame = textFrame(parent=self.mainframe, row=2, column=1, sticky=(W, E))
        self.submitRow = ttk.Frame(self.mainframe)
        self.submitRow.grid(row=3, column=1)
        self.textButton = ttk.Button(self.submitRow, text='Text', command=lambda: self.display_text())
        self.textButton.grid(row=1, column=1, sticky=(W, E))
        self.htmlButton = ttk.Button(self.submitRow, text='HTML', command=lambda: self.submit_form())
        self.htmlButton.grid(row=1, column=2, sticky=(W, E))
        self.warning_label = ttk.Label(self.mainframe, textvariable=self.warning_label_text)
        self.warning_label.grid(row=4, column=1, sticky=(W, E))

    def get_signature_format(self):
        if self.inputFrame.signature_entry_var.get() == 'Organization Director':
            self.signature_file = 'templates/signatures/organization_director.txt'
        elif self.inputFrame.signature_entry_var.get() == 'Marketing Director':
            self.signature_file = 'templates/signatures/marketing_director.txt'
        else:
            self.signature_file = 'templates/signatures/organization_director.txt'

    def submit_form(self):
        if self.display_state == 0:
            self.entered_text = self.textFrame.text_input.get('1.0', END)
        try:
            self.get_signature_format()
            self.formatted_text = easyMail(text=self.entered_text, hero_image=self.inputFrame.hero_image_entry.get(),
                                           preview_text=self.inputFrame.preview_text_entry.get(),
                                           url=self.inputFrame.url_entry.get(),
                                           donate_footer_url=self.inputFrame.donate_footer_url_entry.get(),
                                           button=self.inputFrame.button_question_var.get(),
                                           action=self.inputFrame.action_question_var.get(),
                                           credit=self.inputFrame.credit_entry.get(),
                                           signature=self.signature_file).create_email()
            self.textFrame.text_input.replace('1.0', END, self.formatted_text)
            self.warning_label_text.set('')
            self.display_state = 1
        except IndexError:
            self.warning_label_text.set('Not enough text entered. Please enter more text')

    def display_text(self):
        self.textFrame.text_input.replace('1.0', END, self.entered_text)
        self.display_state = 0


App().root.mainloop()