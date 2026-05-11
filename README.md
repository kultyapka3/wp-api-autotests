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

# WordPress Suite

## D1 Тест-кейсы

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
  1. Удалить созданный пост: `DELETE FROM wp_posts WHERE ID = {id} OR post_parent = %s`

- **Тестовые данные**:
  1. Basic Auth `USERNAME:PASSWORD` — `Firstname.Lastname:123-Test`
  2. `title` — `TestPost1`
  3. `status` — `draft`
  4. `content` — `Test content`

### Тест-кейс №02. Обновление поста

- **Предусловие**:
  1. Авторизоваться (`Firstname.Lastname:123-Test`)
  2. Создать тестовый пост: `INSERT INTO wp_posts (post_title, post_content, post_status) VALUES 
  ('Test Title', 'Test Content', 'publish')`
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
  1. Удалить созданный пост: `DELETE FROM wp_posts WHERE ID = {id} OR post_parent = {id}`

- **Тестовые данные**:
  1. Basic Auth `USERNAME:PASSWORD` — `Firstname.Lastname:123-Test`
  2. `title` — `Updated Title`
  3. `content` — `Updated Content`

### Тест-кейс №03. Удаление поста

- **Предусловие**:
  1. Авторизоваться (`Firstname.Lastname:123-Test`)
  2. Создать тестовый пост: `INSERT INTO wp_posts (post_title, post_content, post_status) VALUES 
  ('Test Title', 'Test Content', 'publish')`
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
  1. Код ответа `201 Created`
  2. Тело ответа содержит переданные параметры
  3. Запрос `SELECT post_title, post_content FROM wp_posts WHERE ID = {id}` находит строку с пустым `post_title`

- **Постусловие**: 
  1. Удалить созданный пост: `DELETE FROM wp_posts WHERE ID = {id} OR post_parent = %s`

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

## D2 Тест-кейсы

### Тест-кейс №07. Получение существующего поста по ID

- **Предусловие**:
  1. Авторизоваться (`Firstname.Lastname:123-Test`)
  2. Создать тестовый пост: `INSERT INTO wp_posts (post_title, post_content, post_status) VALUES 
  ('Test Title', 'Test Content', 'publish')`
  3. Зафиксировать `id` поста

- **Шаги**:
  1. Отправить GET-запрос:
     * На `http://localhost:8000/index.php?rest_route=/wp/v2/posts/{id}`

- **Ожидаемый результат**:
  1. Код ответа `200 OK`
  2. Тело ответа содержит зафиксированный `id`
  3. Запрос `SELECT post_title, post_content FROM wp_posts WHERE ID = {id}` находит строку с 
  `post_title = Test Title`

- **Постусловие**: 
  1. Удалить созданный пост: `DELETE FROM wp_posts WHERE ID = {id} OR post_parent = {id}`

- **Тестовые данные**:
  1. Basic Auth `USERNAME:PASSWORD` — `Firstname.Lastname:123-Test`

### Тест-кейс №08. Получение списка постов с фильтрацией по статусу

- **Предусловие**:
  1. Авторизоваться (`Firstname.Lastname:123-Test`)
  2. Создать первый тестовый пост: `INSERT INTO wp_posts (post_title, post_content, post_status) VALUES 
  ('Test Title', 'Test Content', 'publish')`
  3. Создать первый тестовый пост: `INSERT INTO wp_posts (post_title, post_content, post_status) VALUES 
  ('Test Title', 'Test Content', 'publish')`
  4. Зафиксировать `id` постов

- **Шаги**:
  1. Отправить GET-запрос:
     * На `http://localhost:8000/index.php?rest_route=/wp/v2/posts&status=publish`

- **Ожидаемый результат**:
  1. Код ответа `200 OK`
  2. Тело ответа содержит массив постов со статусами `publish` и зафиксированными `id`

- **Постусловие**: 
  1. Удалить созданные посты: `DELETE FROM wp_posts WHERE ID = {id1}/{id2} OR post_parent = {id1}/{id2}`

- **Тестовые данные**:
  1. Basic Auth `USERNAME:PASSWORD` — `Firstname.Lastname:123-Test`
  2. `status` — `publish`

### Тест-кейс №09. Получение несуществующего поста

- **Предусловие**:
  1. Авторизоваться (`Firstname.Lastname:123-Test`)

- **Шаги**:
  1. Отправить GET-запрос:
     * На `http://localhost:8000/index.php?rest_route=/wp/v2/posts/9999`

- **Ожидаемый результат**:
  1. Код ответа `404 Not Found`
  2. Тело ответа содержит `error` или `message`

- **Тестовые данные**:
  1. Basic Auth `USERNAME:PASSWORD` — `Firstname.Lastname:123-Test`

### Тест-кейс №10. Поиск поста по несуществующему заголовку

