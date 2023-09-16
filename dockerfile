FROM python:latest

ADD GUA-utilization-by-48s.py ./
ADD index-template.html ./

RUN pip install requests python-dotenv jinja2 boto3 numpy parse datetime awscli

CMD [ "python3", "./GUA-utilization-by-48s.py" ]