import tkinter as tk
from tkinter import simpledialog, messagebox
from geometry_package.shapes import Rectangle, Triangle, Trapezoid
from docx import Document


class SimpleGeometryCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Фигуры")
        self.root.geometry("400x300")

        tk.Button(root, text="Прямоугольник", command=lambda: self.calculate("Прямоугольник")).pack(pady=5)
        tk.Button(root, text="Треугольник", command=lambda: self.calculate("Треугольник")).pack(pady=5)
        tk.Button(root, text="Трапеция", command=lambda: self.calculate("Трапеция")).pack(pady=5)

        self.result = tk.Label(root, text="", justify="left")
        self.result.pack(pady=20)

        tk.Button(root, text="Сохранить", command=self.save).pack(pady=5)

    def calculate(self, shape_type):
        try:
            if shape_type == "Прямоугольник":
                a = float(simpledialog.askstring("Ввод", "Сторона a:"))
                b = float(simpledialog.askstring("Ввод", "Сторона b:"))
                shape = Rectangle(a, b)
            elif shape_type == "Треугольник":
                a = float(simpledialog.askstring("Ввод", "Сторона a:"))
                b = float(simpledialog.askstring("Ввод", "Сторона b:"))
                c = float(simpledialog.askstring("Ввод", "Сторона c:"))
                shape = Triangle(a, b, c)
            elif shape_type == "Трапеция":
                a = float(simpledialog.askstring("Ввод", "Основание a:"))
                b = float(simpledialog.askstring("Ввод", "Основание b:"))
                c = float(simpledialog.askstring("Ввод", "Боковая сторона c:"))
                d = float(simpledialog.askstring("Ввод", "Боковая сторона d:"))
                shape = Trapezoid(a, b, c, d)

            result_text = f"{shape}\nПлощадь: {shape.area():.2f}\n"
            result_text += f"Радиус описанной окружности: {shape.circumradius()}\n"
            result_text += f"Радиус вписанной окружности: {shape.inradius()}"

            self.result.config(text=result_text)
            self.last_result = result_text

        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный ввод!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")

    def save(self):
        if not hasattr(self, 'last_result'):
            messagebox.showerror("Ошибка", "Нет данных для сохранения")
            return

        doc = Document()
        doc.add_paragraph(self.last_result)
        doc.save("result.docx")
        messagebox.showinfo("Успех", "Сохранено в result.docx")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleGeometryCalculator(root)
    root.mainloop()
  
