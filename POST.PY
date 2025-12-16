import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import re

DB_NAME = "post_office.db"

PARCEL_TYPES = ["Письмо", "Бандероль", "Посылка", "Одежда", "Электроника", "Посуда"]
PARCEL_STATUS = ["Принято", "В пути", "В отделении", "Доставлено", "Возврат"]
PAYMENT_METHODS = ["Наличные", "Банковская карта", "СБП"]


def db_connect():
    return sqlite3.connect(DB_NAME)


def get_column_values(table, column):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute(f"SELECT {column} FROM {table}")
    values = [str(v[0]) for v in cur.fetchall()]
    conn.close()
    return values


class BasePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#000")

    def create_tree(self, columns, headings):
        frame = tk.Frame(self, bg="#000")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        tree = ttk.Treeview(frame, columns=columns, show="headings", height=14)
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        for col, head, w in headings:
            tree.heading(col, text=head)
            tree.column(col, width=w, anchor="center")

        return tree


class ClientPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_id = None
        self.build_ui()
        self.load_data()

    def build_ui(self):
        cols = ("id", "fio", "tel", "addr")
        heads = [
            ("id", "ID", 60),
            ("fio", "ФИО", 220),
            ("tel", "Телефон", 120),
            ("addr", "Адрес", 260),
        ]
        self.tree = self.create_tree(cols, heads)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        form = tk.Frame(self, bg="#000")
        form.pack(fill="x", padx=20, pady=5)

        self.fio_var = tk.StringVar()
        self.tel_var = tk.StringVar()
        self.adr_var = tk.StringVar()

        tk.Label(form, text="ФИО", fg="white", bg="#000").grid(row=0, column=0, sticky="w")
        tk.Entry(form, textvariable=self.fio_var).grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(form, text="Телефон", fg="white", bg="#000").grid(row=1, column=0, sticky="w")
        tk.Entry(form, textvariable=self.tel_var).grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(form, text="Адрес", fg="white", bg="#000").grid(row=2, column=0, sticky="w")
        tk.Entry(form, textvariable=self.adr_var).grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        form.columnconfigure(1, weight=1)

        btns = tk.Frame(self, bg="#000")
        btns.pack(fill="x", padx=20, pady=5)

        tk.Button(btns, text="Добавить", command=self.add).pack(side="left", padx=5)
        tk.Button(btns, text="Обновить", command=self.update).pack(side="left", padx=5)
        tk.Button(btns, text="Удалить", command=self.delete).pack(side="left", padx=5)
        tk.Button(btns, text="Очистить", command=self.clear_form).pack(side="left", padx=5)

    def load_data(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("SELECT ID_Клиента, ФИО, Телефон, Адрес FROM Клиент")
        for row in cur.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, _):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        self.selected_id = int(vals[0])
        self.fio_var.set(vals[1])
        self.tel_var.set(vals[2])
        self.adr_var.set(vals[3])

    def clear_form(self):
        self.selected_id = None
        self.fio_var.set("")
        self.tel_var.set("")
        self.adr_var.set("")
        self.tree.selection_remove(self.tree.selection())

    def add(self):
        conn = db_connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Клиент (ФИО, Телефон, Адрес) VALUES (?, ?, ?)",
            (self.fio_var.get(), self.tel_var.get(), self.adr_var.get())
        )
        conn.commit()
        conn.close()
        self.clear_form()
        self.load_data()

    def update(self):
        if self.selected_id is None:
            messagebox.showerror("Ошибка", "Выберите клиента")
            return
        conn = db_connect()
        cur = conn.cursor()
        cur.execute(
            "UPDATE Клиент SET ФИО=?, Телефон=?, Адрес=? WHERE ID_Клиента=?",
            (self.fio_var.get(), self.tel_var.get(), self.adr_var.get(), self.selected_id)
        )
        conn.commit()
        conn.close()
        self.load_data()

    def delete(self):
        if self.selected_id is None:
            messagebox.showerror("Ошибка", "Выберите клиента")
            return
        if not messagebox.askyesno("Подтверждение", "Удалить клиента?"):
            return
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM Клиент WHERE ID_Клиента=?", (self.selected_id,))
        conn.commit()
        conn.close()
        self.clear_form()
        self.load_data()


class BranchPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_id = None
        self.build_ui()
        self.load_data()

    def build_ui(self):
        cols = ("id", "name", "addr")
        heads = [
            ("id", "ID", 60),
            ("name", "Название", 220),
            ("addr", "Адрес", 300),
        ]
        self.tree = self.create_tree(cols, heads)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        form = tk.Frame(self, bg="#000")
        form.pack(fill="x", padx=20, pady=5)

        self.id_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.addr_var = tk.StringVar()

        tk.Label(form, text="ID отделения", fg="white", bg="#000").grid(row=0, column=0, sticky="w")
        tk.Entry(form, textvariable=self.id_var).grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(form, text="Название", fg="white", bg="#000").grid(row=1, column=0, sticky="w")
        tk.Entry(form, textvariable=self.name_var).grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(form, text="Адрес", fg="white", bg="#000").grid(row=2, column=0, sticky="w")
        tk.Entry(form, textvariable=self.addr_var).grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        form.columnconfigure(1, weight=1)

        btns = tk.Frame(self, bg="#000")
        btns.pack(fill="x", padx=20, pady=5)

        tk.Button(btns, text="Добавить", command=self.add).pack(side="left", padx=5)
        tk.Button(btns, text="Обновить", command=self.update).pack(side="left", padx=5)
        tk.Button(btns, text="Удалить", command=self.delete).pack(side="left", padx=5)
        tk.Button(btns, text="Очистить", command=self.clear_form).pack(side="left", padx=5)

    def load_data(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("SELECT ID_Отделения, Название, Адрес FROM Отделение")
        for row in cur.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, _):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        self.selected_id = int(vals[0])
        self.id_var.set(vals[0])
        self.name_var.set(vals[1])
        self.addr_var.set(vals[2])

    def clear_form(self):
        self.selected_id = None
        self.id_var.set("")
        self.name_var.set("")
        self.addr_var.set("")
        self.tree.selection_remove(self.tree.selection())

    def add(self):
        if not self.id_var.get().isdigit():
            messagebox.showerror("Ошибка", "ID должен быть числом")
            return
        conn = db_connect()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO Отделение (ID_Отделения, Название, Адрес) VALUES (?, ?, ?)",
                (int(self.id_var.get()), self.name_var.get(), self.addr_var.get())
            )
            conn.commit()
        except sqlite3.IntegrityError:
            messagebox.showerror("Ошибка", "ID уже существует")
        conn.close()
        self.load_data()

    def update(self):
        if self.selected_id is None:
            messagebox.showerror("Ошибка", "Выберите отделение")
            return
        if not self.id_var.get().isdigit():
            messagebox.showerror("Ошибка", "ID должен быть числом")
            return
        conn = db_connect()
        cur = conn.cursor()
        cur.execute(
            "UPDATE Отделение SET ID_Отделения=?, Название=?, Адрес=? WHERE ID_Отделения=?",
            (int(self.id_var.get()), self.name_var.get(), self.addr_var.get(), self.selected_id)
        )
        conn.commit()
        conn.close()
        self.load_data()

    def delete(self):
        if self.selected_id is None:
            messagebox.showerror("Ошибка", "Выберите отделение")
            return
        if not messagebox.askyesno("Подтверждение", "Удалить отделение?"):
            return
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM Отделение WHERE ID_Отделения=?", (self.selected_id,))
        conn.commit()
        conn.close()
        self.clear_form()
        self.load_data()


