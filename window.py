import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from tkcalendar import DateEntry, Calendar
import pandas as pd
import datetime
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
        self.__run()

    def __run(self):
        self.__put_frames()
        self.__widgets_add_stock_frame()
        self.__widgets_stat_frame()
        self.__widgets_db_frame()

    def __put_frames(self):
        self.frame_add_stock.grid(row=0, column=0, sticky='nesw')
        self.frame_stat.grid(row=0, column=1, sticky='nesw')
        self.frame_db.grid(row=1, column=0, columnspan=2, sticky='nesw')

    def __widgets_add_stock_frame(self):
        self.list_stocks = dbm.get_current_list_stocks()
        l_pick_stock = tk.Label(self.frame_add_stock, text='Выбор акции:')
        l_period = tk.Label(self.frame_add_stock, text='Период:')
        self.cb_pick_stock = ttk.Combobox(self.frame_add_stock,
                                     values=self.list_stocks,
                                     justify=tk.CENTER,
                                     state='readonly')
        btn_update_stocks = tk.Button(self.frame_add_stock,
                                      text='Обновить акции',
                                      command=self.__refresh_list_of_stocks)
        chbtn_all_period = tk.Checkbutton(self.frame_add_stock,
                                          text='Весь период',
                                          command=self.__pressed_checkbutton,
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
        btn_add = tk.Button(self.frame_add_stock, text='Добавить', command=self.__add_stock)
        btn_del = tk.Button(self.frame_add_stock, text='Удалить всё', command=self.__deleting)
        btn_actual = tk.Button(self.frame_add_stock, text='Актуализация', command=self.__actualize)
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
        self.cb_pick_stock.bind('<<ComboboxSelected>>', self.__picked_stock)
        self.de_period1.bind('<<DateEntrySelected>>', self.__picked_first_date)
        self.de_period2.bind('<<DateEntrySelected>>', self.__picked_second_date)

    def __picked_stock(self, event):
        self.name_of_stock = self.cb_pick_stock.get()
        self.begin_end_date = dbm.get_begin_end_date(self.name_of_stock)
        if self.flag_all_period.get() == 1:
            self.de_period1.set_date(self.begin_end_date[0])
            self.de_period2.set_date(self.begin_end_date[1])
        self.first_date = self.de_period1.get_date()
        self.second_date = self.de_period2.get_date()

    def __pressed_checkbutton(self):
        if self.name_of_stock != '':
            if self.flag_all_period.get() == 1:
                self.de_period1.set_date(self.begin_end_date[0])
                self.first_date = self.begin_end_date[0]
                self.de_period2.set_date(self.begin_end_date[1])
                self.second_date = self.begin_end_date[1]
            else:
                self.first_date = self.begin_end_date[0] + datetime.timedelta(days=1)
                self.de_period1.set_date(self.first_date)

    def __picked_first_date(self, event):
        self.first_date = self.de_period1.get_date()
        self.second_date = self.de_period2.get_date()
        if self.name_of_stock != '':
            if self.begin_end_date[0] > self.first_date or self.first_date >= self.second_date:
                self.de_period1.set_date(self.begin_end_date[0])
                self.first_date = self.begin_end_date[0]
                self.__warning()
            self.__check_all_period()

    def __picked_second_date(self, event):
        self.first_date = self.de_period1.get_date()
        self.second_date = self.de_period2.get_date()
        if self.name_of_stock != '':
            if self.begin_end_date[1] < self.second_date:
                self.de_period2.set_date(self.begin_end_date[1])
                self.second_date = self.begin_end_date[1]
                self.__warning()
            if self.second_date <= self.first_date:
                self.de_period2.set_date(self.begin_end_date[1])
                self.second_date = self.begin_end_date[1]
                self.__warning()
            self.__check_all_period()

    def __warning(self):
        warning = 'Акция торгуется с ' + str(self.begin_end_date[0]) + ' по ' + str(self.begin_end_date[1])
        warning += '.\nДля обновления информации нажмите "Обновить акции".'
        mb.showwarning('Внимание', warning)

    def __refresh_list_of_stocks(self):
        dbm.truncate_table_stocks()
        dbm.update_list_of_stocks()
        self.list_stocks = dbm.get_current_list_stocks()
        self.cb_pick_stock.configure(values=self.list_stocks)

    def __check_all_period(self):
        self.first_date = self.de_period1.get_date()
        self.second_date = self.de_period2.get_date()
        if self.first_date == self.begin_end_date[0] and self.second_date == self.begin_end_date[1]:
            self.flag_all_period.set(1)
        else:
            self.flag_all_period.set(0)

    def __add_stock(self):
        if self.name_of_stock != '':
            if self.first_date < self.begin_end_date[0] and self.second_date > self.begin_end_date[1]:
                self.__set_begin_end()
                self.__warning()
            elif self.first_date < self.begin_end_date[0]:
                self.__set_begin_end()
                self.__warning()
            elif self.second_date > self.begin_end_date[1]:
                self.__set_begin_end()
                self.__warning()
            else:
                answer = dbm.add_to_db(self.name_of_stock,
                                       bool(self.flag_all_period.get()),
                                       self.first_date,
                                       self.second_date)
                if answer is False:
                    mb.showwarning('Внимание', 'Данные по акции не скачались')
                else:
                    self.list_database = dbm.get_current_list_database()
                    self.table.insert('', tk.END, values=self.list_database[-1])
        else:
            warning = 'Выберите акцию'
            mb.showwarning('Внимание', warning)

    def __set_begin_end(self):
        self.de_period1.set_date(self.begin_end_date[0])
        self.first_date = self.begin_end_date[0]
        self.de_period2.set_date(self.begin_end_date[1])
        self.second_date = self.begin_end_date[1]
        self.flag_all_period.set(1)

    def __deleting(self):
        for i in self.table.get_children():
            self.table.delete(i)
        dbm.delete_tables()
        dbm.create_db()

    def __widgets_stat_frame(self):
        l_graphic = tk.Label(self.frame_stat, text='Получение отчётов')
        btn_stat_cost = tk.Button(self.frame_stat, text='Динамика стоимости', command=self.__new_window_cost)
        btn_stat_profit = tk.Button(self.frame_stat, text='Динамика доходности', command=self.__new_window_profit)
        l_graphic.pack(padx=10, pady=12)
        btn_stat_cost.pack(padx=10, pady=10)
        btn_stat_profit.pack(padx=10, pady=10)

    def __widgets_db_frame(self):
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

    def __actualize(self):
        dbm.actualize()
        self.list_database = dbm.get_current_list_database()
        for i in self.table.get_children():
            self.table.delete(i)
        for row in self.list_database:
            self.table.insert('', tk.END, values=row)

    def __new_window_cost(self):
        window = Window(self, 0)
        window.grab_set()

    def __new_window_profit(self):
        window = Window(self, 1)
        window.grab_set()


class Window(tk.Toplevel):
    def __init__(self, parent, flag):
        super().__init__(parent)
        self.bool = flag
        if self.bool:
            self.title('Динамика доходности')
        else:
            self.title('Динамика стоимости')
        self['background'] = '#EBEBEB'
        self.geometry("700x400+0+0")
        self.resizable(False, False)
        self.frame_settings = tk.Frame(self)
        self.frame_graphic = tk.Frame(self)
        self.flag_download = False
        self.frame_settings.pack(side='left', fill='y')
        self.frame_graphic.pack(side='right')
        self.__widgets_settings()

    def __widgets_settings(self):
        self.btn_graphic = tk.Button(self.frame_settings, text='График', command=self.__draw)
        self.btn_excel = tk.Button(self.frame_settings, text='Скачать в excel', command=self.__excel)
        self.btn_graphic.grid(row=0, column=0, padx=10, pady=10, sticky='we')
        self.btn_excel.grid(row=1, column=0, padx=10, pady=10, sticky='we')

    def __draw(self):
        if self.bool:
            self.dct = dbm.get_tradings_profit()
        else:
            self.dct = dbm.get_current_dict_tradings()
        self.df = pd.DataFrame(self.dct)
        self.flag_download = True
        fig = plt.Figure(figsize=(5.5, 4), dpi=100)
        ax = fig.add_subplot(111)
        line = FigureCanvasTkAgg(fig, master=self.frame_graphic)
        line.get_tk_widget().grid(row=0, column=0)
        self.df.plot(x='Date', y=self.df.axes[1][1:], ax=ax, kind='line')

    def __excel(self):
        if not self.flag_download:
            mb.showwarning('Внимание', 'Нажмите на кнопку "График" перед тем как скачать отчёт')
        else:
            self.df.to_excel("output_profit.xlsx") if self.bool else self.df.to_excel("output_cost.xlsx")
            progress_bar = ttk.Progressbar(self.frame_settings,
                                           orient='horizontal',
                                           mode='determinate',
                                           maximum=100,
                                           value=0)
            label = tk.Label(self.frame_settings, text='Загрузка')
            label.grid(row=2, column=0, padx=10, pady=10, sticky='we')
            progress_bar.grid(row=3, column=0, padx=10, pady=10, sticky='we')
            self.update()
            progress_bar['value'] = 0
            self.update()
            while progress_bar['value'] < 100:
                progress_bar['value'] += 5
                self.update()
                time.sleep(0.1)


def create_app():
    app = App()
    app.mainloop()