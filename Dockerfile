FROM ghcr.io/marvinbuss/aml-docker:1.32.0

LABEL maintainer="azure/gh-aml"

COPY /code /code
ENTRYPOINT ["/code/entrypoint.sh"]