class OperatorPage(BasePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_id = None
        self.build_ui()
        self.load_data()

    def build_ui(self):
        cols = ("id", "fio", "pos", "branch")
        heads = [
            ("id", "ID", 60),
            ("fio", "ФИО", 220),
            ("pos", "Должность", 150),
            ("branch", "ID отделения", 100),
        ]
        self.tree = self.create_tree(cols, heads)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        form = tk.Frame(self, bg="#000")
        form.pack(fill="x", padx=20, pady=5)

        self.fio_var = tk.StringVar()
        self.pos_var = tk.StringVar()
        self.branch_var = tk.StringVar()

        tk.Label(form, text="ФИО", fg="white", bg="#000").grid(row=0, column=0, sticky="w")
        tk.Entry(form, textvariable=self.fio_var).grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(form, text="Должность", fg="white", bg="#000").grid(row=1, column=0, sticky="w")
        tk.Entry(form, textvariable=self.pos_var).grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(form, text="ID отделения", fg="white", bg="#000").grid(row=2, column=0, sticky="w")
        self.branch_cb = ttk.Combobox(form, textvariable=self.branch_var,
                                      values=get_column_values("Отделение", "ID_Отделения"),
                                      state="readonly")
        self.branch_cb.grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        form.columnconfigure(1, weight=1)

        btns = tk.Frame(self, bg="#000")
        btns.pack(fill="x", padx=20, pady=5)

        tk.Button(btns, text="Добавить", command=self.add).pack(side="left", padx=5)
        tk.Button(btns, text="Обновить", command=self.update).pack(side="left", padx=5)
        tk.Button(btns, text="Удалить", command=self.delete).pack(side="left", padx=5)
        tk.Button(btns, text="Очистить", command=self.clear_form).pack(side="left", padx=5)

    def reload_branch_ids(self):
        self.branch_cb["values"] = get_column_values("Отделение", "ID_Отделения")

    def load_data(self):
        self.reload_branch_ids()
        for r in self.tree.get_children():
            self.tree.delete(r)
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("SELECT ID_Оператора, ФИО, Должность, ID_Отделения FROM Оператор")
        for row in cur.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, _):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        self.selected_id = int(vals[0])
        self.fio_var.set(vals[1])
        self.pos_var.set(vals[2])
        self.branch_var.set(str(vals[3]))

    def clear_form(self):
        self.selected_id = None
        self.fio_var.set("")
        self.pos_var.set("")
        self.branch_var.set("")
        self.tree.selection_remove(self.tree.selection())

    def add(self):
        if not self.branch_var.get():
            messagebox.showerror("Ошибка", "Выберите ID отделения")
            return
        conn = db_connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Оператор (ФИО, Должность, ID_Отделения) VALUES (?, ?, ?)",
            (self.fio_var.get(), self.pos_var.get(), int(self.branch_var.get()))
        )
        conn.commit()
        conn.close()
        self.clear_form()
        self.load_data()

    def update(self):
        if self.selected_id is None:
            messagebox.showerror("Ошибка", "Выберите оператора")
            return
        if not self.branch_var.get():
            messagebox.showerror("Ошибка", "Выберите ID отделения")
            return
        conn = db_connect()
        cur = conn.cursor()
        cur.execute(
            "UPDATE Оператор SET ФИО=?, Должность=?, ID_Отделения=? WHERE ID_Оператора=?",
            (self.fio_var.get(), self.pos_var.get(), int(self.branch_var.get()), self.selected_id)
        )
        conn.commit()
        conn.close()
        self.load_data()

    def delete(self):
        if self.selected_id is None:
            messagebox.showerror("Ошибка", "Выберите оператора")
            return
        if not messagebox.askyesno("Подтверждение", "Удалить оператора?"):
            return
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM Оператор WHERE ID_Оператора=?", (self.selected_id,))
        conn.commit()
        conn.close()
        self.clear_form()
        self.load_data()


