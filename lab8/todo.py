import flet as ft
from datetime import datetime
import uuid

# Кастомные исключения
class TaskError(Exception):
    """Базовое исключение для ошибок, связанных с задачами"""
    pass

class EmptyTaskError(TaskError):
    """Вызывается, если описание задачи пустое"""
    pass

class Task:
    """Класс, представляющий одну задачу"""
    def __init__(self, description: str, priority: str = "Low", due_date: datetime = None):
        if not description.strip():
            raise EmptyTaskError("Описание задачи не может быть пустым")
        self._id = str(uuid.uuid4())
        self._description = description.strip()
        self._priority = priority
        self._due_date = due_date
        self._completed = False

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        if not value.strip():
            raise EmptyTaskError("Описание задачи не может быть пустым")
        self._description = value.strip()

    @property
    def priority(self) -> str:
        return self._priority

    @priority.setter
    def priority(self, value: str):
        if value not in ["Low", "Medium", "High"]:
            raise TaskError("Приоритет должен быть Low, Medium или High")
        self._priority = value

    @property
    def due_date(self) -> datetime:
        return self._due_date

    @due_date.setter
    def due_date(self, value: datetime):
        self._due_date = value

    @property
    def completed(self) -> bool:
        return self._completed

    def toggle_complete(self):
        self._completed = not self._completed

    def __str__(self) -> str:
        status = "✓" if self._completed else " "
        due_date_str = self._due_date.strftime("%d-%m-%Y %H:%M") if self._due_date else "Нет срока"
        return f"[{status}] {self._description} (Приоритет: {self._priority}, Срок: {due_date_str})"

    def __repr__(self) -> str:
        return f"Task(id={self._id}, description={self._description}, priority={self._priority}, due_date={self._due_date}, completed={self._completed})"

class ToDoApp:
    """Основной класс приложения для управления задачами"""
    def __init__(self, page: ft.Page):
        self.page = page
        self.tasks = []
        self.setup_ui()

    def setup_ui(self):
        """Настройка основных компонентов интерфейса"""
        self.page.title = "Система учета задач (ToDo)"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 20
        self.page.window_width = 600
        self.page.window_height = 800

        # Поля ввода
        self.task_input = ft.TextField(
            label="Описание задачи",
            width=400,
            on_submit=self.add_task
        )
        self.priority_dropdown = ft.Dropdown(
            label="Приоритет",
            width=150,
            options=[
                ft.dropdown.Option("Low"),
                ft.dropdown.Option("Medium"),
                ft.dropdown.Option("High")
            ],
            value="Low"
        )
        self.due_date_picker = ft.TextField(
            label="Срок выполнения (дд-мм-гггг чч:мм)",
            width=400,
            hint_text="Например, 14-07-2025 14:30"
        )

        # Кнопки
        self.add_button = ft.ElevatedButton(
            text="Добавить задачу",
            on_click=self.add_task
        )

        # Список задач
        self.task_list = ft.ListView(expand=True, spacing=10, padding=10)

        # Макет
        self.page.add(
            ft.Row([
                self.task_input,
                self.priority_dropdown
            ]),
            ft.Row([
                self.due_date_picker
            ]),
            ft.Row([
                self.add_button,
                ft.ElevatedButton("Очистить завершенные", on_click=self.clear_completed)
            ]),
            self.task_list
        )

    def add_task(self, e):
        """Добавление новой задачи в список"""
        try:
            due_date = None
            if self.due_date_picker.value.strip():
                try:
                    due_date = datetime.strptime(
                        self.due_date_picker.value.strip(),
                        "%d-%m-%Y %H:%M"
                    )
                except ValueError:
                    raise TaskError("Неверный формат даты. Используйте дд-мм-гггг чч:мм")

            task = Task(
                description=self.task_input.value,
                priority=self.priority_dropdown.value,
                due_date=due_date
            )
            self.tasks.append(task)
            self.task_input.value = ""
            self.due_date_picker.value = ""
            self.update_task_list()
        except EmptyTaskError as err:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(str(err)),
            )
            self.page.snack_bar.open = True
        except TaskError as err:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(str(err)),
            )
            self.page.snack_bar.open = True
        self.page.update()

    def clear_completed(self, e):
        """Удаление всех завершенных задач"""
        self.tasks = [task for task in self.tasks if not task.completed]
        self.update_task_list()
        self.page.update()

    def update_task_list(self):
        """Обновление отображения списка задач"""
        self.task_list.controls.clear()
        for task in self.tasks:
            task_row = ft.Row([
                ft.Checkbox(
                    value=task.completed,
                    on_change=lambda e, t=task: self.toggle_task_completion(t)
                ),
                ft.Text(str(task), expand=True),
                ft.ElevatedButton(
                    text="Удалить",
                    on_click=lambda e, t=task: self.delete_task(t)
                )
            ])
            self.task_list.controls.append(task_row)

    def toggle_task_completion(self, task: Task):
        """Переключение статуса завершения задачи"""
        task.toggle_complete()
        self.update_task_list()
        self.page.update()

    def delete_task(self, task: Task):
        """Удаление конкретной задачи"""
        self.tasks.remove(task)
        self.update_task_list()
        self.page.update()

def main(page: ft.Page):
    app = ToDoApp(page)

if __name__ == "__main__":
    ft.app(target=main)
