# BeeWise_test
## Тестовое задание для компании BeeWise.
Разработанный скрипт предлагает пользователю произвести с файлом с расшифровкой диалогов следующие действия, вводя соответствующие цифры на клавиатуре: 
```
[1] Извлечь реплики с приветствием
[2] Извлечь реплики, где менеджер представил себя, и имя менеджера 
[3] Извлечь название компании
[4] Извлечь реплики, где менеджер попрощался
[5] Проверить требование к менеджеру: «В каждом диалоге обязательно необходимо поздороваться и попрощаться с клиентом»
[6] Сохранить файл с флагами
```
Скрипт написан с использованием библиотеки Pandas, извлечении именованных сущностей (имен менеджеров) выполняется с помощью SpaCy (ru_core_news_md)

Особенности:
- Сохранить файл с флагами можно только после выполнения действий 1-5 в произвольном порядке.
- Файл с данными должен лежать в одной папке со скриптом.
