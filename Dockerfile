FROM marvinbuss/aml-docker:latest

LABEL maintainer="marvinbuss"

COPY /code .
ENTRYPOINT ["/entrypoint.sh"]
