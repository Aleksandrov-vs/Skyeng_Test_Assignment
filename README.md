## SkyengTestAssignment
## Задача

Нужно повысить качество передаваемого кода на ревью, чтобы ускорить процесс разработки и поставки более качественного кода в проекты. Для этого создайте сервис проверки файлов с выполненными задачами.
Основные модули, из которых состоит система:
1. Модуль авторизации и регистрации пользователя.
Пользователь должен иметь возможность зарегистрироваться в системе по паре почта и пароль, а также войти по этим данным.
2. Модуль загрузки файлов с исходным кодом.
Авторизованный пользователь должен иметь возможность загрузить файл в систему, при этом информация о загруженном файле должна сохраниться в базу данных с пометкой о том, что файл новый. Помимо этого, пользователь должен иметь возможность удалить файл или перезаписать, таким образом, в базе данных должны быть соответствующие пометки. Очень важно не давать загружать файлы, у которых расширение не равно “.py”.
3. Модуль проверки соответствия кода общепринятым правилам.
По расписанию выполняется задача на автоматическую проверку кода для новых загруженных или перезагруженных файлов. По итогу проверки необходимо сформировать отложенную задачу на отправку письма пользователю с информацией о проведенной проверке. Важно хранить лог каждой проверки для каждого файла, который находится в списке файлов у пользователя в системе.
4. Модуль отправки письма с уведомлением пользователю.
Необходимо реализовать обработку задач из очереди на отправку уведомлений пользователю о результате проверки его файла. При этом, важно в логах проверки отмечать факт отправки сообщения пользователю.
5. Модуль отчета о проведенных проверках
В системе также должен быть интерфейс, в котором пользователь может просмотреть результаты выполненных проверок с пометками об отправке отчета пользователю на почту.

#Запуск проекта:
1. создайте `.env` файл с переменными окружения. Пример в `.env.example` (Для теста можно просто скопировать)
2. соберите и запустите контейнеры `docker-compose up --build` 