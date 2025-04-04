# Пример работы с `Docker`

Для сборки образа:

> docker build -t our_first_image .

для запуска контейнера

> docker run --rm -p 8990:8989 --name our_first_container our_first_image