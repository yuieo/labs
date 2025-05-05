# Лабораторная работа №6 / 1 вариант
## Задача
Геометрические фигуры:
    * Прямоугольник
    * Треугольник
    * Трапеция
Расчёт площади, радусов описанной и вписанной окружности.


## Описание 
1. Основная функция:
Программа рассчитывает параметры геометрических фигур (прямоугольник, треугольник, трапеция):
    * Площадь
    * Радиус описанной окружности
    * Радиус вписанной окружности

2. Как работает:
    * Пользователь выбирает фигуру через кнопки
    * Вводит параметры фигуры (стороны) в диалоговых окнах
    * Программа вычисляет и показывает результаты
    * По команде результат сохраняется в файл "результат.docx"

3. Технические детали:

Используется 3 модуля с формулами расчета (rectangle.py, triangle.py, trapezoid.py)
Интерфейс сделан на Tkinter
Для работы нужен Python 3.x и библиотеки:
``` python
pip install tk python-docx
```

## Работа программы

![изображение](https://github.com/user-attachments/assets/cca48360-8023-4e55-a869-04853eda98c5)

![изображение](https://github.com/user-attachments/assets/0ce1e420-1ae7-4cdf-b9c1-d6960192388e)

![изображение](https://github.com/user-attachments/assets/7534315b-94bc-46d4-b09f-6ee43db4afde)

![изображение](https://github.com/user-attachments/assets/22c0adc3-58b8-4183-82da-6943bd88e096)





# Medium 
1. Устанавливаем Docker
2. Создаем контейнер с именем my-postgres
    Устанавливаем пароль mysecretpassword для пользователя postgres
    Открываем порт 5432 для подключения
    Используем последнюю версию PostgreSQL
   
``` docker
docker run --name my-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
```

3. Подключаем к контейнеру:

   ``` docker
   docker exec -it my-postgres psql -U postgres
   ```

4. В консоли PostgreSQL создаем базу данных и таблицу

   ```
   CREATE DATABASE geometry_db;
   \c geometry_db

   CREATE TABLE calculations (
       id SERIAL PRIMARY KEY,
       shape_type VARCHAR(50) NOT NULL,
       area FLOAT NOT NULL,
       circumradius VARCHAR(100) NOT NULL,
       inradius VARCHAR(100) NOT NULL,
       calculation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

5. Скачиваем необходимую библиотеку

   ```
   pip install psycopg2-binary
   ```

6. В main.py:
   * Добавлен метод connect_db() для подключения к базе данных
   * Используется библиотека psycopg2 для работы с PostgreSQL
   * В методе calculate_shape() добавлен вызов save_to_db()
   * Добавлена кнопка "Показать историю" для просмотра последних 10 записей
   * Метод show_history() получает данные из БД и отображает их
  
## Работа программы

![изображение](https://github.com/user-attachments/assets/9b82c3e8-31cf-4887-81ed-4aab396f9f0d)

![изображение](https://github.com/user-attachments/assets/8aa4b586-f1d1-418b-a943-3c8d87b4a661)


## Список используемой информации
1. [Руководство по Tkinter](https://metanit.com/python/tkinter/)
2. [tkinter — Python interface to Tcl/Tk](https://docs.python.org/3/library/tkinter.html)
