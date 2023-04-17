# Mareety Bot

Название - testbot, можете сменить на любое другое

### Запускаем первый раз
1. Вытаскиваем тексты из файлов (он сам находит)

`pybabel extract . -o locales/testbot.pot`

2. Создаем папку для перевода на английский

`pybabel init -i locales/testbot.pot -d locales -D testbot -l en`

3. То же, на русский

`pybabel init -i locales/testbot.pot -d locales -D testbot -l ru`

4. То же, на узбекский

`pybabel init -i locales/testbot.pot -d locales -D testbot -l uz`

5. Переводим, а потом собираем переводы

`pybabel compile -d locales -D testbot`


### Обновляем переводы
1. Вытаскиваем тексты из файлов, Добавляем текст в переведенные версии

`pybabel extract . -o locales/testbot.pot`

`pybabel update -d locales -D testbot -i locales/testbot.pot`

3. Вручную делаем переводы, а потом Собираем

`pybabel compile -d locales -D testbot`

