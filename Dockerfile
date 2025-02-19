FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNDUFFERED 1

RUN pip install --upgrade pip

# Устанавливаем необходимые пакеты
RUN apk update && apk add --no-cache gcc musl-dev postgresql-dev

RUN adduser -D user

WORKDIR /app

# Переключаемся на созданного пользователя
RUN mkdir /app/staticfiles && chown -R user:user /app && chmod -R 755 /app

COPY --chown=user:user . .

RUN pip install -r requirements.txt

USER user

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app.wsgi:application"]