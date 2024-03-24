# Wanderlust
## _Ваш проводник в мир незабываемых путешествий!_

Сслыка: [@wanderlusterbot](https://t.me/wanderlusterbot)

## Описание
---

## Внешние интеграции
1. [geosuggest](https://yandex.ru/dev/geosuggest/doc/ru/) - Используется для проверки на то, существует ли место, которое ввел пользователь, а также для исправления ошибок в названии геолокации. 1000 бесплатных запросов в сутки

2. [geocoder](https://yandex.ru/dev/geocode/doc/ru/) - Используется для получения координат локации, по ее названию. 1000 бесплатных запросов в сутки

3. [openweathermap](https://openweathermap.org/api) - Используется для получения данных о погоде. 1000 бесплатных запросов в сутки

4. [opentripmap](https://dev.opentripmap.org/ru/product) - Используется для получения данных о достопримечательностях места, по его координатам. 5000 бесплатных запросов в сутки.

5. [graphhopper](https://graphhopper.com/maps/) - Отрисовка маршрута путешествия. OpenSource инструмент
---
## Варианты запуска
### 1. Docker
```bash
git clone https://github.com/Central-University-IT-prod/backend-DRAKUTONT.git

cd backend-DRAKUTONT

docker-compose up
```
### 2. Обычная установка
```bash
git clone https://github.com/Central-University-IT-prod/backend-DRAKUTONT.git

cd backend-DRAKUTONT

pip install -r requirements.txt

python main.py
```
#### Файл конфигурации
Скопируйте файл `.env.template`, переименуйте его в `.env` и подставьте необходимые значения

```bash
BOT_TOKEN=
SUGGEST_API_KEY=
GEOCODER_API_KEY=
OPENWEATHER_API_KEY=
OPENTRIPMAP_API_KEY=
```
## СУБД
![Схема базы данных](ER.png)
