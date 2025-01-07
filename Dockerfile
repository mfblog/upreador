FROM docker.io/library/python:3
WORKDIR /root/
COPY . .
VOLUME [ "/root/data" ]
RUN pip install --no-cache-dir  -r requirements.txt 
CMD [ "python", "./booksource.py" ]