class ParcelPage(BasePage):
    DATE_RE = re.compile(r"\d{2}\.\d{2}\.\d{4}")

    def __init__(self, parent):
        super().__init__(parent)
        self.selected_id = None
        self.build_ui()
        self.load_data()

    def build_ui(self):
        cols = ("id", "cid", "oid", "bid", "typ", "w", "d", "st")
        heads = [
            ("id", "ID", 50),
            ("cid", "Клиент", 70),
            ("oid", "Оператор", 70),
            ("bid", "Отделение", 80),
            ("typ", "Тип", 80),
            ("w", "Вес", 60),
            ("d", "Дата приёма", 100),
            ("st", "Статус", 100),
        ]
        self.tree = self.create_tree(cols, heads)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        form = tk.Frame(self, bg="#000")
        form.pack(fill="x", padx=20, pady=5)

        self.cid_var = tk.StringVar()
        self.oid_var = tk.StringVar()
        self.bid_var = tk.StringVar()
        self.typ_var = tk.StringVar()
        self.w_var = tk.StringVar()
        self.d_var = tk.StringVar()
        self.st_var = tk.StringVar()

        tk.Label(form, text="Клиент", fg="white", bg="#000").grid(row=0, column=0, sticky="w")
        self.cid_cb = ttk.Combobox(form, textvariable=self.cid_var,
                                   values=get_column_values("Клиент", "ID_Клиента"),
                                   state="readonly")
        self.cid_cb.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(form, text="Оператор", fg="white", bg="#000").grid(row=0, column=2, sticky="w")
        self.oid_cb = ttk.Combobox(form, textvariable=self.oid_var,
                                   values=get_column_values("Оператор", "ID_Оператора"),
                                   state="readonly")
        self.oid_cb.grid(row=0, column=3, sticky="ew", padx=5, pady=2)

        tk.Label(form, text="Отделение", fg="white", bg="#000").grid(row=1, column=0, sticky="w")
        self.bid_cb = ttk.Combobox(form, textvariable=self.bid_var,
                                   values=get_column_values("Отделение", "ID_Отделения"),
                                   state="readonly")
        self.bid_cb.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(form, text="Тип", fg="white", bg="#000").grid(row=1, column=2, sticky="w")
        self.typ_cb = ttk.Combobox(form, textvariable=self.typ_var,
                                   values=PARCEL_TYPES, state="readonly")
        self.typ_cb.grid(row=1, column=3, sticky="ew", padx=5, pady=2)

        tk.Label(form, text="Вес (кг)", fg="white", bg="#000").grid(row=2, column=0, sticky="w")
        tk.Entry(form, textvariable=self.w_var).grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(form, text="Дата (дд.мм.гггг)", fg="white", bg="#000").grid(row=2, column=2, sticky="w")
        tk.Entry(form, textvariable=self.d_var).grid(row=2, column=3, sticky="ew", padx=5, pady=2)

        tk.Label(form, text="Статус", fg="white", bg="#000").grid(row=3, column=0, sticky="w")
        self.st_cb = ttk.Combobox(form, textvariable=self.st_var,
                                  values=PARCEL_STATUS, state="readonly")
        self.st_cb.grid(row=3, column=1, sticky="ew", padx=5, pady=2)

        for c in (1, 3):
            form.columnconfigure(c, weight=1)

        btns = tk.Frame(self, bg="#000")
        btns.pack(fill="x", padx=20, pady=5)

        tk.Button(btns, text="Добавить", command=self.add).pack(side="left", padx=5)
        tk.Button(btns, text="Обновить", command=self.update).pack(side="left", padx=5)
        tk.Button(btns, text="Удалить", command=self.delete).pack(side="left", padx=5)
        tk.Button(btns, text="Очистить", command=self.clear_form).pack(side="left", padx=5)

    def reload_refs(self):
        self.cid_cb["values"] = get_column_values("Клиент", "ID_Клиента")
        self.oid_cb["values"] = get_column_values("Оператор", "ID_Оператора")
        self.bid_cb["values"] = get_column_values("Отделение", "ID_Отделения")

    def load_data(self):
        self.reload_refs()
        for r in self.tree.get_children():
            self.tree.delete(r)
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT ID_Отпр, ID_Клиента, ID_Оператора, ID_Отделения,
                   Тип, Вес, Дата_приема, Статус
            FROM Отправление
        """)
        for row in cur.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, _):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        self.selected_id = int(vals[0])
        self.cid_var.set(str(vals[1]))
        self.oid_var.set(str(vals[2]))
        self.bid_var.set(str(vals[3]))
        self.typ_var.set(vals[4])
        self.w_var.set(str(vals[5]))
        self.d_var.set(vals[6])
        self.st_var.set(vals[7])

    def clear_form(self):
        self.selected_id = None
        self.cid_var.set("")
        self.oid_var.set("")
        self.bid_var.set("")
        self.typ_var.set("")
        self.w_var.set("")
        self.d_var.set("")
        self.st_var.set("")
        self.tree.selection_remove(self.tree.selection())

    def _validate(self):
        if not (self.cid_var.get() and self.oid_var.get() and self.bid_var.get()):
            messagebox.showerror("Ошибка", "Выберите клиента, оператора и отделение")
            return False
        try:
            float(self.w_var.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Вес — число")
            return False
        if not self.DATE_RE.fullmatch(self.d_var.get()):
            messagebox.showerror("Ошибка", "Дата в формате дд.мм.гггг")
            return False
        return True

    def add(self):
        if not self._validate():
            return
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Отправление
            (ID_Клиента, ID_Оператора, ID_Отделения, Тип, Вес, Дата_приема, Статус)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (int(self.cid_var.get()), int(self.oid_var.get()), int(self.bid_var.get()),
              self.typ_var.get(), float(self.w_var.get()),
              self.d_var.get(), self.st_var.get()))
        conn.commit()
        conn.close()
        self.clear_form()
        self.load_data()

    def update(self):
        if self.selected_id is None:
            messagebox.showerror("Ошибка", "Выберите отправление")
            return
        if not self._validate():
            return
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Отправление
            SET ID_Клиента=?, ID_Оператора=?, ID_Отделения=?,
                Тип=?, Вес=?, Дата_приема=?, Статус=?
            WHERE ID_Отпр=?
        """, (int(self.cid_var.get()), int(self.oid_var.get()), int(self.bid_var.get()),
              self.typ_var.get(), float(self.w_var.get()),
              self.d_var.get(), self.st_var.get(), self.selected_id))
        conn.commit()
        conn.close()
        self.load_data()

    def delete(self):
        if self.selected_id is None:
            messagebox.showerror("Ошибка", "Выберите отправление")
            return
        if not messagebox.askyesno("Подтверждение", "Удалить отправление?"):
            return
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM Отправление WHERE ID_Отпр=?", (self.selected_id,))
        conn.commit()
        conn.close()
        self.clear_form()
        self.load_data()


