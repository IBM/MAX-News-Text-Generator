FROM continuumio/miniconda3

RUN mkdir -p /workspace/data

RUN wget -nv http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/lm_1b/data.tar.gz && mv data.tar.gz /workspace/data/
RUN tar -x -C /workspace/ -f /workspace/data/data.tar.gz -v && rm /workspace/data/data.tar.gz

# Python package versions
ARG numpy_version=1.14.1
ARG tf_version=1.5.0
ARG keras_version=2.1.4

RUN pip install --upgrade pip && \
	pip install numpy==${numpy_version} && \
    pip install tensorflow==${tf_version} && \
    pip install flask-restplus

# Copy local files last so we don't redo all the object storage downloads 
# and package installs every time we build the image.
COPY . /workspace

EXPOSE 5000

CMD cd workspace/ && python app.py
