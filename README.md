# Дашборд по анализу уровня безработицы по странам мира

### Это многостраничный дашборд для анализа данных по безработице за 1991-2020 годы <!-- описание репозитория -->


Ознакомиться с самим датасетом по проценту безработицы можно по [ссылке](https://www.kaggle.com/datasets/pantanjali/unemployment-dataset).
Ознакомиться с датасетом с населенением по странам можно по [ссылке](https://gist.github.com/ngchengpiaw/27f7ac9129ed715d8dedcd55e30e3b7a)

## О проекте

Этот дашборд предоставляет всесторонний анализ данных по безработице, охватывающих период с 1991 по 2020 годы. Вы можете исследовать различные аспекты уровня безработицы через интерактивные диаграммы и визуализации, включая:
- Карта мира по безработице: Позволяет визуализировать уровень безработицы по странам и континентам за выбранный год. Это дает возможность быстро оценить глобальное распределение безработицы и выявить региональные тенденции.
- Линейная диаграмма по динамике безработицы: Демонстрирует изменения уровня безработицы в разных странах за выбранный временной промежуток. Эта диаграмма помогает отслеживать тенденции и сравнивать динамику безработицы между странами.
- Тепловая карта по уровню безработицы: Визуализирует уровень безработицы по странам за выбранный период. Темные оттенки указывают на более высокий уровень безработицы, позволяя легко выявлять проблемные области.
- Изменение уровня безработицы по годам: Представляет собой столбчатую диаграмму, показывающую изменения уровня безработицы в различных странах по годам. Это полезно для анализа ежегодных изменений и оценки эффективности экономических политик.
- Топ 10 стран по безработице: Сортирует страны по уровню безработицы и отображает десять стран с самым высоким уровнем за выбранный год. Это помогает выявить наиболее пострадавшие от безработицы страны.
- Столбчатые диаграммы по отклонению уровня безработицы: Эти диаграммы показывают отклонение уровня безработицы в странах и изменения уровня безработицы по годам. Это позволяет более детально анализировать изменения и выявлять тренды.

Датасет содержит данные об уровне безработицы по странам мира с 1991 по 2020 годы. Каждый год представлен отдельной колонкой, где указаны значения уровня безработицы для каждой страны. Данные позволяют проводить глубокий анализ и выявлять как долгосрочные, так и краткосрочные тренды в уровне безработицы.
## Оглавление
- [Немножко про код](#немножко-про-код)
- [Структура проекта](#структура-проекта)
- [Использование](#использование)
- [Установка](#установка)
- [Итог](#итог)
- [Авторы](#автор)

## Немножко про код
В процессе создания многостраничного дашборда использовались:

- **Bootstrap** - это один из наиболее популярных фреймворков для создания пользовательских интерфейсов веб-приложений, который облегчает создание стильных и отзывчивых веб-страниц.
- **Фреймворк Dash**: это инструмент для создания интерактивных веб-приложений с использованием языка программирования Python. Он предоставляет возможности для быстрой разработки данных и аналитики на основе веб-технологий, таких как HTML, CSS и JavaScript.
```sh
    pip install dash
```
- **Dash Bootstrap Components (dash_bootstrap_components)**: это библиотека для фреймворка Dash, которая предоставляет компоненты пользовательского интерфейса, стилизованные в соответствии с Bootstrap.
```sh
    pip install dash-bootstrap-components
```
- **Plotly Express (px)**: высокоуровневый интерфейс для построения интерактивных графиков и визуализаций данных с использованием библиотеки Plotly. Упрощает создание сложных графиков с минимальным кодом.
```sh
    pip install plotly
```
- **Pandas (pd)**: библиотека для работы с данными, предоставляющая структуры данных и операции для манипуляций с таблицами. Используется для загрузки, обработки и анализа данных.
```sh
    pip install pandas
```
- **Plotly Graph Objects (go)**: низкоуровневый интерфейс для построения графиков и визуализаций с помощью Plotly. Предоставляет полный контроль над стилями и атрибутами графиков.

## Структура проекта

```plaintext
├── app.py                 # Главный файл приложения, содержащий настройки и маршрутизацию
├── data.py                # Файл загрузки данных датасета
└── pages/                 # Директория с файлами страниц
    ├── bar_charts.py      # Страница с топ-10 графиками и отклонениям по континентам
    ├── worldmap.py        # Страница с картой
    └── charts.py          # Страница с графиками для сравнения стран
```
## Использование

Приложение состоит из нескольких страниц:

- **Главная**: Основная информация о проекте.
- **Карта безработицы**: Позволяет пользователям смотреть информацию о уровне безработицы на карте мира.
- **Динамика беработицы**: Отображает различия между странами по безработицы.
- **Отклонения по континентам**: Предоставляет информацию об отклонении уровня безработицы относительно континента.

Для навигации используйте боковую панель меню, как раз таки содержащую эти страницы.

## Установка

1. Склонируйте репозиторий:
    ```sh
    git clone https://github.com/Dk-jvr/Unemployment-analysis.git
    ```
2. Перейдите в директорию проекта:
    ```sh
    cd project
    ```
3. Создайте виртуальное окружение и активируйте его:
    ```sh
    python -m venv venv
    source venv/bin/activate
    ```
4. Установите необходимые зависимости:
    ```sh
    pip install dash-bootstrap-components
    ```
5. Запуск приложения
После установки всех зависимостей, вы можете запустить приложение командой:
    ```sh
    python3 app.py
    ```
## Итог
Полученный многостраничный дашборд был размещен в интернете для публичного доступа с помощью ресурса [PythonAnywhere](https://www.pythonanywhere.com).

Ознакомиться с исходным кодом можно по [ссылке](https://github.com/Dk-jvr/Unemployment-analysis).
Ознакомиться с самим дашбордом можно по [ссылке](https://cybern00b.pythonanywhere.com/)

## Авторы
Проект подготовили студенты 3 курса РТУ МИРЭА в 2024 году:
- [Годин И.А.](https://github.com/CyberN00b) (БСБО-14-21)
- [Кива Д.С.](https://github.com/Dk-jvr) (БСБО-14-21)

Если у вас возникли вопросы или предложения, пожалуйста, свяжитесь с авторами.
