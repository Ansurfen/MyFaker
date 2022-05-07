import ttkbootstrap as ttk
from ttkbootstrap import utility
from ttkbootstrap.constants import *

from mvc.controller import *
from mvc.model import *


class FakerUI(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES)

        self.file_param = ttk.StringVar(value='')
        self.file_path = ttk.StringVar(value='')
        self.url = ttk.StringVar(value='')
        self.param = ttk.StringVar(value='')
        self.method_var = ttk.StringVar(value='GET')
        self.content_type = ttk.StringVar(value='FORM')
        self.ctx_param = ttk.StringVar(value='')
        self.cnt = ttk.IntVar(value=1)
        self.cnt2 = ttk.IntVar(value=1)
        
        notebook = ttk.Notebook(self)
        notebook.pack(side=TOP)
        request_window = ttk.Frame(notebook)
        request_window.pack(side=TOP)
        file_window = ttk.Frame(notebook)
        file_window.pack(side=TOP)
        setting_window = ttk.Frame(notebook)
        setting_window.pack(side=TOP)
        notebook.add(request_window, text='request')
        notebook.add(file_window, text='file')
        notebook.add(setting_window, text='setting')

    # ? request_window
        url_row = ttk.Frame(request_window)
        url_row.pack(fill=X, expand=YES, pady=10)
        restful = ttk.Combobox(url_row, width=5, textvariable=self.method_var)
        restful['values'] = ('GET', 'POST')
        restful.current(0)
        restful.pack(side=LEFT)
        url_input = ttk.Entry(url_row, width=50, textvariable=self.url)
        url_input.pack(side=LEFT, fill=X, expand=YES)
        request_btn = ttk.Button(
            master=url_row,
            command=lambda: deal_requset(self),
            text="Browse",
        )
        request_btn.pack(side=LEFT)

        param_row = ttk.Frame(request_window)
        param_row.pack(fill=X, expand=YES, pady=5)
        content_type = ttk.Combobox(param_row, width=5,textvariable=self.content_type)
        content_type['values'] = ('FORM', 'JSON')
        content_type.current(0)
        content_type.pack(side=LEFT)
        param_input = ttk.Entry(param_row, width=50,textvariable=self.ctx_param)
        param_input.pack(side=LEFT, fill=X, expand=YES)

    # ? file_window
        path_row = ttk.Frame(file_window)
        path_row.pack(fill=X, expand=YES)
        path_tl = ttk.Label(path_row, width=5, text='Path')
        path_tl.pack(side=LEFT)
        path_input = ttk.Entry(path_row, width=50, textvariable=self.file_path)
        path_input.pack(side=LEFT, fill=X, expand=YES)
        browse_btn = ttk.Button(
            master=path_row,
            command=lambda: select_file(self),
            text="Browse",
        )
        browse_btn.pack(side=LEFT)

        file_param_row = ttk.Frame(file_window)
        file_param_row.pack(fill=X, expand=YES, pady=5)
        file_param_lb = ttk.Label(file_param_row, width=5, text='Param')
        file_param_lb.pack(side=LEFT)
        file_param_input = ttk.Entry(
            file_param_row, width=50, textvariable=self.file_param)
        file_param_input.pack(side=LEFT, fill=X, expand=YES)
        browse_btn = ttk.Button(
            master=file_param_row,
            command=lambda: exec_file(self),
            text="Execute",
        )
        browse_btn.pack(side=LEFT)

    # ? setting_window
        base_setting_row = ttk.Frame(setting_window)
        base_setting_row.pack(fill=X,expand=YES)
        cnt_tl = ttk.Label(base_setting_row, width=8, text='Exec cnt')
        cnt_tl.pack(side=LEFT)
        cnt_input = ttk.Entry(base_setting_row, textvariable=self.cnt)
        cnt_input.pack(side=LEFT, fill=X, expand=YES)

        cnt2_tl = ttk.Label(base_setting_row, width=9, text='Create cnt')
        cnt2_tl.pack(side=LEFT)
        cnt2_input = ttk.Entry(base_setting_row, textvariable=self.cnt2)
        cnt2_input.pack(side=LEFT, fill=X, expand=YES)
    # ? common func
        self.logger()
        self.progress()

    def logger(self):
        self.loglist = ttk.Treeview(
            master=self,
            bootstyle=INFO,
            columns=[0, 1],
            show=HEADINGS
        )
        self.loglist.pack(fill=BOTH, expand=YES, pady=10)
        self.loglist.heading(0, text='Time', anchor=W)
        self.loglist.heading(1, text='Context', anchor=W)
        self.loglist.column(
            column=0,
            anchor=W,
            width=utility.scale_size(self, 140),
            stretch=False
        )
        self.loglist.column(
            column=1,
            anchor=W,
            width=utility.scale_size(self, 360),
            stretch=False
        )
        self.loglist.pack(side=TOP)

    def progress(self):
        self.progressbar = ttk.Progressbar(
            master=self,
            mode=INDETERMINATE,
            bootstyle=(STRIPED, SUCCESS)
        )
        self.progressbar.pack(fill=X, expand=YES)
