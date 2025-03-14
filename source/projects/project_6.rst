Руководство доступа к PostgreSQL через ODBC
============================================

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
    3. DATABASE=demo: Указывает имя базы данных, к которой выполняется подключение. В данном случае это база данных "demo".
    4. SERVER=Localhost: Указывает имя хоста или IP-адрес сервера базы данных. "Localhost" означает, что сервер базы данных работает на локальном компьютере.
    5. PORT=5432: Указывает порт, который используется для подключения к серверу базы данных. По умолчанию PostgreSQL использует порт 5432.
    6. UID=postgres: Указывает имя пользователя (User ID), под которым происходит подключение к базе данных. В данном случае это "postgres".
    7. PASSWORD=<password>: Указывает пароль для пользователя, указанного в UID.
    8. SSLmode=disable: Указывает режим SSL для подключения. "disable" означает, что SSL не используется.
    9. ReadOnly=0: Указывает, будет ли подключение только для чтения. 0 (ноль) означает, что подключение не только для чтения.
    10. Protocol=7.4: Указывает версию протокола PostgreSQL, которая будет использоваться.
    11. FakeOidIndex=0: Этот параметр определяет, будет ли драйвер создавать фиктивный OID индекс. 0 означает, что он не будет создан.
    12. ShowOidColumn=0: Указывает, будет ли отображаться колонка OID. 0 означает, что она не будет отображаться.
    13. RowVersioning=0: Указывает, используется ли управление версиями строк. 0 означает, что оно не используется.
    14. ShowSystemTables=0: Указывает, будут ли отображаться системные таблицы. 0 означает, что они не будут отображаться.
    15. ConnSettings=: Дополнительные настройки подключения. В данном случае они не указаны.
    16. Fetch=100: Указывает количество строк, которые будут извлекаться за один раз.
    17. Socket=4096: Указывает размер сокета в байтах.
    18. UnknownSizes=0: Указывает, как обрабатывать столбцы с неизвестными размерами. 0 означает, что они будут обрабатываться как есть.
    19. MaxVarcharSize=255: Указывает максимальный размер для столбцов типа VARCHAR.
    20. MaxLongVarcharSize=8190: Указывает максимальный размер для столбцов типа LONGVARCHAR.
    21. Debug=0: Указывает, будет ли включен режим отладки. 0 означает, что он не включен.
    22. CommLog=0: Указывает, будет ли включен журнал коммуникаций. 0 означает, что он не включен.
    23. Optimizer=0: Указывает, будет ли использоваться оптимизатор. 0 означает, что он не будет использоваться.
    24. Ksqo=1: Указывает, будет ли использоваться ключевой запрос оптимизатора. 1 означает, что он будет использоваться.
    25. UseDeclareFetch=0: Указывает, будет ли использоваться DECLARE и FETCH для извлечения данных. 0 означает, что они не будут использоваться.
    26. TextAsLongVarchar=1: Указывает, будут ли столбцы типа TEXT обрабатываться как LONGVARCHAR. 1 означает, что будут.
    27. UnknownsAsLongVarchar=0: Указывает, будут ли неизвестные типы обрабатываться как LONGVARCHAR. 0 означает, что не будут.
    28. BoolsAsChar=1: Указывает, будут ли булевые значения обрабатываться как CHAR. 1 означает, что будут.
    29. Parse=0: Указывает, будет ли драйвер анализировать SQL-запросы. 0 означает, что не будет.
    30. CancelAsFreeStmt=0: Указывает, будет ли CANCEL обрабатываться как FreeStmt. 0 означает, что не будет.
    31. ExtraSysTablePrefixes=dd_: Указывает дополнительные префиксы для системных таблиц.
    32. LFConversion=1: Указывает, будет ли производиться конвертация строк конца строки. 1 означает, что будет.
    33. UpdatableCursors=1: Указывает, будут ли курсоры обновляемыми. 1 означает, что будут.
    34. DisallowPremature=0: Указывает, будет ли запрещен преждевременный доступ к данным. 0 означает, что не будет.
    35. TrueIsMinus1=0: Указывает, будет ли TRUE представляться как -1. 0 означает, что не будет.
    36. BI=0: Параметр, возможно, означает использование метаданных для идентификации столбцов. 0 означает, что не используется.
    37. ByteaAsLongVarBinary=0: Указывает, будут ли столбцы типа BYTEA обрабатываться как LONGVARBINARY. 0 означает, что не будут.
    38. UseServerSidePrepare=0: Указывает, будет ли использоваться подготовка на стороне сервера. 0 означает, что не будет.
    39. LowerCaseIdentifier=0: Указывает, будут ли идентификаторы преобразованы в нижний регистр. 0 означает, что не будут.
    40. GssAuthUseGSS=0: Указывает, будет ли использоваться GSS-авторизация. 0 означает, что не будет.
    41. XaOpt=1: Указывает опции для XA (расширенной архитектуры транзакций). 1 означает, что опции включены.
    Перед выполнением запроса проверить данные, замену DATABASE, <user> на имя пользователя базы данных PostgreSQL и <password>,  на соответствующий пароль.
    3)	Сохранение файла:
    Сохранить файл с расширением .dqy.
    Убедится, что в процессе сохранения выбрано правильное расширение .dqy, а не .txt или другое.
    4)	Открыть файл
    После открытия файла, будет выполнен запрос.
    Примечание!
    Проверьте, что все настройки ODBC и учётные данные правильны, чтобы избежать проблем с подключением

