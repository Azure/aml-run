FROM marvinbuss/aml-docker:1.4.0

LABEL maintainer="azure/gh-aml"

RUN pip install pyyaml

COPY /code /code
ENTRYPOINT ["/code/entrypoint.sh"]
