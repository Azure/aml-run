FROM marvinbuss/aml-docker:1.1.5.1

LABEL maintainer="azure/gh-aml"

COPY /code /code
ENTRYPOINT ["/code/entrypoint.sh"]
