FROM python:2.7
MAINTAINER Captain Dao <support@daocloud.io>

RUN mkdir -p /app
WORKDIR /app

RUN pip install web.py

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
COPY code.py /usr/local/bin/code.py



RUN chmod +x /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/code.py

EXPOSE 8080
ENTRYPOINT ["docker-entrypoint.sh"]
CMD [""]
