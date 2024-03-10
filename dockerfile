FROM python:3.11.8-alpine3.19
WORKDIR /app
COPY requirements.txt ./

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps


COPY . .
EXPOSE 5001

ENV FLASK_APP=main.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]