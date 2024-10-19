FROM python:3.10

WORKDIR /curl_to_requests

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5100

CMD ["flask", "--app", "curl_to_requests", "run", "-h", "0.0.0.0", "-p", "5100"]