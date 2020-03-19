FROM marvinbuss/aml-docker:latest

LABEL maintainer="marvinbuss"

COPY /code /code
ENTRYPOINT ["/code/entrypoint.sh"]