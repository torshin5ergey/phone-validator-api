# Phone Validator API

## References

- [Задачи квалификации чемпионата по програм­мированию 2019 среди бэкенд-разработчиков. G Сервис валидации телефонных номеров](https://yandex.ru/cup/backend/analysis#)
- [Quickstart — Flask Documentation (3.1.x)](https://flask.palletsprojects.com/en/stable/quickstart/)
- [Faker Documentation](https://faker.readthedocs.io/en/stable/index.html#)

## Run with Python

1. Install requirements
```bash
pip install -r requirements
```
2. Run app
```bash
python3 app.py
```

## Run with Docker

1. Create image
```bash
docker build -t validate-phone-number-api .
```
2. Run container
```bash
docker run -p 7777:7777 -d --rm validate-phone-number-api
```

## Usage

When run in container

- Ping
```bash
curl localhost:7777/ping
```

- Shutdown
```bash
curl localhost:7777/shutdown
```

- Validate phone number
```bash
curl -X POST http://localhost:7777/validatePhoneNumber \
-H "Content-Type: application/json" \
-d '{"phone_number": "+7 912 123 4567"}'
# output
{"normalized":"+7-912-123-4567","status":true}
```

- Invalid phone
```bash
curl -X POST http://localhost:7777/validatePhoneNumber \
-H "Content-Type: application/json" \
-d '{"phone_number": "+7 913 123 4567"}' \
-w "Response code: %{http_code}\n"
# output
Response code: 404
```

- Invalid request
```bash
curl -X POST http://localhost:7777/validatePhoneNumber \
-H "Content-Type: application/json" \
-d '{"phone": "+7 912 123 4567"}' \
-w "Response code: %{http_code}\n"
# output
Response code: 400
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
