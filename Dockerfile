FROM jupyter/pyspark-notebook:latest
COPY dist /tmp/
RUN pip install /tmp/tools_datapipeline_3b-0.1-py3-none-any.whl
RUN pip install requests
RUN pip install beautifulsoup4
RUN pip install lxml
RUN pip install delta-spark==2.4.0

