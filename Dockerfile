FROM public.ecr.aws/docker/library/python:3.12-alpine

COPY requirements.txt /

RUN pip install --break-system-packages -r /requirements.txt

COPY entrypoint.py /
ENTRYPOINT ["/entrypoint.py"]
