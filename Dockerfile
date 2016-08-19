FROM python:3.6
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /cookiecutters
COPY cookiecutters.txt /cookiecutters/cookiecutters.txt
RUN bash -c 'while read repo; do cd /cookiecutters && git clone "$repo"; done < /cookiecutters/cookiecutters.txt'

RUN groupadd -r cookie && useradd -m -d /home/cookie -g cookie cookie
RUN mkdir /app
RUN chown -R cookie.cookie /app
USER cookie
WORKDIR /app

COPY bakery.py /app/bakery.py