FROM jupyter/pyspark-notebook:latest
COPY dist /tmp/
RUN pip install /tmp/datapipeline_konfio-0.1-py3-none-any.whl
RUN pip install requests
