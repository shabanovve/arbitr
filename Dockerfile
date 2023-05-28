FROM python:3.10.9
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src /app/src
COPY start.py .
RUN mkdir share
ENV API_KEY=''
ENV API_SECRET=''
ENV ETHEREUM_ADDRESS=''
ENV PASS_PHRASE=''
ENV STARK_PRIVATE_KEY=''
ENV SYM_BYBIT=''
ENV SYM_DYDX=''
ENTRYPOINT ["python", "start.py"]