import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from tkcalendar import DateEntry, Calendar
import pandas as pd
import datetime

import db_maker as dbm


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('My App')
        # self['background'] = '#EBEBEB'
        self.geometry("740x345+300+200")
        self.resizable(False, False)
        self.frame_add_stock = tk.Frame(self)
        self.frame_stat = tk.Frame(self)
        self.frame_db = tk.Frame(self)

        self.flag_all_period = tk.IntVar()
        self.name_of_stock = ''
        self.first_date = datetime.datetime.now().date()
        self.second_date = datetime.datetime.now().date()

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
        self.list_stocks = dbm.get_current_list_stocks()

        l_pick_stock = tk.Label(self.frame_add_stock, text='Выбор акции:')
        l_period = tk.Label(self.frame_add_stock, text='Период:')
        self.cb_pick_stock = ttk.Combobox(self.frame_add_stock,
                                     values=self.list_stocks,
                                     justify=tk.CENTER,
                                     state='readonly')

        btn_update_stocks = tk.Button(self.frame_add_stock,
                                      text='Обновить акции',
                                      command=self.refresh_list_of_stocks)
        chbtn_all_period = tk.Checkbutton(self.frame_add_stock,
                                          text='Весь период',
                                          command=self.pressed_checkbutton,
                                          variable=self.flag_all_period,
                                          offvalue=0,
                                          onvalue=1)
        self.de_period1 = DateEntry(self.frame_add_stock,
                                    foreground='black',
                                    normalforeground='black',
                                    selectforeground='red',
                                    background='white',
                                    date_pattern='YYYY-mm-dd',
                                    state='readonly')
        l_dash = tk.Label(self.frame_add_stock, text='-')
        self.de_period2 = DateEntry(self.frame_add_stock,
                                    foreground='black',
                                    normalforeground='black',
                                    selectforeground='red',
                                    background='white',
                                    date_pattern='YYYY-mm-dd',
                                    state='readonly')

        btn_add = tk.Button(self.frame_add_stock, text='Добавить', command=self.add_stock)
        btn_del = tk.Button(self.frame_add_stock, text='Удалить всё', command=self.deleting)
        btn_actual = tk.Button(self.frame_add_stock, text='Актуализация', command=self.actualize)

        l_pick_stock.grid(row=0, column=0, padx=10, pady=10)
        self.cb_pick_stock.grid(row=0, column=1, columnspan=2, sticky='w', padx=10, pady=10)
        btn_update_stocks.grid(row=0, column=2, columnspan=3, padx=10, pady=10, sticky='e')
        l_period.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        chbtn_all_period.grid(row=1, column=1, padx=10, pady=10)
        self.de_period1.grid(row=1, column=2, padx=10, pady=10)
        l_dash.grid(row=1, column=3)
        self.de_period2.grid(row=1, column=4, padx=10, pady=10)
        btn_add.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        btn_del.grid(row=2, column=2, padx=10, pady=10)
        btn_actual.grid(row=2, column=3, columnspan=2, padx=10, pady=10, sticky='e')

        self.cb_pick_stock.bind('<<ComboboxSelected>>', self.picked_stock)
        self.de_period1.bind('<<DateEntrySelected>>', self.picked_first_date)
        self.de_period2.bind('<<DateEntrySelected>>', self.picked_second_date)

    def picked_stock(self, event):
        self.name_of_stock = self.cb_pick_stock.get()
        self.begin_end_date = dbm.get_begin_end_date(self.name_of_stock)
        if self.flag_all_period.get() == 1:
            self.de_period1.set_date(self.begin_end_date[0])
            self.de_period2.set_date(self.begin_end_date[1])
        self.first_date = self.de_period1.get_date()
        self.second_date = self.de_period2.get_date()

    def pressed_checkbutton(self):
        if self.name_of_stock != '':
            if self.flag_all_period.get() == 1:
                self.de_period1.set_date(self.begin_end_date[0])
                self.first_date = self.begin_end_date[0]
                self.de_period2.set_date(self.begin_end_date[1])
                self.second_date = self.begin_end_date[1]
            else:
                self.first_date = self.begin_end_date[0] + datetime.timedelta(days=1)
                self.de_period1.set_date(self.first_date)

    def picked_first_date(self, event):
        self.first_date = self.de_period1.get_date()
        self.second_date = self.de_period2.get_date()
        if self.name_of_stock != '':
            if self.begin_end_date[0] > self.first_date or self.first_date >= self.second_date:
                self.de_period1.set_date(self.begin_end_date[0])
                self.first_date = self.begin_end_date[0]
                self.warning()
            self.check_all_period()

    def picked_second_date(self, event):
        self.first_date = self.de_period1.get_date()
        self.second_date = self.de_period2.get_date()
        if self.name_of_stock != '':
            if self.begin_end_date[1] < self.second_date:
                self.de_period2.set_date(self.begin_end_date[1])
                self.second_date = self.begin_end_date[1]
                self.warning()
            if self.second_date <= self.first_date:
                self.de_period2.set_date(self.begin_end_date[1])
                self.second_date = self.begin_end_date[1]
                self.warning()
            self.check_all_period()

    def warning(self):
        warning = 'Акция торгуется с ' + str(self.begin_end_date[0]) + ' по ' + str(self.begin_end_date[1])
        warning += '.\nДля обновления информации нажмите "Обновить акции".'
        mb.showwarning('Внимание', warning)

    def refresh_list_of_stocks(self):
        dbm.truncate_table_stocks()
        dbm.update_list_of_stocks()
        self.list_stocks = dbm.get_current_list_stocks()
        self.cb_pick_stock.configure(values=self.list_stocks)

    def check_all_period(self):
        self.first_date = self.de_period1.get_date()
        self.second_date = self.de_period2.get_date()
        if self.first_date == self.begin_end_date[0] and self.second_date == self.begin_end_date[1]:
            self.flag_all_period.set(1)
        else:
            self.flag_all_period.set(0)

    def add_stock(self):
        if self.name_of_stock != '':
            if self.first_date < self.begin_end_date[0] and self.second_date > self.begin_end_date[1]:
                self.set_begin_end()
                self.warning()
            elif self.first_date < self.begin_end_date[0]:
                self.set_begin_end()
                self.warning()
            elif self.second_date > self.begin_end_date[1]:
                self.set_begin_end()
                self.warning()
            else:
                dbm.add_to_db(self.name_of_stock,
                              bool(self.flag_all_period.get()),
                              self.first_date,
                              self.second_date)
            self.list_database = dbm.get_current_list_database()
            self.table.insert('', tk.END, values=self.list_database[-1])
        else:
            warning = 'Выберите акцию'
            mb.showwarning('Внимание', warning)

    def set_begin_end(self):
        self.de_period1.set_date(self.begin_end_date[0])
        self.first_date = self.begin_end_date[0]
        self.de_period2.set_date(self.begin_end_date[1])
        self.second_date = self.begin_end_date[1]
        self.flag_all_period.set(1)

    def deleting(self):
        for i in self.table.get_children():
            self.table.delete(i)
        self.cb_pick_stock.configure(values=[])
        dbm.delete_tables()
        dbm.create_db()

    def widgets_stat_frame(self):
        l_graphic = tk.Label(self.frame_stat, text='Получение отчётов')
        btn_stat_cost = tk.Button(self.frame_stat, text='Динамика стоимости', command=self.new_window_cost)
        btn_stat_profit = tk.Button(self.frame_stat, text='Динамика доходности')

        l_graphic.pack(padx=10, pady=12)
        btn_stat_cost.pack(padx=10, pady=10)
        btn_stat_profit.pack(padx=10, pady=10)

    def widgets_db_frame(self):
        self.list_database = dbm.get_current_list_database()

        self.table = ttk.Treeview(self.frame_db, show='headings')
        heads = ['id', 'name', 'all_period', 'from_date', 'to_date']
        self.table['columns'] = heads
        for header in heads:
            self.table.heading(header, text=header, anchor='center')
            self.table.column(header, anchor='center')
        for row in self.list_database:
            self.table.insert('', tk.END, values=row)

        self.table.column('0', width=140)
        self.table.column('1', width=145)
        self.table.column('2', width=145)
        self.table.column('3', width=145)
        self.table.column('4', width=145)

        scroll_pane = ttk.Scrollbar(self.frame_db, command=self.table.yview)
        self.table.configure(yscrollcommand=scroll_pane.set)

        scroll_pane.pack(side=tk.RIGHT, fill='y')
        self.table.pack(expand=tk.YES, fill='both')

    def actualize(self):
        dbm.actualize()
        self.list_database = dbm.get_current_list_database()

        for i in self.table.get_children():
            self.table.delete(i)
        for row in self.list_database:
            self.table.insert('', tk.END, values=row)

    def new_window_cost(self):
        window = WindowCost(self)
        window.grab_set()


