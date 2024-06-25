# Инструкции по запуску микросервиса
### 0. Общие инструкции
- Для корректной работы сервиса в Docker-контейнере необходимо создать файл .env в директории mle-project-sprint-3-v001/services со следующим содержимым:
```
AUTHOR=...
# автор контейнера (можно вписать, например, свое имя)
MODEL_PATH="../models/model.pkl"
# путь до модели
APP_PORT=8081
# значение порта fastapi сервиса (можно вписать любой другой свободный порт)
PROM_PORT=9090
# значение порта prometheus сервиса (можно вписать любой другой свободный порт)
GRAF_PORT=3000
# значение порта grafana сервиса (можно вписать любой другой свободный порт)
GRAFANA_USER=...
GRAFANA_PASS=...
# имя пользователя и пароль для сервиса grafana (нужно задать свои значения для этих двух переменных)
```
- Если не менять предложенные выше порты, тогда:
 http://localhost:8081/ - адрес FastAPI микросервиса
 http://localhost:9090/ - адрес Prometheus микросервиса
 http://localhost:3000/ - адрес Grafana микросервиса
- Пример валидного запроса для любого способа запуска сервиса:
```
curl -X 'POST' \
  'http://127.0.0.1:8081/api/price/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
"floor": 11,
"is_apartment": false,
"kitchen_area": 10.0,
"living_area": 46.0,
"rooms": 3,
"studio": false,
"total_area": 75.0,
"build_year": 2008,
"building_type_int": 4,
"latitude": 55.87521743774414,
"longitude": 37.59069442749024,
"ceiling_height": 2.700000047683716,
"flats_count": 315,
"floors_total": 25,
"has_elevator": true
}'
```
### 1. FastAPI микросервис в виртуальном окружение
- Переходим в папку c cервисом: 
```
cd mle-project-sprint-3-v001/services
```
- Создаем виртуальное окружение:
```
python3.10 -m venv ./venv_fastapi
```
- Активируем вирутальное окружение: 
```
source ./venv_fastapi/bin/activate
```
- Устанавиваем все необходимые библиотеки:
```
pip install -r requirements.txt
```
- Переходим в папку с микросервисом и запускаем FastAPI микросервис с помощью uvicorn:
```
cd ml_service && uvicorn price_app:app --reload --port 8081 --host 0.0.0.0
```

### 2.1. FastAPI микросервис в Docker-контейнере без использования Docker Compose
- Переходим в папку c cервисом: 
```
cd mle-project-sprint-3-v001/services
```
-  Собираем образ из файла Dockerfile_ml_service:
```
docker image build . --file Dockerfile_ml_service --tag fastapi
```
- Запускаем контейнер из образа fastapi, собранного на предыдущем шаге:
```
docker container run --publish 8081:8081 --env-file .env --volume=./models:/models fastapi
```
### 2.2. FastAPI микросервис в Docker-контейнере c использованием Docker Compose
- Переходим в папку c cервисом: 
```
cd mle-project-sprint-3-v001/services
```
- Собираем образ и запускаем контейнер с помощью docker сompose:
```
docker compose up  --build
```
### 3. Запуск FastAPI микросервиса вместе с системой мониторинга Prometheus и Grafana
- Переходим в папку c cервисом: 
```
cd mle-project-sprint-3-v001/services
```
- Собираем образ и запускаем контейнер с помощью docker сompose:
```
docker compose up  --build
```
### 4. Построение дашборда для мониторинга: симуляция нагрузки на сервис
- Переходим в папку c проектом: 
```
cd mle-project-sprint-3-v001
```
- Запускаем скрипт для симуляции нагрузки на сервис:
```
python generate_requests.py
```