.. _introduction:

1. Введение
------------

Настоящее руководство предназначено для администраторов баз данных, разработчиков и специалистов по интеграции систем, которые занимаются настройкой подключения между базой данных PostgreSQL и другими программными продуктами через ODBC (Open Database Connectivity). 

Цель данного документа — предоставить подробные инструкции по настройке подключения к PostgreSQL через ODBC для различных платформ и инструментов, таких как Oracle Database, Microsoft Excel, Microsoft Access и Power Query. Руководство содержит шаги для установки драйверов, настройки конфигурационных файлов и выполнения запросов.

Руководство фокусируется на PostgreSQL версии 11.2.0. Следует учесть, что действия могут отличаться в зависимости от конкретной версии PostgreSQL, используемой в вашей среде.

1.1 Целевая аудитория:
+++++++++++++++++++++++

Данная инструкция будет полезна следующим категориям пользователей:

- **Администраторы баз данных**: Которые настраивают подключение между различными системами баз данных (например, Oracle и PostgreSQL).
- **Разработчики**: Которым требуется доступ к данным PostgreSQL из приложений или инструментов, таких как Microsoft Excel, Access или Power Query.
- **Специалисты по интеграции систем**: Задачи которых включают объединение разных баз данных и обеспечение их взаимодействия через стандартные протоколы, такие как ODBC.

Для успешного использования данного руководства рекомендуется иметь базовые знания работы с ODBC, SQL и конфигурационными файлами операционных систем.

.. _guide_to_postgresql_access:

2. Руководство по созданию доступа к PostgreSQL из Oracle
-----------------------------------------------------------

.. _installing_odbc_driver:

2.1 Установка PostgreSQL ODBC драйвера
+++++++++++++++++++++++++++++++++++++++

.. _windows_installation:

2.1.1 Windows
^^^^^^^^^^^^^^

1. Загрузить драйвер с официального сайта PostgreSQL для версии ОС: https://www.postgresql.org/ftp/odbc/

   .. note::
      Необходимо выбрать корректный тип разрядности драйвера. Если приложение, которому требуется доступ, является 32-разрядным, а драйвер – 64-разрядным, возникнет ошибка: ``ERROR [IM014] [Microsoft][ODBC Driver Manager] The specified DSN contains an architecture mismatch``.

2. Установить драйвер ODBC для PostgreSQL.
   В операционной системе Windows рекомендуется устанавливать драйвер из MSI-пакета.

