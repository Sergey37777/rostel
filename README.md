# Установка проекта


## Технические детали

- Язык: Python 3.12
- Парадигма: Объектно-ориентированное программирование (ООП)
- Инструменты парсинга: Selenium WebDriver (Chrome)
- Выгрузка данных: Pandas (Excel)
- Виртуальное окружение: [Poetry](https://python-poetry.org/)
- Скрипт предназначен для запуска на Windows/MacOS/Linux

## Шаги установки

### 1. Клонирование репозитория с GitHub

Откройте терминал и выполните следующие команды:

```bash
git clone https://github.com/Sergey37777/.git
cd your-repo-name
```

### 2. Установка зависимостей

```bash
poetry install
```


### 3. Активация виртуального окружения

```bash
poetry shell
```


### 4. Установка chromedriver

Скачайте Stable версию [chromedriver](https://googlechromelabs.github.io/chrome-for-testing/) и поместите его в корне проекта.
Убедитесь, что версия chromedriver совпадает с версией вашего браузера.


### 5. Запуск скрипта

```bash
poetry run python main.py
```
