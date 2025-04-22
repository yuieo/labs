import tkinter as tk
from tkinter import simpledialog, messagebox
from geometry_package import Rectangle, Triangle, Trapezoid
from docx import Document


class SimpleGeometryCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("фигурки")
        self.root.geometry("600x300")

        # Кнопки выбора фигуры
        tk.Button(root, text="Прямоугольник", command=lambda: self.calculate_shape("Прямоугольник")).pack(pady=5)
        tk.Button(root, text="Треугольник", command=lambda: self.calculate_shape("Треугольник")).pack(pady=5)
        tk.Button(root, text="Трапеция", command=lambda: self.calculate_shape("Трапеция")).pack(pady=5)

        # Поле для вывода результатов
        self.result_label = tk.Label(root, text="", justify="left")
        self.result_label.pack(pady=10)

        # Кнопка сохранения
        tk.Button(root, text="Сохранить в DOCX", command=self.save_to_docx).pack(pady=5)

        self.last_result = ""

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

            self.last_result = f"{shape}\nПлощадь: {area:.2f}\n"
            self.last_result += f"Описанная окружность: {circumradius}\n"
            self.last_result += f"Вписанная окружность: {inradius}"

            self.result_label.config(text=self.last_result)

        except ValueError:
            messagebox.showerror("Ошибка", "Введите числа!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка расчёта: {e}")

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