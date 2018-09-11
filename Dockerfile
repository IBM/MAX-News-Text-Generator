FROM codait/max-base

RUN mkdir -p /workspace/data

RUN wget -nv --show-progress --progress=bar:force:noscroll http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/lm_1b/data.tar.gz && mv data.tar.gz /workspace/data/
RUN tar -x -C /workspace/ -f /workspace/data/data.tar.gz -v && rm /workspace/data/data.tar.gz

# Python package versions
ARG numpy_version=1.14.1
ARG tf_version=1.5.0

RUN pip install numpy==${numpy_version} && \
    pip install tensorflow==${tf_version}

COPY . /workspace

EXPOSE 5000

CMD python app.py
