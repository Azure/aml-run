FROM marvinbuss/aml-docker:latest

LABEL "com.github.actions.name"="Azure Machine Learning Run"
LABEL "com.github.actions.description"="Submit a run to an Azure Machine Learning Workspace with this GitHub Action"
LABEL "com.github.actions.icon"="arrow-up-right"
LABEL "com.github.actions.color"="gray-dark"

LABEL version="1.0.0"
LABEL repository="https://github.com/Azure/aml-run"
LABEL homepage="https://github.com/Azure/aml-run"
LABEL maintainer=""

COPY /code /code
ENTRYPOINT ["/code/entrypoint.sh"]