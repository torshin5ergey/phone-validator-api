# Validate Phone Number API

[![Docker Image Version](https://img.shields.io/docker/v/torshin5ergey/validate-phone-number-api)](https://hub.docker.com/r/torshin5ergey/validate-phone-number-api)
[![CI](https://github.com/torshin5ergey/validate-phone-number-api/actions/workflows/cicd.yaml/badge.svg)](https://github.com/torshin5ergey/validate-phone-number-api/actions)

Phone number validation API inspired by [Yandex Backend Developers Championship Qualification 2019 Challenge G](https://yandex.ru/cup/backend/analysis)

## References

- [Задачи квалификации чемпионата по програм­мированию 2019 среди бэкенд-разработчиков](https://yandex.ru/cup/backend/analysis)
- [Quickstart — Flask Documentation (3.1.x)](https://flask.palletsprojects.com/en/stable/quickstart/)
- [Faker Documentation](https://faker.readthedocs.io/en/stable/index.html#)
- [HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status#client_error_responses)

## Run with Python

1. Install requirements
```bash
pip install -r requirements.txt
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
2. Run container (build locally or pull from Docker Hub)
```bash
# Local Build
docker run -p 7777:7777 -d --rm validate-phone-number-api

# Pull from Docker Hub
docker run -p 7777:7777 -d --rm torshin5ergey/validate-phone-number-api
```

## Usage

Available endpoints:
- `GET /ping` - healthcheck
- `POST /validatePhoneNumber` - phone number validation
- `GET /shutdown` - stop service

### Examples

- Ping
```bash
curl localhost:7777/ping
```

- Shutdown
```bash
curl localhost:7777/shutdown
```

- Valid phone number
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

1. Install test dependencies
```bash
pip install -r requirements-dev.txt
```
2. Run tests
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