- **Предусловие**:
  1. Авторизоваться (`Firstname.Lastname:123-Test`)

- **Шаги**:
  1. Отправить GET-запрос:
     * На `http://localhost:8000/index.php?rest_route=/wp/v2/posts&search=123NONEXISTENT_TITLE321`

- **Ожидаемый результат**:
  1. Код ответа `200 OK`
  2. Тело ответа содержит пустой массив `[]`

- **Тестовые данные**:
  1. Basic Auth `USERNAME:PASSWORD` — `Firstname.Lastname:123-Test`
  2. `search` — `123NONEXISTENT_TITLE321`

## D4 Тест-кейсы

### Тест-кейс №11. Создание папки

- **Предусловие**:
  1. Авторизоваться (`valid_token`)

- **Шаги**:
  1. Отправить PUT-запрос:
     * На `https://cloud-api.yandex.net/v1/disk/resources`
     * В параметрах запроса передать: `path=FolderForTest`

- **Ожидаемый результат**:
  1. Код ответа `201 Created`
  2. Тело ответа содержит `href` с параметром `path=FolderForTest`

- **Постусловие**: 
  1. Удалить созданную папку: `DELETE https://cloud-api.yandex.net/v1/disk/resources?path=FolderForTest&permanently=true`

- **Тестовые данные**:
  1. OAuth `valid_token`
  2. `path` — `FolderForTest`

### Тест-кейс №12. Удаление папки (перемещение в корзину)

- **Предусловие**:
  1. Авторизоваться (`valid_token`)
  2. Создать тестовую папку: `PUT https://cloud-api.yandex.net/v1/disk/resources?path=TestFolder`

- **Шаги**:
  1. Отправить DELETE-запрос:
     * На `https://cloud-api.yandex.net/v1/disk/resources`
     * В параметрах запроса передать: `path=TestFolder`

- **Ожидаемый результат**:
  1. Код ответа `204 No Content`
  2. Тело ответа отсутствует (`пустой ответ`)

- **Постусловие**: 
  1. Удалить папку в корзине: `DELETE https://cloud-api.yandex.net/v1/disk/trash/resources?path=TestFolder`

- **Тестовые данные**:
  1. OAuth `valid_token`
  2. `path` — `TestFolder`

### Тест-кейс №13. Восстановление папки

- **Предусловие**:
  1. Авторизоваться (`valid_token`)
  2. Создать тестовую папку: `PUT https://cloud-api.yandex.net/v1/disk/resources?path=TestFolder`
  3. Переместить тестовую папку в корзину: `DELETE https://cloud-api.yandex.net/v1/disk/resources?path=TestFolder`
  4. Зафиксировать `path` элемента с текстом `TestFolder`: `GET https://cloud-api.yandex.net/v1/disk/trash/resources` 

- **Шаги**:
  1. Отправить PUT-запрос:
     * На `https://cloud-api.yandex.net/v1/disk/trash/resources/restore`
     * В параметрах запроса передать зафиксированный `path`

- **Ожидаемый результат**:
  1. Код ответа `201 Created`
  2. Тело ответа содержит `href` с параметром `path=TestFolder`

- **Постусловие**: 
  1. Удалить восстановленную папку: `DELETE https://cloud-api.yandex.net/v1/disk/resources?path=TestFolder&permanently=true`

- **Тестовые данные**:
  1. OAuth `valid_token`
  2. `path` — `TestFolder`

### Тест-кейс №14. Создание уже существующей папки

- **Предусловие**:
  1. Авторизоваться (`valid_token`)
  2. Создать тестовую папку: `PUT https://cloud-api.yandex.net/v1/disk/resources?path=TestFolder`

- **Шаги**:
  1. Отправить PUT-запрос:
     * На `https://cloud-api.yandex.net/v1/disk/resources`
     * В параметрах запроса передать: `path=TestFolder`

- **Ожидаемый результат**:
  1. Код ответа `409 Conflict`
  2. Тело ответа содержит `error` и `message`

- **Постусловие**: 
  1. Удалить созданную папку: `DELETE https://cloud-api.yandex.net/v1/disk/resources?path=TestFolder&permanently=true`

- **Тестовые данные**:
  1. OAuth `valid_token`
  2. `path` — `TestFolder`

### Тест-кейс №15. Удаление несуществующей папки

- **Предусловие**:
  1. Авторизоваться (`valid_token`)

- **Шаги**:
  1. Отправить DELETE-запрос:
     * На `https://cloud-api.yandex.net/v1/disk/resources`
     * В параметрах запроса передать: `path=123NONEXISTENT_FOLDER321`

- **Ожидаемый результат**:
  1. Код ответа `404 Not Found`
  2. Тело ответа содержит `error` и `message`

- **Тестовые данные**:
  1. OAuth `valid_token`
  2. `path` — `123NONEXISTENT_FOLDER321`
