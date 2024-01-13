FROM ubuntu

WORKDIR /market-microservice

RUN apt-get update && apt-get install -y supervisor cron python3-pip
COPY crontab.txt /etc/cron.d/crontab
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY . .
ADD . /market-microservice


RUN pip install --no-cache-dir -r requirements.txt
RUN crontab /etc/cron.d/crontab
EXPOSE 50050 50051

CMD ["/usr/bin/supervisord"]