FROM alpine:3.8
RUN apk add python3 py-pip && python3 -m ensurepip && pip install --upgrade pip && pip install flask
COPY templates /app
WORKDIR /app
COPY . /app/
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app.py"]