3. Перейти в раздел «Источники данных ODBC» и создать новый системный DSN для PostgreSQL.
   Если Windows 64-битная, а драйвер 32-битный, то панель управления следует запустить вручную: ``c:\windows\system32\odbcad32.exe``.

   Шаги выполнения:
   
   - Нажать «Системный DSN» (Data Source Name).
   - Нажать «Добавить», далее выбрать «PostgreSQL Unicode».
   - Указать параметры:
     
     - Data Source Name: <имя источника данных> (например, Product).
     - Description: <описание>.
     - Database: <базу данных> (например, demo).
     - Server: <сервер> (например, localhost).
     - Port: <порт> (например, 5432).
     - User Name: <имя пользователя> (например, postgres).
     - Password: <пароль>.

   - Нажать «Test», чтобы проверить подключение.
   - Сохранить настройки.

.. _linux_installation:

2.1.2 Linux
^^^^^^^^^^^^^^^

1. Установить UnixODBC.
   Менеджер ODBC драйверов, который понадобится для работы с ODBC в Linux-системах.

   Для Debian/Ubuntu:
   
   .. code-block:: bash
   
      sudo apt-get update
      sudo apt-get install unixodbc unixodbc-dev

   Для RHEL/CentOS:
   
   .. code-block:: bash
   
      sudo yum install unixODBC unixODBC-devel

2. Загрузить необходимый драйвер (например psqlODBC).

3. Установить драйвер ODBC для PostgreSQL (см. документацию на примере psqlODBC: https://odbc.postgresql.org/docs/unix-compilation.html).

4. Настроить файлы конфигурации ``odbcinst.ini`` и ``odbc.ini``.

   - ``odbcinst.ini``
   
     Этот файл содержит информацию о драйверах ODBC. Обычно он находится в ``/etc/odbcinst.ini``.
     
     .. code-block:: ini
     
        [PostgreSQL]
        Description = ODBC for PostgreSQL
        Driver = /usr/lib/x86_64-linux-gnu/odbc/psqlodbcw.so
        Setup = /usr/lib/x86_64-linux-gnu/odbc/libodbcpsqlS.so
        FileUsage = 1

     .. note::
        Пути к драйверам могут варьироваться в зависимости от используемой системы. Убедитесь, что указанные пути правильные.

   - ``odbc.ini``
   
     Этот файл содержит информацию о DSN. Обычно он находится в ``/etc/odbc.ini``.
     
     .. code-block:: ini
     
        [pg_dsn]
        Description = PostgreSQL DSN
        Driver = PostgreSQL
        Servername = <hostname>
        Port = 5432
        Database = <database_name>
        Username = <username>
        Password = <password>

     Пример настройки ``odbc.ini``:
     
     .. code-block:: ini
     
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

5. Проверить настройки.
   После настройки конфигурационных файлов, можно использовать команду ``isql`` для проверки подключения к базе данных:
   
   .. code-block:: bash
   
      isql -v <MyDataSource> <myuser> <mypassword>

   Если подключение успешно, команда должна вывести сообщение о успешном подключении.

.. _oracle_heterogeneous_services:

2.2 Настройка Oracle Heterogeneous Services (hs) agents
--------------------------------------------------------

.. note::
   В данном разделе описывается процесс настройки компонента Oracle Database, который позволяет взаимодействовать с внешними, не-Oracle системами баз данных. HS агент выступает в качестве моста, позволяя Oracle Database выполнять запросы к данным, хранящимся в других СУБД, в данной инструкции это PostgreSQL.

   Инструкции по настройке вашего агента могут незначительно отличаться от приведенных ниже инструкций. Пожалуйста, ознакомьтесь с Руководством по установке и эксплуатации вашего агента для получения более полной информации по установке.

.. _init_file_creation:

2.2.1 Создание и настройка файла init<dg4odbc>.ora
+++++++++++++++++++++++++++++++++++++++++++++++++++

.. _windows_init_file:

2.2.1.1 Windows
^^^^^^^^^^^^^^^^^^^^^

1. Перейти в директорию ``ORACLE_HOME\database\hs\admin\``.
   Где ``ORACLE_HOME`` — домашняя директория, куда установлена база данных.

2. Создайте файл ``init<dg4odbc>.ora``:
   ``initProduct.ora``, где ``<sid>`` — это Data Source Name:<имя источника данных>, созданное выше.

3. Внести следующие параметры:
   
   .. code-block:: ini
   
      HS_FDS_CONNECT_INFO = PostgreSQL
      HS_FDS_TRACE_LEVEL = OFF

   Возможно, потребуются дополнительные параметры:
   
   .. code-block:: ini
   
      HS_NLS_NCHAR = AL32UTF8
      HS_LANGUAGE = AMERICAN_AMERICA.AL32UTF8

   Для корректного отображения символов в базе данных PostgreSQL при использовании Heterogeneous Services (HS) в Oracle, необходимо правильно настроить параметры ``HS_NLS_NCHAR`` и ``HS_LANGUAGE``. Эти параметры определяют национальные языковые настройки и кодировки.

   В PostgreSQL база данных может использовать различные кодировки символов, языки и кодовые страницы. Чтобы узнать, какие из них используются в конкретной базе данных, можно выполнить несколько SQL-запросов.

   a) Кодировка символов и Collation (сравнение строк):
   
   .. code-block:: sql
   
      SELECT
          datname,
          pg_encoding_to_char(encoding) AS encoding,
          datcollate,
          datctype
      FROM
          pg_database
      WHERE
          datname = 'имя_вашей_базы_данных';

   Этот запрос вернет информацию о кодировке, collation и ctype для указанной базы данных. Замените ``'имя_вашей_базы_данных'`` на название вашей базы данных.

   b) Язык сервера (локаль):
   
   Можно узнать текущие настройки локали сервера с помощью следующих запросов:
   
   .. code-block:: sql
   
      SHOW lc_collate;
      SHOW lc_ctype;
      SHOW lc_messages;
      SHOW lc_monetary;
      SHOW lc_numeric;

   Эти команды покажут текущие настройки локали для различного рода данных (сравнение строк, типизация, сообщения, денежные единицы, числовые данные, время).

   c) Кодовая страница (encoding):
   
   Кодовая страница отображает способ кодирования символов. PostgreSQL использует кодировку UTF-8 по умолчанию, но это может быть изменено при создании базы данных или при настройке сервера.
   
   .. code-block:: sql
   
      SHOW server_encoding;

   Этот запрос покажет текущую кодировку сервера.

