FROM python:3.7

EXPOSE 5000

WORKDIR /readDB

COPY requirements.txt /readDB
RUN pip install -r requirements.txt

COPY input.txt /readDB

COPY readDB.py /readDB
CMD python readDB.py
