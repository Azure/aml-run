FROM marvinbuss/aml-docker:1.10.0-alpine

LABEL maintainer="azure/gh-aml"

COPY /code /code
ENTRYPOINT ["/code/entrypoint.sh"]