.. _linux_init_file:

2.2.1.2 Linux
^^^^^^^^^^^^^^^

1. Перейти в директорию ``$ORACLE_HOME/hs/admin``.

2. Добавить или изменить настройки:
   
   .. code-block:: ini
   
      HS_FDS_CONNECT_INFO = PostgreSQL
      HS_FDS_TRACE_LEVEL = 0

   Возможно, потребуются дополнительные параметры:
   
   .. code-block:: ini
   
      HS_FDS_CONNECT_INFO = MoodlePostgres 
      # Указывает информацию для подключения к удаленной базе данных
      HS_FDS_SHAREABLE_NAME = /<path_to_postrges>/psqlodbc.so 
      # Указывает путь к драйверу ODBC для PostgreSQL
      HS_FDS_SUPPORT_STATISTICS = FALSE 
      # Контролирует поддержку статистики со стороны удаленной базы данных
      HS_KEEP_REMOTE_COLUMN_SIZE = ALL 
      # Указывает, как обрабатывать размеры удаленных столбцов

   Пример параметров:
   
   .. code-block:: ini
   
      HS_FDS_CONNECT_INFO = PostgreSQL
      HS_FDS_SHAREABLE_NAME = /usr/lib/psqlodbc.so
      HS_FDS_SUPPORT_STATISTICS = FALSE
      HS_KEEP_REMOTE_COLUMN_SIZE = ALL

.. _listener_ora_configuration:

2.3 Настройка listener.ora
---------------------------

1. Перейти в директорию ``c:\oracle\product\11.2.0\database\NETWORK\ADMIN\``.

2. Изменить файл ``listener.ora``.
   Открыть файл ``listener.ora`` и добавить следующие строки в секцию ``SID_LIST_LISTENER``:

   .. code-block:: ini

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

   Объяснение параметров:
   
   - ``(SID_NAME = Product)``: Указывает имя DSN, созданное ранее для PostgreSQL.
   - ``(ORACLE_HOME = ...)``: Указывает путь к домашней директории Oracle.
   - ``(PROGRAM = dg4odbc)``: Указывает программу, которая будет использоваться для подключения к внешней базе данных через Heterogeneous Services.

