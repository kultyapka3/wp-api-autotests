## Тесты

Этот репозиторий содержит проект автотестов для WordPress REST API с проверкой данных в БД

---

## Технологии

*   **Язык программирования:** Python 3.10+
*   **Тестовый фреймворк:** pytest
*   **Сборка зависимостей:** pip (файл `requirements.txt`)
*   **API:** requests

---

## Структура проекта

```
project_root/
├── README.md                                        # Этот файл
├── .gitignore                                       # Файл управления Git
├── requirements.txt                                 # Список зависимостей Python
├── pytest.ini                                       # Конфигурация pytest
└── conftest.py                                      # Фикстуры pytest
```

---

## Установка и запуск

### Клонирование репозитория

1. Сначала клонируйте репозиторий:
   ```bash
   git clone https://github.com/kultyapka3/wp-api-autotests.git
   ```
   
2. Перейдите в нужную директорию:
   ```bash
   cd wp-api-autotests
   ```

### Виртуальное окружение

1.  Создайте виртуальное окружение:
    ```bash
    python -m venv venv
    ```
    
2.  Активируйте его:
    *   **Windows:**
        ```bash
        venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

### Установка зависимостей

После активации виртуального окружения установите зависимости из файла `requirements.txt`:

```bash
  pip install -r requirements.txt
```

---

## Запуск тестов