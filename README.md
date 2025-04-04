# Phone Validator API

## References

- [Quickstart — Flask Documentation (3.1.x)](https://flask.palletsprojects.com/en/stable/quickstart/)
- [Задачи квалификации чемпионата по програм­мированию 2019 среди бэкенд-разработчиков. G Сервис валидации телефонных номеров](https://yandex.ru/cup/backend/analysis#)

## App

1. Install requirements
```bash
pip install -r requirements
```
2. Run app
```bash
python3 app.py
```
3. Use app
```bash
# ping
curl localhost:7777/ping

# shutdown
curl localhost:7777/shutdown

# validatePhoneNumber
# valid phone
curl -X POST -d "+7 982 123 4567" http://localhost:7777/validatePhoneNumber
# invalid phone
curl -X POST -d "12345" http://localhost:7777/validatePhoneNumber
```

## Run with Docker

1. Create image
```bash
docker build -t phone-validator-api .
```
2. Run container
```bash
docker run -p 7777:7777 -d phone-validator-api
```
3. Use app
```bash
# ping
curl localhost:7777/ping

# shutdown
curl localhost:7777/shutdown

# validatePhoneNumber
# valid phone
curl -X POST -d "+7 982 123 4567" http://localhost:7777/validatePhoneNumber
# invalid phone
curl -X POST -d "12345" http://localhost:7777/validatePhoneNumber
```

## Tests

Run tests
```bash
# simple run
pytest -v

# run with test cover report
pytest -v --cov=app

# run with test cover report in html
# htmlcov directory
pytest -v -cov=app --cov-report=html
```

## Author

Sergey Torshin [@torshin5ergey](https://github.com/torshin5ergey)
