import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry, Calendar





def creating_app():
    window = tk.Tk()
    window.title('My App')
    frame_add_stock = tk.Frame(window, bg='blue')
    frame_actual = tk.Frame(window, bg='purple')
    frame_bd = tk.Frame(window, bg='yellow')
    frame_stat = tk.Frame(window, bg='grey')

    frame_add_stock.grid(row=0, column=0, sticky='ns')
    frame_actual.grid(row=0, column=1, sticky='ns')
    frame_bd.grid(row=1, column=0, columnspan=2, sticky='we')
    frame_stat.grid(row=2, column=0, columnspan=2, sticky='we')

    l_pick_stock = ttk.Label(frame_add_stock, text='Выбор акции:')
    l_quantity = ttk.Label(frame_add_stock, text='Количество:')
    l_period = ttk.Label(frame_add_stock, text='Период:')
    lb_pick_stock = ttk.Combobox(frame_add_stock)
    lb_quantity = ttk.Spinbox(frame_add_stock, justify=tk.RIGHT)
    e_period1 = DateEntry(frame_add_stock)
    l_dash = ttk.Label(frame_add_stock, text='-')
    e_period2 = DateEntry(frame_add_stock)
    btn_add = ttk.Button(frame_add_stock, text='Добавить')
    btn_del = ttk.Button(frame_add_stock, text='Удалить')

    l_pick_stock.grid(row=0, column=0, sticky='w', padx=5, pady=5)
    l_quantity.grid(row=1, column=0, sticky='w', padx=5, pady=5)
    l_period.grid(row=2, column=0, sticky='w', padx=5, pady=5)
    lb_pick_stock.grid(row=0, column=1, columnspan=3, sticky='e', padx=5, pady=5)
    lb_quantity.grid(row=1, column=1, columnspan=3, sticky='e', padx=5, pady=5)
    e_period1.grid(row=2, column=1, padx=5, pady=5)
    l_dash.grid(row=2, column=2)
    e_period2.grid(row=2, column=3, padx=5, pady=5)
    btn_add.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='e')
    btn_del.grid(row=3, column=2, columnspan=2, padx=5, pady=5)

    btn_actual = ttk.Button(frame_actual, text='Режим актуализации')

    btn_actual.grid(pady=50, padx=5)

    window.mainloop()
