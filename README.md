# Дашборд по анализу уровня безработицы по странам мира

Добро пожаловать на дашборд, предоставляющий всесторонний анализ данных по безработице в различных странах мира за период с 1991 по 2020 годы. Этот проект использует Dash и Plotly для создания интерактивных визуализаций и анализа данных.

### Возможности дашборда:

- **Карта мира по безработице:** Визуализация уровня безработицы по странам и континентам за выбранный год.
- **Линейная диаграмма по динамике безработицы:** Отображение изменений уровня безработицы в различных странах за выбранный временной промежуток.
- **Тепловая карта по уровню безработицы:** Визуальное представление уровня безработицы по странам за выбранный период.
- **Изменение уровня безработицы по годам:** Столбчатая диаграмма, отображающая изменения уровня безработицы в различных странах с течением времени.
- **Топ 10 стран по безработице:** Сортировка и отображение десяти стран с самым высоким уровнем безработицы за выбранный год.
- **Столбчатые диаграммы по отклонению уровня безработицы:** Визуализация отклонения уровня безработицы и изменений в различных странах и по годам.

### Установка

Для установки приложения выполните следующие шаги:

1. **Клонирование репозитория:**
   ```bash
   git clone https://github.com/Dk-jvr/Unemployment-analysis.git
   cd Unemployment-analysis
   ```

2. **Настройка виртуального окружения:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Для Windows: venv\Scripts\activate
   ```

3. **Установка зависимостей:**
   ```bash
   pip install dash-bootstrap-components
   ```

### Запуск приложения

После установки зависимостей запустите приложение командой:
```bash
python app.py
```

Откройте веб-браузер и перейдите по адресу [http://127.0.0.1:8050/](http://127.0.0.1:8050/) для просмотра дашборда.

### Данные

Датасет содержит данные об уровне безработицы в различных странах мира с 1991 по 2020 годы. Каждый год представлен в отдельной колонке, содержащей значения уровня безработицы для каждой страны.

### Авторы

Проект подготовили студенты 3 курса РТУ МИРЭА:

- [Кива Д.С.](https://github.com/Dk-jvr) (БСБО-14-21)
- [Годин И.А](https://github.com/CyberN00b) (БСБО-14-21)
