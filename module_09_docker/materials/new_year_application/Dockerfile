FROM python:3.7.9-slim-stretch

COPY requirements.txt /new_year_app/

RUN python -m pip install -r /new_year_app/requirements.txt

COPY . /new_year_app/

WORKDIR /new_year_app

ENTRYPOINT ["python", "app.py"]