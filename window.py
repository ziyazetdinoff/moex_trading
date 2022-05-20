import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry, Calendar

import db_maker


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('My App')
        self['background'] = '#EBEBEB'
        self.geometry("750x500+300+200")
        self.resizable(False, True)
        self.frame_add_stock = tk.Frame(self, width=570)
        self.frame_stat = tk.Frame(self, width=230)
        self.frame_db = tk.Frame(self, width=800, height=460)
        self.flag_all_period = tk.BooleanVar()
        self.list_stocks = db_maker.get_current_list_stocks()
        self.run()

    def run(self):
        self.put_frames()
        self.widgets_add_stock_frame()
        self.widgets_stat_frame()
        self.widgets_db_frame()

    def put_frames(self):
        self.frame_add_stock.grid(row=0, column=0, sticky='nesw')
        self.frame_stat.grid(row=0, column=1, sticky='nesw')
        self.frame_db.grid(row=1, column=0, columnspan=2, sticky='nesw')

    def widgets_add_stock_frame(self):
        l_pick_stock = tk.Label(self.frame_add_stock, text='Выбор акции:')
        l_period = tk.Label(self.frame_add_stock, text='Период:')
        self.cb_pick_stock = ttk.Combobox(self.frame_add_stock,
                                     values=self.list_stocks,
                                     justify=tk.CENTER,
                                     state='readonly')
        self.cb_pick_stock.bind('<<ComboboxSelected>>', self.refresh_widgets_add_stock_frame)
        btn_update_stocks = tk.Button(self.frame_add_stock, text='Обновить акции')  # command=db_maker.update_list_of_stocks()
        chbtn_all_period = tk.Checkbutton(self.frame_add_stock,
                                         text='Весь период',
                                         variable=self.flag_all_period)
        self.de_period1 = DateEntry(self.frame_add_stock,
                                    foreground='black',
                                    normalforeground='black',
                                    selectforeground='red',
                                    background='white',
                                    date_pattern='YYYY-mm-dd')
        l_dash = tk.Label(self.frame_add_stock, text='-')
        self.de_period2 = DateEntry(self.frame_add_stock,
                                    foreground='black',
                                    normalforeground='black',
                                    selectforeground='red',
                                    background='white',
                                    date_pattern='YYYY-mm-dd')
        btn_add = tk.Button(self.frame_add_stock, text='Добавить')
        btn_del = tk.Button(self.frame_add_stock, text='Удалить')
        btn_actual = tk.Button(self.frame_add_stock, text='Актуализация')

        l_pick_stock.grid(row=0, column=0, padx=10, pady=10)
        self.cb_pick_stock.grid(row=0, column=1, columnspan=2, sticky='w', padx=10, pady=10)
        btn_update_stocks.grid(row=0, column=3, columnspan=2, padx=10, pady=10, sticky='e')
        l_period.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        chbtn_all_period.grid(row=1, column=1, padx=10, pady=10)
        self.de_period1.grid(row=1, column=2, padx=10, pady=10)
        l_dash.grid(row=1, column=3)
        self.de_period2.grid(row=1, column=4, padx=10, pady=10)
        btn_add.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        btn_del.grid(row=2, column=2, padx=10, pady=10)
        btn_actual.grid(row=2, column=3, columnspan=2, padx=10, pady=10, sticky='e')

        self.cb_pick_stock.bind('<<ComboboxSelected>>', self.refresh_widgets_add_stock_frame)

    def refresh_widgets_add_stock_frame(self, event):
        if self.flag_all_period.get():
            self.begin_end_date = db_maker.get_begin_end_date(self.cb_pick_stock.get())
            print(self.begin_end_date)
            self.de_period1.set_date(self.begin_end_date[0])
            self.de_period2.set_date(self.begin_end_date[1])

    def widgets_stat_frame(self):
        l_graphic = tk.Label(self.frame_stat, text='Получение отчётов')
        btn_stat_cost = tk.Button(self.frame_stat, text='Динамика стоимости')
        btn_stat_profit = tk.Button(self.frame_stat, text='Динамика доходности')

        l_graphic.pack(padx=10, pady=12)
        btn_stat_cost.pack(padx=10, pady=10)
        btn_stat_profit.pack(padx=10, pady=10)

    def widgets_db_frame(self):
        l_db = tk.Label(self.frame_db, text='База данных')
        table_scroll = tk.Scrollbar(self.frame_db)
        table_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        table = ttk.Treeview(self.frame_db, yscrollcommand=table_scroll.set)
        table['columns'] = ['id', 'stock_name', 'all_period', 'from_date', 'to_date']
        table.column("#0", width=0, stretch=tk.NO)
        table.column("id", anchor=tk.CENTER, width=60)
        table.column("stock_name", anchor=tk.CENTER, width=180)
        table.column("all_period", anchor=tk.CENTER, width=60)
        table.column("from_date", anchor=tk.CENTER, width=210)
        table.column("to_date", anchor=tk.CENTER, width=210)

        # Create Headings
        table.heading("#0", text="", anchor=tk.CENTER)
        table.heading("id", text="Id", anchor=tk.CENTER)
        table.heading("stock_name", text="Name of stock", anchor=tk.CENTER)
        table.heading("all_period", text="all_period", anchor=tk.CENTER)
        table.heading("from_date", text="from_date", anchor=tk.CENTER)
        table.heading("to_date", text="to_date", anchor=tk.CENTER)
        table.pack()
        table_scroll.config(command=table.yview)


def create_app():
    app = App()
    app.mainloop()

