# Django Rest Framework questionnaire API

#### API для проведения опросов пользователей.
#### Регистрация не предусмотрена.
#### Для авторизации администраторов используется тип авторизации Basic Auth (username/password).
#### Доступные действия:

1. Управление списком опросов (CRUD-операции) - только администраторы системы:
  - http://127.0.0.1:8000/questionnaires/ - POST, GET (выдаются только актуальные опросы с датой завершения более текущей даты) 
  - http://127.0.0.1:8000/questionnaires/<int:pk>/ - GET, PUT
  - http://127.0.0.1:8000/questionnaires/<int:pk>/questions/ - GET, список всех вопросов по конкретному опросу
  - http://127.0.0.1:8000/questionnaires/<int:pk>/completed_polls/ - GET, список всех прохождений по конкретному опросу 

  Для уже созданных опросов при обновлении методом PUT запрещено изменение поля start_date 
  ##### Поля опроса:
  - title - наименование (строка (макс. 500 символов))
  - start_date - дата начала (дата и время)
  - end_date - дата завершения (дата и время)
  - body - описание (неограниченная строка)


2. Управление вопросами к опросам (CRUD-операции) - только администраторы системы:
  - http://127.0.0.1:8000/questions/ - POST, GET
  - http://127.0.0.1:8000/questions/<int:pk>/ - GET, PUT 
  - http://127.0.0.1:8000/questions/<int:pk>/answers/ - GET, список всех доступных ответов по конкретному вопросу<br> 
  - http://127.0.0.1:8000/questions/<int:pk>/polls/ - GET, список всех фактических ответов всех пользователей по конкретному вопросу
  - http://127.0.0.1:8000/questions/<int:pk>/polls/?user_id=<int:id>/ - GET, список всех фактических ответов пользователя с user_id = id по конкретному вопросу  
  
  ##### Поля вопроса:
  - title - текст вопроса (строка (макс. 500 символов))
  - question_type - тип вопроса (строка с ограниченным списком значений - 'text'/'single_choice'/multiple_choices)
  - questionnaire - внешний ключ к опросам (целое число)


3. Управление доступными ответами к вопросам: (CRUD-операции)  - только администраторы системы:
  - http://127.0.0.1:8000/answers/ - POST, GET
  - http://127.0.0.1:8000/answers/<int:pk>/ - GET, PUT 
  
  ##### Поля ответа:
  - text - текст ответа (строка (макс. 500 символов))
  - question - внешний ключ к вопросам (целое число)


4. Запись в систему фактических ответов пользователей на вопросы опроса - не требуется админский доступ.
Выполняются проверки на корректность ответа (ранее не был получен, кол-во ответов не превышает кол-во доступных ответов на вопрос, ответ соответствует доступным вариантам ответа на вопрос.
  ##### Ответ (текст ответа) записывается в разрезе id пользователя и id вопроса.
  - http://127.0.0.1:8000/polls/ - GET, POST 
  - http://127.0.0.1:8000/polls/answers/?user_id=<int:id>/ - GET с параметром 'user_id': получение списка всех ответов пользователя с user_id = id

  ##### Поля фактического ответа пользователя:
  - user_id - идентификатор пользователя (целое число)
  - question - внешний ключ к вопросам (целое число)
  - user_answer - фактический текст ответа (строка (макс. 500 символов))


5. Информация о полностью пройденных пользователями опросах - (CRUD-операции) - только администраторы системы.
Запись о пройденном опросе добавляется автоматически после успешной записи в базу не менее одного ответа пользователя на каждый вопрос в опросе.
  ##### Результат записывается в разрезе id пользователя, id опроса и текущей даты со временем.
  - http://127.0.0.1:8000/completed_polls/ - GET, POST 
  - http://127.0.0.1:8000/completed_polls/by_user/?user_id=<int:id>/ - GET с параметром 'user_id': получение списка всех ответов пользователя с user_id = id

  ##### Поля записи о прохождении опроса пользователем:
  - user_id - идентификатор пользователя (целое число)
  - questionnaire - внешний ключ к опросу (целое число)
  - completion_date - дата и время завершения прохождения осмотра (заполняется автоматически)

#### Предварительные шаги для запуска приложения (на тестовом сервере):
  1. Развернуть виртуальное окружение для проекта - `pip -m venv venv`
  2. Активировать виртуальное окружение для проекта - `source venv/bin/activate` в терминале Linux/Mac или `venv\Scripts\activate.bat` в командной строке Windows.
  3. Установить требуемые зависимости проекта - `pip install -r requirements.txt`
  4. В django shell выполнить последовательно команды: 
  ```
    python manage.py createsuperuser
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
  ```
  
  Приложение будет доступно в отладочном режиме по указанным выше урлам.