3. Проверить статус Listener после изменения конфигурации:
   
   .. code-block:: bash
   
      lsnrctl status

   Если Listener не работает корректно, выполните перезапуск:
   
   .. code-block:: bash
   
      lsnrctl stop
      lsnrctl start

   Или обновите конфигурацию без перезапуска:
   
   .. code-block:: bash
   
      lsnrctl reload

.. _tnsnames_ora_configuration:

2.4 Настройка tnsnames.ora
---------------------------

1. Перейти в директорию ``c:\oracle\product\11.2.0\database\NETWORK\ADMIN\``.

2. Изменить файл ``tnsnames.ora``.
   Открыть файл ``tnsnames.ora`` и добавить следующую запись:

   .. code-block:: ini

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

   Объяснение параметров:
   
   - ``(HS=OK)``: Указывает, что это соединение использует Heterogeneous Services (HS). Без этого параметра Oracle не сможет работать с внешними базами данных.

3. Проверить корректность конфигурации:
   
   .. code-block:: bash
   
      tnsping <SID>

   Например:
   
   .. code-block:: bash
   
      tnsping Product

   Если конфигурация правильная, команда выведет успешный результат.

.. _database_link_creation:

2.5 Создание Database Link в Oracle
------------------------------------

Подключиться к Oracle базе данных и выполнить следующий SQL-запрос:

.. code-block:: sql

   CREATE DATABASE LINK postgres_link
   CONNECT TO "<user>" IDENTIFIED BY "<pass>"
   USING 'POSTGRESQL';

Пример:

.. code-block:: sql

   CREATE DATABASE LINK Product CONNECT TO "Product_scr" IDENTIFIED BY "password" USING 'Product';

Объяснение параметров:

- ``<user>``: Учетное имя пользователя PostgreSQL, которое имеет доступ к целевой базе данных.
- ``<pass>``: Пароль для указанного пользователя PostgreSQL.

Удаление или изменение существующего Database Link:

- Для удаления:
  
  .. code-block:: sql
  
     DROP DATABASE LINK postgres_link;

- Для изменения: Сначала удалите существующий link, затем создайте новый с нужными параметрами.

.. _connection_test:

2.6 Проверка соединения
------------------------

Выполнить тестовый запрос через созданный Database Link, чтобы убедиться, что соединение работает корректно:

.. code-block:: sql

   SELECT * FROM "<remote_table>"@postgres_link;

Примечание:
При выполнении запроса, таблицу нужно брать в двойные кавычки. Это связано с чувствительностью PostgreSQL к регистру имен объектов. Двойные кавычки позволяют использовать точное имя таблицы, сохраняя его регистр.

.. _troubleshooting:

2.7 Устранение неполадок
-------------------------

Если возникли проблемы с настройкой Database Link, рассмотрите следующие шаги для устранения неполадок:

1. **Проверка конфигурационных файлов**
   Убедитесь, что все параметры в файлах ``init<dg4odbc>.ora``, ``listener.ora`` и ``tnsnames.ora`` указаны правильно.

2. **Перезапуск Listener и баз данных**
   Перезапустите Listener и убедитесь, что все службы работают корректно:
   
   .. code-block:: bash
   
      lsnrctl stop
      lsnrctl start

   Или обновите конфигурацию без перезапуска:
   
   .. code-block:: bash
   
      lsnrctl reload

3. **Просмотр журналов ошибок**
   Просмотреть журналы Oracle для выявления ошибок, связанных с Heterogeneous Services или DG4ODBC. Журналы обычно находятся в директории ``$ORACLE_HOME/hs/log/``.

   Интерпретация логов:
   - Логи содержат информацию о подключении, запросах и ошибках.
   - Пример типичных ошибок:

     - ``ORA-28545``: Ошибка подключения между Oracle и внешней системой. Проверьте конфигурацию DG4ODBC.
     - ``ORA-12541``: Listener не найден. Убедитесь, что Listener запущен и настроен правильно.

