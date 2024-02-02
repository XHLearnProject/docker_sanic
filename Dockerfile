FROM sanicframework/sanic:3.11-latest

WORKDIR /sanic

COPY . .

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

EXPOSE 16471

CMD ["python", "main.py"]
