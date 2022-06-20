FROM python:3.10-slim-bullseye

LABEL maintainer="siriusbrightstar@protonmail.com"
LABEL author="SiriusBrightstar"
LABEL github="https://github.com/SiriusBrightstar"
LABEL project="F1 Events Bot"

COPY src/main.py /src/
COPY src/auth.py /src/
COPY src/requirments.txt /src/

RUN pip3 install -r /src/requirments.txt

WORKDIR /src

CMD ["python3", "main.py"]