4. **Включение отладки**
   Измените параметр ``HS_FDS_TRACE_LEVEL`` в файле ``init<dg4odbc>.ora`` на ``DEBUG``:
   
   .. code-block:: ini
   
      HS_FDS_TRACE_LEVEL = DEBUG

5. **Связь с поддержкой**
   Если все вышеперечисленное не помогло, обратитесь в службу поддержки Oracle или PostgreSQL за помощью.

3.	Получение данных из базы данных PostgreSQL в Microsoft Excel или Access
-------------------------------------------------------------------------------
Чтобы быстро получить данные из базы данных PostgreSQL в Microsoft Excel или Access, можно использовать ODBC (Open Database Connectivity).

Для этого необходимо выполнить подготовительные действия:

1.	Установите ODBC-драйвер для PostgreSQL
2.	Настройте ODBC DSN

Подробности указаны в разделе: Установка PostgreSQL ODBC драйвера `:ref:`installing_odbc_driver` `

.. _microsoft_excel_import:

3.1.	Получение данных в Microsoft Excel
+++++++++++++++++++++++++++++++++++++++++++

1.	Открыть Microsoft Excel.

2.	Перейти на вкладку «Данные».

3.	Выбрать «Получить данные» -> «Из других источников» -> «Из ODBC».

4.	Выбрать DSN:

    В открывшемся окне выбрать настроенный ранее DSN для PostgreSQL и нажать «ОК».

5.	Ввести учетные данные:

    Введите имя пользователя и пароль для подключения к базе данных PostgreSQL.

6.	Выбрать таблицы и данные:

    После подключения появится окно «Навигатор» (Navigator), где можно выбрать нужные таблицы и данные.

7.	Загрузить данные:

    Нажать «Загрузить», чтобы импортировать выбранные данные в Excel.

.. _access_data_import:

3.2 Получение данных в Microsoft Access
++++++++++++++++++++++++++++++++++++++++

1. Открыть Microsoft Access.

2. Создать новую базу данных или открыть существующую.

3. Импорт данных:
   
   a. Перейти на вкладку «Внешние данные».
   
   b. Нажать «Создать источник данных» -> «Из других источников» -> «Из ODBC».

4. Выбрать источник данных:
   В открывшемся диалоговом окне выбрать «Импортировать таблицы в текущую базу данных» или «Связать источник данных, создавая связную таблицу».
   Нажать «ОК».

   Объяснение разницы между импортированием и созданием связанных таблиц:
   
   - **Импортирование таблиц**: Данные копируются из внешней базы данных (PostgreSQL) в локальную базу данных Access. После импорта изменения в исходной базе данных не будут отражаться в Access.
   
   - **Создание связанных таблиц**: Создается ссылка на внешнюю базу данных (PostgreSQL). Все изменения в исходной базе данных автоматически отображаются в Access.

5. Выбрать DSN:
   В открывшемся окне «Выбор источника данных» выбрать настроенный ранее DSN для PostgreSQL и нажать «ОК».

6. Ввести учетные данные:
   Ввести имя пользователя и пароль для подключения к базе данных PostgreSQL.

7. Выбрать таблицы:
   В диалоговом окне «Импорт объектов» выбрать необходимые таблицы и нажать «ОК».

.. _power_query_excel:

3.3 Получение данных используя Power Query в Excel
+++++++++++++++++++++++++++++++++++++++++++++++++++

Power Query — мощный инструмент для импорта и трансформации данных в Excel. Можно использовать его для подключения к PostgreSQL через ODBC.

Создание и настройка файла с расширением .dqy для подключения к базе данных PostgreSQL и выполнения SQL-запроса включает несколько шагов.

.. _creating_dqy_file:

1. Создание файла с расширением .dqy:
   
   a. Открыть текстовый редактор (например, Notepad, Notepad++, Visual Studio Code и т.п.).
   
   b. Создать новый пустой файл.

