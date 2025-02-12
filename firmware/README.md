# Протокол межуровнего общения

Общение происходит по Serial порту при BOD = 500000

Со стророны верхнего уровня посылаются запросы вида:
    "<сommand>{data}" в виде ASCII строки

    Содержимое распологается с разделителем 
    (при необходимости), для уменьшения размера сообщений,
    чтобы не терять структуру, каждая ведичина имеет 
    фиксированный размер и степень необходимости, 
    поэтому если 

    Поддерживаемые команды и примеры (для MagLev System):

        1) Передача параметров настройки и начало их выполнения
            Request:
                text: "<command><signal><freq><amp><origin>"
                    //Без пробелов, чтобы парсить было проще (request[i])

                Поле     : макрос       = значение  | тип
                ------------------------------------------
                command  : SET          = 0         | char
                ------------------------------------------
                signal   : TRIANGULAR   = 0         | unsigned char
                         : SINE         = 1         |
                         : SAWLIKE      = 2         |
                         : SQUARE       = 3         |  
                ------------------------------------------
                freq     :              = frequacy  | 3 unsigned char //от 0 до 50 Hz 
                ------------------------------------------
                amp      :              = amplitude | 3 unsigned char //от 0 до 150 mm 
                ------------------------------------------
                origin   :              = origin    | 3 unsigned char //от 0 до 150 mm

                Example: "01005050075" == <SET><SINE><5Hz><50mm><75mm>

            Answer:
                Без ответа
            

        2) Запуск отсчёта времени
            Request:
                text: "<command>"

                Поле     : макрос       = значение  | тип
                ------------------------------------------
                command  : START        = 1         | char

                Example: "1" == <START>

            Answer:
                Без ответа


        3) Приостановить отсчёт времени
            Request:
                text: "<command>"

                Поле     : макрос       = значение  | тип
                ------------------------------------------
                command  : STOP         = 2         | char

            Answer:
                Без ответа


        3) Сбросить отсчёт времени в ноль
            Request:
                text: "<command>"

                Поле     : макрос       = значение  | тип
                ------------------------------------------
                command  : DROP         = 3         | char

            Answer:
                Без ответа


        3) Запрос на получение данных
            Request:
                text: "<command>"

                Поле     : макрос       = значение  | тип
                ------------------------------------------
                command  : GET          = 4         | char

            Answer: 
                text: "<time> <idle_pos> <real_pos>" 
                    //пробелы для упрощения парсинга питоном

                Поле     : макрос       = значение  | тип
                ------------------------------------------
                time     :             = time       | size_t
                idle_pos :             = idle_pos   | unsigned char
                real_pos :             = real_pos   | unsigned char

                Example: "3000 75 64"

