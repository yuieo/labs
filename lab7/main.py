from appJar import gui
from shapes import Rectangle, Triangle, Trapezoid
from docx import Document


class SimpleGeometryCalculator:
    def __init__(self):
        self.app = gui("Фигуры", "400x300")

        self.app.addButton("Прямоугольник", lambda: self.calculate("Прямоугольник"))
        self.app.addButton("Треугольник", lambda: self.calculate("Треугольник"))
        self.app.addButton("Трапеция", lambda: self.calculate("Трапеция"))

        self.result = self.app.addLabel("result", "")
        self.app.setLabelAlign("result", "left")

        self.app.addButton("Сохранить", self.save)

        self.last_result = None

    def calculate(self, shape_type):
        try:
            if shape_type == "Прямоугольник":
                a = float(self.app.textBox("Ввод", "Сторона a:"))
                b = float(self.app.textBox("Ввод", "Сторона b:"))
                shape = Rectangle(a, b)
            elif shape_type == "Треугольник":
                a = float(self.app.textBox("Ввод", "Сторона a:"))
                b = float(self.app.textBox("Ввод", "Сторона b:"))
                c = float(self.app.textBox("Ввод", "Сторона c:"))
                shape = Triangle(a, b, c)
            elif shape_type == "Трапеция":
                a = float(self.app.textBox("Ввод", "Основание a:"))
                b = float(self.app.textBox("Ввод", "Основание b:"))
                c = float(self.app.textBox("Ввод", "Боковая сторона c:"))
                d = float(self.app.textBox("Ввод", "Боковая сторона d:"))
                shape = Trapezoid(a, b, c, d)

            result_text = f"{shape}\nПлощадь: {shape.area():.2f}\n"
            result_text += f"Радиус описанной окружности: {shape.circumradius()}\n"
            result_text += f"Радиус вписанной окружности: {shape.inradius()}"

            self.app.setLabel("result", result_text)
            self.last_result = result_text

        except ValueError:
            self.app.errorBox("Ошибка", "Некорректный ввод!")
        except Exception as e:
            self.app.errorBox("Ошибка", f"Ошибка: {str(e)}")

    def save(self):
        if not self.last_result:
            self.app.errorBox("Ошибка", "Нет данных для сохранения")
            return

        doc = Document()
        doc.add_paragraph(self.last_result)
        doc.save("result.docx")
        self.app.infoBox("Успех", "Сохранено в result.docx")


if __name__ == "__main__":
    app = SimpleGeometryCalculator()
    app.app.go()
