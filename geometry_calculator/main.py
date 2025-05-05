import tkinter as tk
from tkinter import simpledialog, messagebox
from geometry_package import Rectangle, Triangle, Trapezoid
from docx import Document
import psycopg2
from datetime import datetime


class SimpleGeometryCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("фигурки")
        self.root.geometry("600x300")

        # выбор фигур
        tk.Button(root, text="Прямоугольник", command=lambda: self.calculate_shape("Прямоугольник")).pack(pady=5)
        tk.Button(root, text="Треугольник", command=lambda: self.calculate_shape("Треугольник")).pack(pady=5)
        tk.Button(root, text="Трапеция", command=lambda: self.calculate_shape("Трапеция")).pack(pady=5)

        # вывод результатов
        self.result_label = tk.Label(root, text="", justify="left")
        self.result_label.pack(pady=10)

        # сохранение
        tk.Button(root, text="Сохранить в DOCX", command=self.save_to_docx).pack(pady=5)
        tk.Button(root, text="Показать историю", command=self.show_history).pack(pady=5)

        self.last_result = ""
        self.last_shape = ""
        self.last_area = 0
        self.last_circumradius = ""
        self.last_inradius = ""

    def connect_db(self):
        try:
            return psycopg2.connect(
                host="localhost",
                database="geometry_db",
                user="postgres",
                password="mysecretpassword"
            )
        except Exception as e:
            messagebox.showerror("Ошибка БД", f"Не удалось подключиться к БД: {e}")
            return None

    def calculate_shape(self, shape):
        try:
            if shape == "Прямоугольник":
                a = float(simpledialog.askstring("Ввод", "Сторона a:"))
                b = float(simpledialog.askstring("Ввод", "Сторона b:"))
                area = Rectangle.area(a, b)
                circumradius = Rectangle.circumradius(a, b)
                inradius = Rectangle.inradius(a, b)
            elif shape == "Треугольник":
                a = float(simpledialog.askstring("Ввод", "Сторона a:"))
                b = float(simpledialog.askstring("Ввод", "Сторона b:"))
                c = float(simpledialog.askstring("Ввод", "Сторона c:"))
                area = Triangle.area(a, b, c)
                circumradius = Triangle.circumradius(a, b, c)
                inradius = Triangle.inradius(a, b, c)
            elif shape == "Трапеция":
                a = float(simpledialog.askstring("Ввод", "Основание a:"))
                b = float(simpledialog.askstring("Ввод", "Основание b:"))
                c = float(simpledialog.askstring("Ввод", "Боковая сторона c:"))
                d = float(simpledialog.askstring("Ввод", "Боковая сторона d:"))
                area = Trapezoid.area(a, b, c, d)
                circumradius = Trapezoid.circumradius(a, b, c, d)
                inradius = Trapezoid.inradius(a, b, c, d)

            self.last_shape = shape
            self.last_area = area
            self.last_circumradius = str(circumradius)
            self.last_inradius = str(inradius)

            self.last_result = f"{shape}\nПлощадь: {area:.2f}\n"
            self.last_result += f"Описанная окружность: {circumradius}\n"
            self.last_result += f"Вписанная окружность: {inradius}"

            self.result_label.config(text=self.last_result)

            # Сохраняем в БД
            self.save_to_db()

        except ValueError:
            messagebox.showerror("Ошибка", "Введите числа!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка расчёта: {e}")

    def save_to_db(self):
        conn = self.connect_db()
        if conn is None:
            return

        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO calculations (shape_type, area, circumradius, inradius) VALUES (%s, %s, %s, %s)",
                    (self.last_shape, self.last_area, self.last_circumradius, self.last_inradius)
                )
                conn.commit()
        except Exception as e:
            messagebox.showerror("Ошибка БД", f"Не удалось сохранить в БД: {e}")
        finally:
            conn.close()

    def show_history(self):
        conn = self.connect_db()
        if conn is None:
            return

        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM calculations ORDER BY calculation_time DESC LIMIT 10")
                records = cur.fetchall()

                history_text = "Последние 10 записей:\n\n"
                for record in records:
                    history_text += f"Фигура: {record[1]}\n"
                    history_text += f"Площадь: {record[2]:.2f}\n"
                    history_text += f"Опис. окр.: {record[3]}\n"
                    history_text += f"Впис. окр.: {record[4]}\n"
                    history_text += f"Дата: {record[5]}\n\n"

                messagebox.showinfo("История расчетов", history_text)
        except Exception as e:
            messagebox.showerror("Ошибка БД", f"Не удалось загрузить историю: {e}")
        finally:
            conn.close()

    def save_to_docx(self):
        if not self.last_result:
            messagebox.showerror("Ошибка", "Сначала выполните расчёт")
            return

        doc = Document()
        doc.add_paragraph(self.last_result)
        doc.save("результат.docx")
        messagebox.showinfo("Сохранено", "Результаты сохранены в файл 'результат.docx'")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleGeometryCalculator(root)
    root.mainloop()
