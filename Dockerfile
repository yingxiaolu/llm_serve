FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# COPY  dist/chatgpt_serve-1.1.2-py3-none-any.whl /app/chatgpt_serve-1.1.2-py3-none-any.whl

# RUN pip install -U pip && pip install chatgpt_serve-1.1.2-py3-none-any.whl

# RUN rm -rfv /app/chatgpt_serve-1.1.2-py3-none-any.whl
