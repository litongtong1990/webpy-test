FROM daocloud.io/python:2.7
MAINTAINER Captain Dao <support@daocloud.io>

RUN mkdir -p /app
WORKDIR /app

RUN pip install web.py

COPY code.py /app/code.py
RUN chmod +x /app/code.py


EXPOSE 8080

CMD ["python","/app/code.py"]