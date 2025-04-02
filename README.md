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
3. Use app (example)
```bash
curl localhost:7777
# return
hello world
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
