Руководство доступа к PostgreSQL через ODBC
============================================

.. image:: ../_static/sticker_lama_nothing.jpg
    :scale: 30%
    :align: center

.. todo::

    1.	Введение
    В данном руководстве описывается подключение к базе данных PostgreSQL через ODBC (Open Database Connectivity). ODBC – это стандартный интерфейс для доступа к различным СУБД (Microsoft SQL Server, MySQL, PostgreSQL, Oracle Database, Microsoft Access, MariaDB и др.). Руководство содержит инструкции для PostgreSQL версии 11.2.0. Следуют учесть, что действия могут отличаться в зависимости от конкретной версии PostgreSQL, которая используется.
    2.	Руководство по созданию доступа к PostgreSQL из Oracle
    2.1.	Установка PostgreSQL ODBC драйвера
    2.1.1.	Windows
    1)	Загрузить драйвер с официального сайта PostgreSQL для версии ОС (https://www.postgresql.org/ftp/odbc/)
    Примечание!
    Необходимо выбрать корректный тип разрядности драйвера. Если приложение, которому требуется доступ, является 32-разрядным, 
    а драйвер – 64-разрядным, возникнет ошибка: «ERROR [IM014] [Microsoft][ODBC Driver Manager] The specified DSN contains an architecture mismatch».
    2)	Установить драйвер ODBC для PostgreSQL
    В операционной системе Windows рекомендуется устанавливать драйвер из MSI-пакета.
    3)	Перейти в раздел «Источники данных ODBC» и создать новый системный DSN для PostgreSQL
    Если Windows 64-битная, а драйвер 32-битный, то панель управления следует запустить вручную: c:\windows\system32\odbcad32.exe.
    Укажите параметры подключения, такие как сервер, база данных, пользователь и пароль.
    Шаги выполнения:
    1)	нажать Системный DSN (Data Source Name)
    2)	нажать «Добавить», далее выбрать «PostgreSQL Unicode»
    3)	указать в полях: 
    o	Data Source Name:<имя источника данных> (например, Product);
    o	Description: <описание>;
    o	Database: <базу данных> (например, demo);
    o	Server: <сервер> (например, localhost);
    o	Port: <порт> (например, 5432);
    o	User Name: <имя пользователя> (например, postgres), 
    o	Password: <пароль> 
    4)	нажать «Test», чтобы проверить подключение.
    Если подключение успешно, отобразится сообщение, например, «Connection successful».
    5)	сохранить настройки.
    2.1.2.	Linux
    1)	Установить UnixODBC
    Менеджер ODBC драйверов, который понадобится для работы с ODBC в Linux-системах.
    Для Debian/Ubuntu:
    sudo apt-get update
    sudo apt-get install unixodbc unixodbc-dev
    Для RHEL/CentOS:
    sudo yum install unixODBC unixODBC-devel

    2)	Загрузить необходимый драйвер (например psqlODBC)
    3)	Установить драйвер ODBC для PostgreSQL (см. документацию на примере psqlODBC https://odbc.postgresql.org/docs/unix-compilation.html)
    4)	Настроить файлы конфигурации odbcinst.ini и odbc.ini. 
    •	odbcinst.ini
    Этот файл содержит информацию о драйверах ODBC. Обычно он находится в /etc/odbcinst.ini.
    sudo nano /etc/odbcinst.ini
    Добавить следующую информацию о драйвере PostgreSQL:
    [PostgreSQL]
    Description = ODBC for PostgreSQL
    Driver = /usr/lib/x86_64-linux-gnu/odbc/psqlodbcw.so
    Setup = /usr/lib/x86_64-linux-gnu/odbc/libodbcpsqlS.so
    FileUsage = 1

    Примечание!
    Пути к драйверам могут варьироваться в зависимости от используемой системы. Убедитесь, что указанные пути правильные.

    •	odbc.ini
    Этот файл содержит информацию о DSN. Обычно он находится в /etc/odbc.ini.
    sudo nano /etc/odbc.ini
    В odbc.ini добавить запись для DSN:
    [pg_dsn]
    Description = PostgreSQL DSN
    Driver = PostgreSQL
    Servername = <hostname>
    Port = 5432
    Database = <database_name>
    Username = <username>
    Password = <password>
    Пример настройки odbc.ini:
    [ODBC Data Sources]
    Product = PostgreSQL
    [Product]
    Description = PostgreSQL DSN
    Debug = 1
    CommLog = 1
    ReadOnly = no
    Driver = /usr/pgsql-9.1/lib/psqlodbc.so
    Servername = localhost
    FetchBufferSize = 99
    Username = postgres
    Password = <пароль> 
    Port = 5432
    Database = demo
    [Default]
    Driver = /usr/lib64/liboplodbcS.so.1

    Убедитесь, что все пути и параметры указаны правильно для вашей системы (Windows или Linux).
    5)	Проверить настройки
    После настройки конфигурационных файлов, можно использовать команду isql для проверки подключения к базе данных:
    isql -v <MyDataSource> <myuser> <mypassword>
    Если подключение успешно, команда должна вывести сообщение о успешном подключении.


    2.2.	Настройка Oracle Heterogeneous Services (hs) agents
    В данном разделе описывается процесс настройки компонента Oracle Database, который позволяет взаимодействовать с внешними, не-Oracle системами баз данных. HS агент выступает в качестве моста, позволяя Oracle Database выполнять запросы к данным, хранящимся в других СУБД, в данной инструкции это PostgreSQL.
    Примечание!
    Инструкции по настройке вашего агента могут незначительно отличаться от приведенных ниже инструкций. Пожалуйста, ознакомьтесь с Руководством по установке и эксплуатации вашего агента для получения более полной информации по установке.

    2.2.1.	Создание и настройка файла init<dg4odbc>.ora
    2.2.1.1.	Windows
    •	Перейти в директорию ORACLE_HOME\database\hs\admin\
    Где ORACLE_HOME домашняя директория, куда установлена база данных
    •	Создайте файл init<dg4odbc>.ora:
    initProduct.ora
    где <sid> – это Data Source Name:<имя источника данных>, созданное выше.
    •	Внести следующие параметры: 
    HS_FDS_CONNECT_INFO = PostgreSQL
    HS_FDS_TRACE_LEVEL = OFF
    Возможно, потребуются дополнительные параметры:
    HS_NLS_NCHAR = AL32UTF8
    HS_LANGUAGE = AMERICAN_AMERICA.AL32UTF8
    Для корректного отображения символов в базе данных PostgreSQL при использовании Heterogeneous Services (HS) в Oracle, необходимо правильно настроить параметры `HS_NLS_NCHAR` и `HS_LANGUAGE`. Эти параметры определяют национальные языковые настройки и кодировки.
    В PostgreSQL база данных может использовать различные кодировки символов, языки и кодовые страницы. Чтобы узнать, какие из них используются в конкретной базе данных, можно выполнить несколько SQL-запросов.
    а)	Кодировка символов и Collation (сравнение строк):

    SELECT
        datname,
        pg_encoding_to_char(encoding) AS encoding,
        datcollate,
        datctype
    FROM
        pg_database
    WHERE
        datname = 'имя_вашей_базы_данных';
    Этот запрос вернет информацию о кодировке, collation и ctype для указанной базы данных. Замените 'имя_вашей_базы_данных' на название вашей базы данных.
    б)	Язык сервера (локаль):
    Можно узнать текущие настройки локали сервера с помощью следующего запроса:
    SHOW lc_collate;
    SHOW lc_ctype;
    SHOW lc_messages;
    SHOW lc_monetary;
    SHOW lc_numeric;

    Эти команды покажут текущие настройки локали для различного рода данных (сравнение строк, типизация, сообщения, денежные единицы, числовые данные, время).
    в)	Кодовая страница (encoding):
    Кодовая страница отображает способ кодирования символов. PostgreSQL использует кодировку UTF-8 по умолчанию, но это может быть изменено при создании базы данных или при настройке сервера.
    SHOW server_encoding;
    Этот запрос покажет текущую кодировку сервера.

    2.2.1.2.	Linux
    •	Перейти в директорию $ORACLE_HOME/hs/admin
    •	Добавить или изменить настройки:
    HS_FDS_CONNECT_INFO = PostgreSQL
    HS_FDS_TRACE_LEVEL = 0
    Возможно, потребуются дополнительные параметры:
    HS_FDS_CONNECT_INFO = MoodlePostgres 
    #Указывает информацию для подключения к удаленной базе данных
    HS_FDS_SHAREABLE_NAME = /<path_to_postrges>/psqlodbc.so 
    #Указывает путь к драйверу ODBC для PostgreSQL
    HS_FDS_SUPPORT_STATISTICS = FALSE 
    #Контролирует поддержку статистики со стороны удаленной базы данных
    HS_KEEP_REMOTE_COLUMN_SIZE = ALL 
    #Указывает, как обрабатывать размеры удаленных столбцов
    Пример параметров 
    HS_FDS_CONNECT_INFO = PostgreSQL
    HS_FDS_SHAREABLE_NAME = /usr/lib/psqlodbc.so
    HS_FDS_SUPPORT_STATISTICS = FALSE
    HS_KEEP_REMOTE_COLUMN_SIZE = ALL

    2.3.	Настройка listener.ora
    •	Перейти в директорию c:\oracle\product\11.2.0\database\NETWORK\ADMIN\.
    •	Изменить файл listener.ora
    Открыть файл listener.ora и добавить следующие строки в секцию SID_LIST_LISTENER:
    # listener.ora Network Configuration File: C:\oracle\product\11.2.0\dbhome_1\network\admin\listener.ora
    # Generated by Oracle configuration tools.

    SID_LIST_LISTENER =
    (SID_LIST =
        (SID_DESC =
        (SID_NAME = CLRExtProc)
        (ORACLE_HOME = C:\oracle\product\11.2.0\database)
        (PROGRAM = extproc)
        (ENVS = "EXTPROC_DLLS=ONLY:C:\oracle\product\11.2.0\database\bin\oraclr11.dll")
        )
        (SID_DESC =
        (SID_NAME = Product)
        (ORACLE_HOME = C:\oracle\product\11.2.0\database)
        (PROGRAM = dg4odbc)
        )
    )

    LISTENER =
    (DESCRIPTION_LIST =
        (DESCRIPTION =
        (ADDRESS = (PROTOCOL = IPC)(KEY = EXTPROC1521))
        (ADDRESS = (PROTOCOL = TCP)(HOST = localhost)(PORT = 1521))
        )
    )

    •	Перезапустите Listener:
    Открыть командную строку и выполнить следующие команды:
    lsnrctl stop
    lsnrctl start
    Или 
    lsnrctl reload

    2.4.	Настроить файл tnsnames.ora
    •	Перейти в директорию c:\oracle\product\11.2.0\database\NETWORK\ADMIN\
    •	Изменить файл tnsnames.ora
    Открыть файл tnsnames.ora и добавьте следующую запись:
    # tnsnames.ora Network Configuration File: C:\oracle\product\11.2.0\dbhome_1\network\admin\tnsnames.ora
    # Generated by Oracle configuration tools.

    LISTENER_ORCL =
    (ADDRESS = (PROTOCOL = TCP)(HOST = localhost)(PORT = 1521))


    ORACLR_CONNECTION_DATA =
    (DESCRIPTION =
        (ADDRESS_LIST =
        (ADDRESS = (PROTOCOL = IPC)(KEY = EXTPROC1521))
        )
        (CONNECT_DATA =
        (SID = CLRExtProc)
        (PRESENTATION = RO)
        )
    )

    Product =
    (DESCRIPTION =
        (ADDRESS= (PROTOCOL = tcp)(HOST = 127.0.0.1)(PORT=1521))
        (CONNECT_DATA = (SID=PG_LINK))
        (HS=OK)
    )



    2.5.	Создание Database Link в Oracle
    Подключится к Oracle базе данных и выполнить следующий SQL-запрос:
    CREATE DATABASE LINK postgres_link
    CONNECT TO "<user>" IDENTIFIED BY "<pass>"
    USING 'POSTGRESQL';
    Пример:
    CREATE DATABASE LINK Product CONNECT TO "Product_scr" IDENTIFIED BY "password" USING 'Product';

    2.6.	Проверка соединения
    Выполнить тестовый запрос через созданный Database Link, чтобы убедиться, что соединение работает корректно:
    SELECT * FROM “<remote_table>”@postgres_link;

    Примечание!
    При выполнении запроса, таблицу нужно брать в кавычки

    2.7.	Устранение неполадок
    Если возникли проблемы с настройкой Database Link, рассмотрите следующие шаги для устранения неполадок:
    1)	Проверка конфигурационных файлов
    Убедитесь, что все параметры в файлах init<dg4odbc>.ora, listener.ora и tnsnames.ora указаны правильно.
    2)	Перезапуск Listener и баз данных
    Перезапустите Listener и убедитесь, что все службы работают корректно:
    lsnrctl stop
    lsnrctl start
    Или 
    lsnrctl reload
    3)	Просмотр журналов ошибок
    Просмотреть журналы Oracle для выявления ошибок, связанных с Heterogeneous Services или DG4ODBC. Журналы обычно находятся в директории $ORACLE_HOME/hs/log/.
    4)	Включение отладки
    Измените параметр HS_FDS_TRACE_LEVEL в файле init<dg4odbc>.ora на DEBUG:
    HS_FDS_TRACE_LEVEL = DEBUG
    5)	Связь с поддержкой
    Если все вышеперечисленное не помогло, обратитесь в службу поддержки Oracle или PostgreSQL за помощью.
     
    3.	Получение данных из базы данных PostgreSQL в Microsoft Excel или Access
    Чтобы быстро получить данные из базы данных PostgreSQL в Microsoft Excel или Access, можно использовать ODBC (Open Database Connectivity).
    Для этого необходимо выполнить подготовительные действия:
    1)	Установите ODBC-драйвер для PostgreSQL
    2)	Настройте ODBC DSN
    Подробности указаны в разделе: Установка PostgreSQL ODBC драйвера
    3.1.	Получение данных в Microsoft Excel
    1)	Открыть Microsoft Excel.
    2)	Перейти на вкладку «Данные».
    3)	Выбрать «Получить данные» -> «Из других источников» -> «Из ODBC».
    4)	Выбрать DSN:
    В открывшемся окне выбрать настроенный ранее DSN для PostgreSQL и нажать «ОК».
    5)	Ввести учетные данные:
    Введите имя пользователя и пароль для подключения к базе данных PostgreSQL.
    6)	Выбрать таблицы и данные:
    После подключения появится окно «Навигатор» (Navigator), где можно выбрать нужные таблицы и данные.
    7)	Загрузить данные:
    Нажать «Загрузить», чтобы импортировать выбранные данные в Excel.

    3.2.	Получение данных в Microsoft Access
    1)	Открыть Microsoft Access.
    2)	Создать новую базу данных или открыть существующую.
    3)	Импорт данных:
    a.	Перейти на вкладку «Внешние данные».
    b.	Нажать «Создать источник данных» -> «Из других источников» -> «Из ODBC».
    4)	Выбрать источник данных:
    В открывшемся диалоговом окне выбрать «Импортировать таблицы в текущую базу данных» или «Связать источник данных, создавая связную таблицу».
    Нажать «ОК».
    5)	Выбрать DSN:
    В открывшемся окне «Выбор источника данных» выбрать настроенный ранее DSN для PostgreSQL и нажать «ОК».
    6)	Ввести учетные данные:
    Ввести имя пользователя и пароль для подключения к базе данных PostgreSQL.
    7)	Выбрать таблицы:
    В диалоговом окне «Импорт объектов» выбрать необходимые таблицы и нажать «ОК».

    3.3.	Получение данных используя Power Query в Excel
    Power Query — мощный инструмент для импорта и трансформации данных в Excel. Можно использовать его для подключения к PostgreSQL через ODBC.
    Создание и настройка файла с расширением .dqy для подключения к базе данных PostgreSQL и выполнения SQL-запроса включает несколько шагов.
    1)	Создание файла с расширением .dqy:
    a.	Открыть текстовый редактор (например, Notepad, Notepad++, Visual Studio Code и т.п.).
    b.	Создать новый пустой файл.
    2)	Запись необходимых данных в файл:
    Вставить следующую информацию в файл, заменив <user> и <password> на соответствующие значения:
        XLODBC #Обозначает, что это файл запроса ODBC для Excel.
        1 #Версия файла.
        DRIVER={PostgreSQL Unicode};...;XaOpt=1 #Строка соединения, которая содержит параметры подключения к PostgreSQL.
        select * from Product_rate_plans: #SQL-запрос, который будет выполнен после установления соединения. В данном случае, он выбирает все данные из таблицы Product_rate_plans.
    Пример файла:
    XLODBC
    1
    DRIVER={PostgreSQL Unicode};DATABASE=demo;SERVER=Localhost;PORT=5432;UID=postgres;PASSWORD=<password>;SSLmode=disable;ReadOnly=0;Protocol=7.4;FakeOidIndex=0;ShowOidColumn=0;RowVersioning=0;ShowSystemTables=0;ConnSettings=;Fetch=100;Socket=4096;UnknownSizes=0;MaxVarcharSize=255;MaxLongVarcharSize=8190;Debug=0;CommLog=0;Optimizer=0;Ksqo=1;UseDeclareFetch=0;TextAsLongVarchar=1;UnknownsAsLongVarchar=0;BoolsAsChar=1;Parse=0;CancelAsFreeStmt=0;ExtraSysTablePrefixes=dd_;LFConversion=1;UpdatableCursors=1;DisallowPremature=0;TrueIsMinus1=0;BI=0;ByteaAsLongVarBinary=0;UseServerSidePrepare=0;LowerCaseIdentifier=0;GssAuthUseGSS=0;XaOpt=1
    select * from aircrafts
    Всего должно получиться 4 строки, запрос - в последней.
    DRIVER= Эта строка подключения содержит множество параметров, которые можно настроить в зависимости от потребностей и конфигурации базы данных:
    1.DRIVER={PostgreSQL Unicode}: Указывает драйвер ODBC, который используется для подключения. В данном случае это драйвер для PostgreSQL с поддержкой Unicode.
    2. DATABASE=demo: Указывает имя базы данных, к которой выполняется подключение. В данном случае это база данных "demo".
    3. SERVER=Localhost: Указывает имя хоста или IP-адрес сервера базы данных. "Localhost" означает, что сервер базы данных работает на локальном компьютере.
    4. PORT=5432: Указывает порт, который используется для подключения к серверу базы данных. По умолчанию PostgreSQL использует порт 5432.
    5. UID=postgres: Указывает имя пользователя (User ID), под которым происходит подключение к базе данных. В данном случае это "postgres".
    6. PASSWORD=<password>: Указывает пароль для пользователя, указанного в UID.
    7. SSLmode=disable: Указывает режим SSL для подключения. "disable" означает, что SSL не используется.
    8. ReadOnly=0: Указывает, будет ли подключение только для чтения. 0 (ноль) означает, что подключение не только для чтения.
    9. Protocol=7.4: Указывает версию протокола PostgreSQL, которая будет использоваться.
    10. FakeOidIndex=0: Этот параметр определяет, будет ли драйвер создавать фиктивный OID индекс. 0 означает, что он не будет создан.
    11. ShowOidColumn=0: Указывает, будет ли отображаться колонка OID. 0 означает, что она не будет отображаться.
    12. RowVersioning=0: Указывает, используется ли управление версиями строк. 0 означает, что оно не используется.
    13. ShowSystemTables=0: Указывает, будут ли отображаться системные таблицы. 0 означает, что они не будут отображаться.
    14. ConnSettings=: Дополнительные настройки подключения. В данном случае они не указаны.
    15. Fetch=100: Указывает количество строк, которые будут извлекаться за один раз.
    16. Socket=4096: Указывает размер сокета в байтах.
    17. UnknownSizes=0: Указывает, как обрабатывать столбцы с неизвестными размерами. 0 означает, что они будут обрабатываться как есть.
    18. MaxVarcharSize=255: Указывает максимальный размер для столбцов типа VARCHAR.
    19. MaxLongVarcharSize=8190: Указывает максимальный размер для столбцов типа LONGVARCHAR.
    20. Debug=0: Указывает, будет ли включен режим отладки. 0 означает, что он не включен.
    21. CommLog=0: Указывает, будет ли включен журнал коммуникаций. 0 означает, что он не включен.
    22. Optimizer=0: Указывает, будет ли использоваться оптимизатор. 0 означает, что он не будет использоваться.
    23. Ksqo=1: Указывает, будет ли использоваться ключевой запрос оптимизатора. 1 означает, что он будет использоваться.
    24. UseDeclareFetch=0: Указывает, будет ли использоваться DECLARE и FETCH для извлечения данных. 0 означает, что они не будут использоваться.
    25. TextAsLongVarchar=1: Указывает, будут ли столбцы типа TEXT обрабатываться как LONGVARCHAR. 1 означает, что будут.
    26. UnknownsAsLongVarchar=0: Указывает, будут ли неизвестные типы обрабатываться как LONGVARCHAR. 0 означает, что не будут.
    27. BoolsAsChar=1: Указывает, будут ли булевые значения обрабатываться как CHAR. 1 означает, что будут.
    28. Parse=0: Указывает, будет ли драйвер анализировать SQL-запросы. 0 означает, что не будет.
    29. CancelAsFreeStmt=0: Указывает, будет ли CANCEL обрабатываться как FreeStmt. 0 означает, что не будет.
    30. ExtraSysTablePrefixes=dd_: Указывает дополнительные префиксы для системных таблиц.
    31. LFConversion=1: Указывает, будет ли производиться конвертация строк конца строки. 1 означает, что будет.
    32. UpdatableCursors=1: Указывает, будут ли курсоры обновляемыми. 1 означает, что будут.
    33. DisallowPremature=0: Указывает, будет ли запрещен преждевременный доступ к данным. 0 означает, что не будет.
    34. TrueIsMinus1=0: Указывает, будет ли TRUE представляться как -1. 0 означает, что не будет.
    35. BI=0: Параметр, возможно, означает использование метаданных для идентификации столбцов. 0 означает, что не используется.
    36. ByteaAsLongVarBinary=0: Указывает, будут ли столбцы типа BYTEA обрабатываться как LONGVARBINARY. 0 означает, что не будут.
    37. UseServerSidePrepare=0: Указывает, будет ли использоваться подготовка на стороне сервера. 0 означает, что не будет.
    38. LowerCaseIdentifier=0: Указывает, будут ли идентификаторы преобразованы в нижний регистр. 0 означает, что не будут.
    39. GssAuthUseGSS=0: Указывает, будет ли использоваться GSS-авторизация. 0 означает, что не будет.
    40. XaOpt=1: Указывает опции для XA (расширенной архитектуры транзакций). 1 означает, что опции включены.
    Перед выполнением запроса проверить данные, замену DATABASE, <user> на имя пользователя базы данных PostgreSQL и <password>,  на соответствующий пароль.
    3)	Сохранение файла:
    Сохранить файл с расширением .dqy.
    Убедится, что в процессе сохранения выбрано правильное расширение .dqy, а не .txt или другое.
    4)	Открыть файл
    После открытия файла, будет выполнен запрос.
    Примечание!
    Проверьте, что все настройки ODBC и учётные данные правильны, чтобы избежать проблем с подключением
