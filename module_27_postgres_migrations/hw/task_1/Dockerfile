FROM python:3.12-slim
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app
RUN pip install -r requirements.txt
ADD . /app
EXPOSE 5000
ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app", "--timeout 120"]