import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry, Calendar


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('My App')
        self['background'] = '#EBEBEB'
        self.geometry("800x600+300+200")
        self.resizable(False, True)
        self.frame_add_stock = tk.Frame(self, bg='#BEBEBE', width=570)
        self.frame_stat = tk.Frame(self, bg='purple', width=230)
        self.frame_db = tk.Frame(self, bg='yellow', width=800, height=460)
        self.flag_all_period = tk.StringVar()
        self.run()

    def run(self):
        self.put_frames()
        self.widgets_add_stock_frame()
        self.widgets_stat_frame()
        self.widgets_db_frame()

    def put_frames(self):
        self.frame_add_stock.grid(row=0, column=0, sticky='nswe')
        self.frame_stat.grid(row=0, column=1, sticky='nwse')
        self.frame_db.grid(row=1, column=0, columnspan=2, sticky='ns')

    def widgets_add_stock_frame(self):
        l_pick_stock = tk.Label(self.frame_add_stock, text='Выбор акции:')
        l_period = tk.Label(self.frame_add_stock, text='Период:')
        cb_pick_stock = ttk.Combobox(self.frame_add_stock)
        rbtn_all_period = tk.Radiobutton(self.frame_add_stock, text='Весь период', variable=self.flag_all_period)
        de_period1 = DateEntry(self.frame_add_stock)
        l_dash = tk.Label(self.frame_add_stock, text='-')
        de_period2 = DateEntry(self.frame_add_stock)
        btn_add = tk.Button(self.frame_add_stock, text='Добавить')
        btn_del = tk.Button(self.frame_add_stock, text='Удалить')
        btn_actual = tk.Button(self.frame_add_stock, text='Актуализация')

        l_pick_stock.grid(row=0, column=0, padx=10, pady=10)
        cb_pick_stock.grid(row=0, column=1, columnspan=4, sticky='w', padx=10, pady=10)
        l_period.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        rbtn_all_period.grid(row=1, column=1, padx=10, pady=10)
        de_period1.grid(row=1, column=2, padx=10, pady=10)
        l_dash.grid(row=1, column=3)
        de_period2.grid(row=1, column=4, padx=10, pady=10)
        btn_add.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        btn_del.grid(row=2, column=2, padx=10, pady=10)
        btn_actual.grid(row=2, column=3, columnspan=2, padx=10, pady=10, sticky='e')

    def widgets_stat_frame(self):
        l_graphic = tk.Label(self.frame_stat, text='Получение отчётов')
        btn_stat_cost = tk.Button(self.frame_stat, text='Динамика стоимости')
        btn_stat_profit = tk.Button(self.frame_stat, text='Динамика доходности')

        l_graphic.pack(padx=10, pady=10)
        btn_stat_cost.pack(padx=10, pady=10)
        btn_stat_profit.pack(padx=10, pady=10)

    def widgets_db_frame(self):
        l_db = tk.Label(self.frame_db, text='База данных')
        table_scroll = tk.Scrollbar(self.frame_db)
        table_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        table = ttk.Treeview(self.frame_db, yscrollcommand=table_scroll.set)
        table['columns'] = ['id', 'stock_name', 'all_period', 'from_date', 'to_date']
        table.column("#0", width=0, stretch=tk.NO)
        table.column("id", anchor=tk.CENTER)
        table.column("stock_name", anchor=tk.CENTER)
        table.column("all_period", anchor=tk.CENTER)
        table.column("from_date", anchor=tk.CENTER)
        table.column("to_date", anchor=tk.CENTER)

        # Create Headings
        table.heading("#0", text="", anchor=tk.CENTER)
        table.heading("id", text="Id", anchor=tk.CENTER)
        table.heading("stock_name", text="Name of stock", anchor=tk.CENTER)
        table.heading("all_period", text="all_period", anchor=tk.CENTER)
        table.heading("from_date", text="from_date", anchor=tk.CENTER)
        table.heading("to_date", text="to_date", anchor=tk.CENTER)
        table.pack(expand=True, fill=tk.BOTH)
        table_scroll.config(command=table.yview)







def creating_app():
    app = App()
    app.mainloop()