2. Запись необходимых данных в файл:
   Вставить следующую информацию в файл, заменив ``<user>`` и ``<password>`` на соответствующие значения:

   .. code-block:: text
   
      XLODBC
      1
      DRIVER={PostgreSQL Unicode};DATABASE=demo;SERVER=localhost;PORT=5432;UID=postgres;PASSWORD=<password>;SSLmode=disable;ReadOnly=0;Protocol=7.4;FakeOidIndex=0;ShowOidColumn=0;RowVersioning=0;ShowSystemTables=0;ConnSettings=;Fetch=100;Socket=4096;UnknownSizes=0;MaxVarcharSize=255;MaxLongVarcharSize=8190;Debug=0;CommLog=0;Optimizer=0;Ksqo=1;UseDeclareFetch=0;TextAsLongVarchar=1;UnknownsAsLongVarchar=0;BoolsAsChar=1;Parse=0;CancelAsFreeStmt=0;ExtraSysTablePrefixes=dd_;LFConversion=1;UpdatableCursors=1;DisallowPremature=0;TrueIsMinus1=0;BI=0;ByteaAsLongVarBinary=0;UseServerSidePrepare=0;LowerCaseIdentifier=0;GssAuthUseGSS=0;XaOpt=1
      select * from aircrafts

Всего должно получиться 4 строки, запрос - в последней.