class PaymentPage(BasePage):
    DATE_RE = re.compile(r"\d{2}\.\d{2}\.\d{4}")

    def __init__(self, parent):
        super().__init__(parent)
        self.selected_id = None
        self.build_ui()
        self.load_data()

    def build_ui(self):
        cols = ("id", "pid", "sum", "date", "meth")
        heads = [
            ("id", "ID", 50),
            ("pid", "ID отправления", 110),
            ("sum", "Сумма", 80),
            ("date", "Дата оплаты", 100),
            ("meth", "Способ", 120),
        ]
        self.tree = self.create_tree(cols, heads)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        form = tk.Frame(self, bg="#000")
        form.pack(fill="x", padx=20, pady=5)

        self.parcel_var = tk.StringVar()
        self.sum_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.meth_var = tk.StringVar()

        tk.Label(form, text="Отправление", fg="white", bg="#000").grid(row=0, column=0, sticky="w")
        self.parcel_cb = ttk.Combobox(form, textvariable=self.parcel_var,
                                      values=get_column_values("Отправление", "ID_Отпр"),
                                      state="readonly")
        self.parcel_cb.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(form, text="Сумма", fg="white", bg="#000").grid(row=0, column=2, sticky="w")
        tk.Entry(form, textvariable=self.sum_var).grid(row=0, column=3, sticky="ew", padx=5, pady=2)

        tk.Label(form, text="Дата (дд.мм.гггг)", fg="white", bg="#000").grid(row=1, column=0, sticky="w")
        tk.Entry(form, textvariable=self.date_var).grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(form, text="Способ", fg="white", bg="#000").grid(row=1, column=2, sticky="w")
        self.meth_cb = ttk.Combobox(form, textvariable=self.meth_var,
                                    values=PAYMENT_METHODS, state="readonly")
        self.meth_cb.grid(row=1, column=3, sticky="ew", padx=5, pady=2)

        for c in (1, 3):
            form.columnconfigure(c, weight=1)

        btns = tk.Frame(self, bg="#000")
        btns.pack(fill="x", padx=20, pady=5)

        tk.Button(btns, text="Добавить", command=self.add).pack(side="left", padx=5)
        tk.Button(btns, text="Обновить", command=self.update).pack(side="left", padx=5)
        tk.Button(btns, text="Удалить", command=self.delete).pack(side="left", padx=5)
        tk.Button(btns, text="Очистить", command=self.clear_form).pack(side="left", padx=5)

    def reload_refs(self):
        self.parcel_cb["values"] = get_column_values("Отправление", "ID_Отпр")

    def load_data(self):
        self.reload_refs()
        for r in self.tree.get_children():
            self.tree.delete(r)
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT ID_Платежа, ID_Отпр, Сумма, Дата_оплаты, Способ_оплаты
            FROM Платеж
        """)
        for row in cur.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, _):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        self.selected_id = int(vals[0])
        self.parcel_var.set(str(vals[1]))
        self.sum_var.set(str(vals[2]))
        self.date_var.set(vals[3])
        self.meth_var.set(vals[4])

    def clear_form(self):
        self.selected_id = None
        self.parcel_var.set("")
        self.sum_var.set("")
        self.date_var.set("")
        self.meth_var.set("")
        self.tree.selection_remove(self.tree.selection())

    def _validate(self):
        if not self.parcel_var.get():
            messagebox.showerror("Ошибка", "Выберите отправление")
            return False
        try:
            float(self.sum_var.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Сумма — число")
            return False
        if not self.DATE_RE.fullmatch(self.date_var.get()):
            messagebox.showerror("Ошибка", "Дата в формате дд.мм.гггг")
            return False
        return True

    def add(self):
        if not self._validate():
            return
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Платеж (ID_Отпр, Сумма, Дата_оплаты, Способ_оплаты)
            VALUES (?, ?, ?, ?)
        """, (int(self.parcel_var.get()), float(self.sum_var.get()),
              self.date_var.get(), self.meth_var.get()))
        conn.commit()
        conn.close()
        self.clear_form()
        self.load_data()

    def update(self):
        if self.selected_id is None:
            messagebox.showerror("Ошибка", "Выберите платеж")
            return
        if not self._validate():
            return
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Платеж
            SET ID_Отпр=?, Сумма=?, Дата_оплаты=?, Способ_оплаты=?
            WHERE ID_Платежа=?
        """, (int(self.parcel_var.get()), float(self.sum_var.get()),
              self.date_var.get(), self.meth_var.get(), self.selected_id))
        conn.commit()
        conn.close()
        self.load_data()

    def delete(self):
        if self.selected_id is None:
            messagebox.showerror("Ошибка", "Выберите платеж")
            return
        if not messagebox.askyesno("Подтверждение", "Удалить платеж?"):
            return
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM Платеж WHERE ID_Платежа=?", (self.selected_id,))
        conn.commit()
        conn.close()
        self.clear_form()
        self.load_data()


class RoutePage(BasePage):
    DATE_RE = re.compile(r"\d{2}\.\d{2}\.\d{4}")

    def __init__(self, parent):
        super().__init__(parent)
        self.selected_id = None
        self.build_ui()
        self.load_data()

    def build_ui(self):
        cols = ("id", "pid", "from", "to", "d1", "d2")
        heads = [
            ("id", "ID", 50),
            ("pid", "Отпр.", 60),
            ("from", "Отправка", 80),
            ("to", "Прибытие", 80),
            ("d1", "Дата отправки", 110),
            ("d2", "Дата прибытия", 110),
        ]
        self.tree = self.create_tree(cols, heads)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        form = tk.Frame(self, bg="#000")
        form.pack(fill="x", padx=20, pady=5)

        self.parcel_var = tk.StringVar()
        self.from_var = tk.StringVar()
        self.to_var = tk.StringVar()
        self.d1_var = tk.StringVar()
        self.d2_var = tk.StringVar()

        tk.Label(form, text="Отправление", fg="white", bg="#000").grid(row=0, column=0, sticky="w")
        self.parcel_cb = ttk.Combobox(form, textvariable=self.parcel_var,
                                      values=get_column_values("Отправление", "ID_Отпр"),
                                      state="readonly")
        self.parcel_cb.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(form, text="Отделение отправки", fg="white", bg="#000").grid(row=1, column=0, sticky="w")
        self.from_cb = ttk.Combobox(form, textvariable=self.from_var,
                                    values=get_column_values("Отделение", "ID_Отделения"),
                                    state="readonly")
        self.from_cb.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(form, text="Отделение прибытия", fg="white", bg="#000").grid(row=1, column=2, sticky="w")
        self.to_cb = ttk.Combobox(form, textvariable=self.to_var,
                                  values=get_column_values("Отделение", "ID_Отделения"),
                                  state="readonly")
        self.to_cb.grid(row=1, column=3, sticky="ew", padx=5, pady=2)

        tk.Label(form, text="Дата отправки (дд.мм.гггг)", fg="white", bg="#000").grid(row=2, column=0, sticky="w")
        tk.Entry(form, textvariable=self.d1_var).grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(form, text="Дата прибытия (дд.мм.гггг)", fg="white", bg="#000").grid(row=2, column=2, sticky="w")
        tk.Entry(form, textvariable=self.d2_var).grid(row=2, column=3, sticky="ew", padx=5, pady=2)

        for c in (1, 3):
            form.columnconfigure(c, weight=1)

        btns = tk.Frame(self, bg="#000")
        btns.pack(fill="x", padx=20, pady=5)

        tk.Button(btns, text="Добавить", command=self.add).pack(side="left", padx=5)
        tk.Button(btns, text="Обновить", command=self.update).pack(side="left", padx=5)
        tk.Button(btns, text="Удалить", command=self.delete).pack(side="left", padx=5)
        tk.Button(btns, text="Очистить", command=self.clear_form).pack(side="left", padx=5)

    def reload_refs(self):
        self.parcel_cb["values"] = get_column_values("Отправление", "ID_Отпр")
        ids = get_column_values("Отделение", "ID_Отделения")
        self.from_cb["values"] = ids
        self.to_cb["values"] = ids

    def load_data(self):
        self.reload_refs()
        for r in self.tree.get_children():
            self.tree.delete(r)
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT ID_Маршрута, ID_Отпр, Отделение_отправки,
                   Отделение_прибытия, Дата_отправки, Дата_прибытия
            FROM Маршрут
        """)
        for row in cur.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_select(self, _):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        self.selected_id = int(vals[0])
        self.parcel_var.set(str(vals[1]))
        self.from_var.set(str(vals[2]))
        self.to_var.set(str(vals[3]))
        self.d1_var.set(vals[4] or "")
        self.d2_var.set(vals[5] or "")

    def clear_form(self):
        self.selected_id = None
        self.parcel_var.set("")
        self.from_var.set("")
        self.to_var.set("")
        self.d1_var.set("")
        self.d2_var.set("")
        self.tree.selection_remove(self.tree.selection())

    def _validate(self):
        if not (self.parcel_var.get() and self.from_var.get() and self.to_var.get()):
            messagebox.showerror("Ошибка", "Выберите отправление и отделения")
            return False
        if self.d1_var.get() and not self.DATE_RE.fullmatch(self.d1_var.get()):
            messagebox.showerror("Ошибка", "Дата отправки в формате дд.мм.гггг")
            return False
        if self.d2_var.get() and not self.DATE_RE.fullmatch(self.d2_var.get()):
            messagebox.showerror("Ошибка", "Дата прибытия в формате дд.мм.гггг")
            return False
        return True

    def add(self):
        if not self._validate():
            return
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Маршрут
            (ID_Отпр, Отделение_отправки, Отделение_прибытия, Дата_отправки, Дата_прибытия)
            VALUES (?, ?, ?, ?, ?)
        """, (int(self.parcel_var.get()), int(self.from_var.get()),
              int(self.to_var.get()), self.d1_var.get(), self.d2_var.get()))
        conn.commit()
        conn.close()
        self.clear_form()
        self.load_data()

    def update(self):
        if self.selected_id is None:
            messagebox.showerror("Ошибка", "Выберите маршрут")
            return
        if not self._validate():
            return
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Маршрут
            SET ID_Отпр=?, Отделение_отправки=?, Отделение_прибытия=?,
                Дата_отправки=?, Дата_прибытия=?
            WHERE ID_Маршрута=?
        """, (int(self.parcel_var.get()), int(self.from_var.get()),
              int(self.to_var.get()), self.d1_var.get(), self.d2_var.get(), self.selected_id))
        conn.commit()
        conn.close()
        self.load_data()

    def delete(self):
        if self.selected_id is None:
            messagebox.showerror("Ошибка", "Выберите маршрут")
            return
        if not messagebox.askyesno("Подтверждение", "Удалить маршрут?"):
            return
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM Маршрут WHERE ID_Маршрута=?", (self.selected_id,))
        conn.commit()
        conn.close()
        self.clear_form()
        self.load_data()


class PostOfficeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("АИС Почта")
        self.geometry("1200x750")
        self.configure(bg="#000")

        self.sidebar = tk.Frame(self, bg="#111", width=220)
        self.sidebar.pack(side="left", fill="y")

        tk.Label(self.sidebar, text="📮 АИС Почта",
                 fg="white", bg="#111",
                 font=("San Francisco", 22, "bold")).pack(pady=25)

        self.container = tk.Frame(self, bg="#000")
        self.container.pack(side="right", expand=True, fill="both")

        self.pages = {}
        self.current_page = None

        self.add_menu("Клиенты", lambda: self.show_page("clients"))
        self.add_menu("Отделения", lambda: self.show_page("branches"))
        self.add_menu("Операторы", lambda: self.show_page("operators"))
        self.add_menu("Отправления", lambda: self.show_page("parcels"))
        self.add_menu("Платежи", lambda: self.show_page("payments"))
        self.add_menu("Маршруты", lambda: self.show_page("routes"))

        self.create_pages()
        self.show_page("clients")

    def add_menu(self, text, cmd):
        l = tk.Label(self.sidebar, text=text,
                     fg="white", bg="#111",
                     font=("San Francisco", 16), pady=10)
        l.pack(fill="x", padx=15, pady=3)
        l.bind("<Button-1>", lambda e: cmd())
        l.bind("<Enter>", lambda e: l.config(bg="#222"))
        l.bind("<Leave>", lambda e: l.config(bg="#111"))

    def create_pages(self):
        self.pages["clients"] = ClientPage(self.container)
        self.pages["branches"] = BranchPage(self.container)
        self.pages["operators"] = OperatorPage(self.container)
        self.pages["parcels"] = ParcelPage(self.container)
        self.pages["payments"] = PaymentPage(self.container)
        self.pages["routes"] = RoutePage(self.container)

    def show_page(self, name):
        if self.current_page:
            self.current_page.pack_forget()
        page = self.pages[name]
        page.pack(fill="both", expand=True)
        self.current_page = page


if __name__ == "__main__":
    PostOfficeApp().mainloop()
