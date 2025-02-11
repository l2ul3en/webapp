FROM registry.redhat.io/ubi9/python-312

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt
RUN pip install --upgrade pip

COPY ./ .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080", "--settings=config.settings.development"]
