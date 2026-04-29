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
...
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

...

---

## WordPress Suite

### Тест-кейс №01. Создание поста

- **Предусловие**:
  1. Авторизоваться (`Firstname.Lastname:123-Test`)

- **Шаги**:
  1. Отправить POST-запрос:
     * На `http://localhost:8000/index.php?rest_route=/wp/v2/posts`
     * В теле запроса передать: `{"title": "TestPost1", "status": "draft", "content": "Test content"}`
  2. Зафиксировать `id` из ответа

- **Ожидаемый результат**: 
  1. Код ответа `201 Created`
  2. Тело ответа содержит переданные параметры
  3. Запрос `SELECT post_title, post_content FROM wp_posts WHERE ID = {id}` находит строку с `post_title = TestPost1`

- **Постусловие**: 
  1. Удалить созданный пост: `DELETE FROM wp_posts WHERE ID = {id}`

- **Тестовые данные**:
  1. Basic Auth `USERNAME:PASSWORD` — `Firstname.Lastname:123-Test`
  2. `title` — `TestPost1`
  3. `status` — `draft`
  4. `content` — `Test content`

### Тест-кейс №02. Обновление поста

- **Предусловие**:
  1. Авторизоваться (`Firstname.Lastname:123-Test`)
  2. Создать тестовый пост: `INSERT INTO wp_posts (post_title, post_content, post_status) VALUES 
  ('Original Title', 'Original Content', 'publish')`
  3. Зафиксировать `id` поста

- **Шаги**:
  1. Отправить POST-запрос:
     * На `http://localhost:8000/index.php?rest_route=/wp/v2/posts/{id}`
     * В теле запроса передать: `{"title": "Updated Title", "content": "Updated Content"}`

- **Ожидаемый результат**:
  1. Код ответа `200 OK`
  2. Тело ответа содержит переданные параметры
  3. Запрос `SELECT post_title, post_content FROM wp_posts WHERE ID = {id}` находит строку с 
  `post_title = Updated Title`

- **Постусловие**: 
  1. Удалить созданный пост: `DELETE FROM wp_posts WHERE ID = {id}`

- **Тестовые данные**:
  1. Basic Auth `USERNAME:PASSWORD` — `Firstname.Lastname:123-Test`
  2. `title` — `Updated Title`
  3. `content` — `Updated Content`

### Тест-кейс №03. Удаление поста

- **Предусловие**:
  1. Авторизоваться (`Firstname.Lastname:123-Test`)
  2. Создать тестовый пост: `INSERT INTO wp_posts (post_title, post_content, post_status) VALUES 
  ('Test Post 2', 'Test Content 2', 'publish')`
  3. Зафиксировать `id` поста

- **Шаги**:
  1. Отправить DELETE-запрос:
     * На `http://localhost:8000/index.php?rest_route=/wp/v2/posts/{id}?force=true`

- **Ожидаемый результат**: 
  1. Код ответа `200 OK`
  2. Запрос `SELECT COUNT(*) FROM wp_posts WHERE ID = {id}` возвращает `0`

- **Тестовые данные**:
  1. Basic Auth `USERNAME:PASSWORD` — `Firstname.Lastname:123-Test`
  2. `force` — `True`

### Тест-кейс №04. Создание поста без title

- **Предусловие**:
  1. Авторизоваться (`Firstname.Lastname:123-Test`)

- **Шаги**:
  1. Отправить POST-запрос:
     * На `http://localhost:8000/index.php?rest_route=/wp/v2/posts`
     * В теле запроса передать: `{"status": "draft", "content": "No Title"}`

- **Ожидаемый результат**: 
  1. Код ответа `400 Bad Request`
  2. Тело ответа содержит `error` или `message`
  3. Запрос `SELECT COUNT(*) FROM wp_posts WHERE post_title IS NULL` возвращает `0`

- **Тестовые данные**:
  1. Basic Auth `USERNAME:PASSWORD` — `Firstname.Lastname:123-Test`
  2. `status` — `draft`
  3. `content` — `No Title`

### Тест-кейс №05. Обновление несуществующего поста

- **Предусловие**:
  1. Авторизоваться (`Firstname.Lastname:123-Test`)

- **Шаги**:
  1. Отправить POST-запрос:
     * На `http://localhost:8000/index.php?rest_route=/wp/v2/posts/9999`
     * В теле запроса передать: `{"title": "New Title"}`

- **Ожидаемый результат**:
  1. Код ответа `404 Not Found`
  2. Тело ответа содержит `error` или `message`
  3. Запрос `SELECT COUNT(*) FROM wp_posts WHERE ID = 9999` возвращает `0`

- **Тестовые данные**:
  1. Basic Auth `USERNAME:PASSWORD` — `Firstname.Lastname:123-Test`
  2. `title` — `New Title`

### Тест-кейс №06. Удаление несуществующего поста

- **Предусловие**:
  1. Авторизоваться (`Firstname.Lastname:123-Test`)

- **Шаги**:
  1. Отправить DELETE-запрос:
     * На `http://localhost:8000/index.php?rest_route=/wp/v2/posts/9999?force=true`

- **Ожидаемый результат**: 
  1. Код ответа `404 Not Found`
  2. Тело ответа содержит `error` или `message`
  3. Запрос `SELECT COUNT(*) FROM wp_posts WHERE ID = 9999` возвращает `0`

- **Тестовые данные**:
  1. Basic Auth `USERNAME:PASSWORD` — `Firstname.Lastname:123-Test`
  2. `force` — `True`