DRIVER= Эта строка подключения содержит множество параметров, которые можно настроить в зависимости от потребностей и конфигурации базы данных:
 
   Объяснение параметров строки подключения:

   - ``DRIVER={PostgreSQL Unicode}``: Указывает драйвер ODBC, который используется для подключения. В данном случае это драйвер для PostgreSQL с поддержкой Unicode.
   - ``DATABASE=demo``: Указывает имя базы данных, к которой выполняется подключение. В данном случае это база данных "demo".
   - ``SERVER=localhost``: Указывает имя хоста или IP-адрес сервера базы данных. "localhost" означает, что сервер базы данных работает на локальном компьютере.
   - ``PORT=5432``: Указывает порт, который используется для подключения к серверу базы данных. По умолчанию PostgreSQL использует порт 5432.
   - ``UID=postgres``: Указывает имя пользователя (User ID), под которым происходит подключение к базе данных. В данном случае это "postgres".
   - ``PASSWORD=<password>``: Указывает пароль для пользователя, указанного в UID.
   - ``SSLmode=disable``: Указывает режим SSL для подключения. "disable" означает, что SSL не используется.
   - ``MaxVarcharSize=255``: Указывает максимальный размер для столбцов типа VARCHAR.
   - ``MaxLongVarcharSize=8190``: Указывает максимальный размер для столбцов типа LONGVARCHAR.
   - ``DRIVER={PostgreSQL Unicode}``: Указывает драйвер ODBC, который используется для подключения. В данном случае это драйвер для PostgreSQL с поддержкой Unicode.
   - ``DATABASE=demo``: Указывает имя базы данных, к которой выполняется подключение. В данном случае это база данных "demo".
   - ``SERVER=Localhost``: Указывает имя хоста или IP-адрес сервера базы данных. "Localhost" означает, что сервер базы данных работает на локальном компьютере.
   - ``PORT=5432``: Указывает порт, который используется для подключения к серверу базы данных. По умолчанию PostgreSQL использует порт 5432.
   - ``UID=postgres``: Указывает имя пользователя (User ID), под которым происходит подключение к базе данных. В данном случае это "postgres".
   - ``PASSWORD=<password>``: Указывает пароль для пользователя, указанного в UID.
   - ``SSLmode=disable``: Указывает режим SSL для подключения. "disable" означает, что SSL не используется.
   - ``ReadOnly=0``: Указывает, будет ли подключение только для чтения. 0 (ноль) означает, что подключение не только для чтения.
   - ``Protocol=7.4``: Указывает версию протокола PostgreSQL, которая будет использоваться.
   - ``FakeOidIndex=0``: Этот параметр определяет, будет ли драйвер создавать фиктивный OID индекс. 0 означает, что он не будет создан.
   - ``ShowOidColumn=0``: Указывает, будет ли отображаться колонка OID. 0 означает, что она не будет отображаться.
   - ``RowVersioning=0``: Указывает, используется ли управление версиями строк. 0 означает, что оно не используется.
   - ``ShowSystemTables=0``: Указывает, будут ли отображаться системные таблицы. 0 означает, что они не будут отображаться.
   - ``ConnSettings=``: Дополнительные настройки подключения. В данном случае они не указаны.
   - ``Fetch=100``: Указывает количество строк, которые будут извлекаться за один раз.
   - ``Socket=4096``: Указывает размер сокета в байтах.
   - ``UnknownSizes=0``: Указывает, как обрабатывать столбцы с неизвестными размерами. 0 означает, что они будут обрабатываться как есть.
   - ``MaxVarcharSize=255``: Указывает максимальный размер для столбцов типа VARCHAR.
   - ``MaxLongVarcharSize=8190``: Указывает максимальный размер для столбцов типа LONGVARCHAR.
   - ``Debug=0``: Указывает, будет ли включен режим отладки. 0 означает, что он не включен.
   - ``CommLog=0``: Указывает, будет ли включен журнал коммуникаций. 0 означает, что он не включен.
   - ``Optimizer=0``: Указывает, будет ли использоваться оптимизатор. 0 означает, что он не будет использоваться.
   - ``Ksqo=1``: Указывает, будет ли использоваться ключевой запрос оптимизатора. 1 означает, что он будет использоваться.
   - ``UseDeclareFetch=0``: Указывает, будет ли использоваться DECLARE и FETCH для извлечения данных. 0 означает, что они не будут использоваться.
   - ``TextAsLongVarchar=1``: Указывает, будут ли столбцы типа TEXT обрабатываться как LONGVARCHAR. 1 означает, что будут.
   - ``UnknownsAsLongVarchar=0``: Указывает, будут ли неизвестные типы обрабатываться как LONGVARCHAR. 0 означает, что не будут.
   - ``BoolsAsChar=1``: Указывает, будут ли булевые значения обрабатываться как CHAR. 1 означает, что будут.
   - ``Parse=0``: Указывает, будет ли драйвер анализировать SQL-запросы. 0 означает, что не будет.
   - ``CancelAsFreeStmt=0``: Указывает, будет ли CANCEL обрабатываться как FreeStmt. 0 означает, что не будет.
   - ``ExtraSysTablePrefixes=dd_``: Указывает дополнительные префиксы для системных таблиц.
   - ``LFConversion=1``: Указывает, будет ли производиться конвертация строк конца строки. 1 означает, что будет.
   - ``UpdatableCursors=1``: Указывает, будут ли курсоры обновляемыми. 1 означает, что будут.
   - ``DisallowPremature=0``: Указывает, будет ли запрещен преждевременный доступ к данным. 0 означает, что не будет.
   - ``TrueIsMinus1=0``: Указывает, будет ли TRUE представляться как -1. 0 означает, что не будет.
   - ``BI=0``: Параметр, возможно, означает использование метаданных для идентификации столбцов. 0 означает, что не используется.
   - ``ByteaAsLongVarBinary=0``: Указывает, будут ли столбцы типа BYTEA обрабатываться как LONGVARBINARY. 0 означает, что не будут.
   - ``UseServerSidePrepare=0``: Указывает, будет ли использоваться подготовка на стороне сервера. 0 означает, что не будет.
   - ``LowerCaseIdentifier=0``: Указывает, будут ли идентификаторы преобразованы в нижний регистр. 0 означает, что не будут.
   - ``GssAuthUseGSS=0``: Указывает, будет ли использоваться GSS-авторизация. 0 означает, что не будет.
   - ``XaOpt=1``: Указывает опции для XA (расширенной архитектуры транзакций). 1 означает, что опции включены.

Перед выполнением запроса проверить данные, замену DATABASE, <user> на имя пользователя базы данных PostgreSQL и <password>,  на соответствующий пароль.

3. Сохранение файла:
   
Сохранить файл с расширением ``.dqy``.

Убедитесь, что в процессе сохранения выбрано правильное расширение ``.dqy``, а не ``.txt`` или другое.

4. Открыть файл

После открытия файла, будет выполнен запрос.

.. note::
   Проверьте, что все настройки ODBC и учётные данные правильны, чтобы избежать проблем с подключением.