FROM python:3.7

EXPOSE 8000

WORKDIR /fillDB

COPY requirements.txt /fillDB
RUN pip install -r requirements.txt

COPY gnomad.exomes.r2.1.1.sites.13.vcf /fillDB

COPY fillDB.py /fillDB
CMD python fillDB.py
