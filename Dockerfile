FROM python:3.10-alpine

ARG USER=docker
ARG UID=1000

RUN adduser \
    --disabled-password \
    --gecos "" \
    --ingroup "users" \
    --uid "$UID" \
    "$USER"

RUN apk add --no-cache build-base libffi-dev git 

RUN pip install --upgrade pip setuptools wheel

WORKDIR /app

COPY auto-generated-requirements.txt .

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache --mount=type=secret,id=pipconf,target=/root/.config/pip/pip.conf pip3 install --no-build-isolation -r requirements.txt

COPY . .

USER $USER

CMD ["uvicorn", "web:app", "--host", "0.0.0.0", "--port", "8080"]
