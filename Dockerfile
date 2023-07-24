FROM python:3.7

COPY . /app
WORKDIR /app
RUN pip3 install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 5000

ENTRYPOINT ["gunicorn", "--config", "./gunicorn_cfg.py", "app:app"]