class WindowCost(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Динамика стоимости')
        self['background'] = '#EBEBEB'
        self.geometry("600x400+200+200")
        self.resizable(False, False)

        self.frame_settings = tk.Frame(self)
        self.frame_graphic = tk.Frame(self)

        self.frame_settings.pack(side='left', fill='y')
        self.frame_graphic.pack(side='right')
        self.widgets_settings()

    def widgets_settings(self):
        self.x = tk.IntVar()
        self.x.set(0)
        self.y = tk.IntVar()
        self.y.set(0)

        tk.Label(self.frame_settings, text='Дата:').grid(row=0, column=0, columnspan=2)
        self.rdbtn_day = ttk.Radiobutton(self.frame_settings, text='День', value=1, variable=self.x)
        self.rdbtn_week = ttk.Radiobutton(self.frame_settings, text='Неделя', value=2, variable=self.x)
        self.rdbtn_month = ttk.Radiobutton(self.frame_settings, text='Месяц', value=3, variable=self.x)
        self.rdbtn_year = ttk.Radiobutton(self.frame_settings, text='Год', value=4, variable=self.x)
        tk.Label(self.frame_settings, text='Цена:').grid(row=3, column=0, columnspan=2)
        self.rdbtn_open = ttk.Radiobutton(self.frame_settings, text='Открытия', value=1, variable=self.y)
        self.rdbtn_close = ttk.Radiobutton(self.frame_settings, text='Закрытия', value=2, variable=self.y)
        self.rdbtn_low = ttk.Radiobutton(self.frame_settings, text='Минимальная', value=3, variable=self.y)
        self.rdbtn_high = ttk.Radiobutton(self.frame_settings, text='Максимальная', value=4, variable=self.y)
        self.btn_graphic = tk.Button(self.frame_settings, text='График', command=self.draw)
        self.btn_excel = tk.Button(self.frame_settings, text='Скачать excel')

        self.rdbtn_day.grid(row=1, column=0, padx=10, pady=10, sticky='we')
        self.rdbtn_week.grid(row=1, column=1, padx=10, pady=10, sticky='we')
        self.rdbtn_month.grid(row=2, column=0, padx=10, pady=10, sticky='we')
        self.rdbtn_year.grid(row=2, column=1, padx=10, pady=10, sticky='we')
        self.rdbtn_open.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='nswe')
        self.rdbtn_close.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='nswe')
        self.rdbtn_low.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky='nswe')
        self.rdbtn_high.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky='nswe')
        self.btn_graphic.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky='we')
        self.btn_excel.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky='we')

    def draw(self):
        if self.x.get() == self.y.get() == 0:
            mb.showwarning('Внимание', 'Выберите систему координат')
        elif self.x.get() * self.y.get() != 0:
            self.list_tradings = dbm.get_current_list_tradings()
            self.df = pd.DataFrame(self.list_tradings)





def create_app():
    app = App()
    app.mainloop()

