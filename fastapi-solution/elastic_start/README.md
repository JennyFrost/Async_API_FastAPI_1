## Описание
Сервис для первичной загрузки данных в эластик из дампа
Необходим для разработки, после запуска docker-compose с эластиком будет загружать данные из дампа.
Если данные уже загружены, сервис засыпает.

### Задачи:
 - Выгрузить дамп из постгреса в json +
    - изменить код изначального etl, чтобы он просто выгрузил все данные в json +
 - Положить файл дампа и файл с индексом в папку с сервисом +
 - Написать логику для загрузки дампа в elastic
    - Подключение к эластику +
    - Проверка, есть ли индекс в эластике
        - Если индекса нет то загрузка индекса из файла
            - Если файла нет, заверщение программы с ошибкой
        - После загрузки индекса, или если он есть:
            - Проверка количества записей, должно быть от 900 записей, можно поставить как параметр, жесткая проверка или мягкая
        - Если записей нет, то загрузка записей из дампа
            - Если дампа нет то завершение программы с ошибкой
        - После загрузки записей проверка количества, если количество совпадает то окончание программы
 - Тестовый запуск сервиса локально
 - Создать докер файл
 - Создать скрипт для запуска сервиса, сервис должен запуститься после elastic, так же можно в сервисе прописать переподключение при запуске, но только при подключении к эластику, при любой ошибке сервис должен валиться
 - Запуск сервиса через docker-compose вместе с эластиком