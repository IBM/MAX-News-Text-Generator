FROM floydhub/dl-base:2.1.0-py3.22

RUN mkdir -p /workspace/data

RUN wget -nv http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/lm_1b/ckpt-base && mv ckpt-base /workspace/data/
RUN wget -nv http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/lm_1b/ckpt-char-embedding && mv ckpt-char-embedding /workspace/data/
RUN wget -nv http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/lm_1b/ckpt-lstm && mv ckpt-lstm /workspace/data/
RUN wget -nv http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/lm_1b/ckpt-softmax0 && mv ckpt-softmax0 /workspace/data/
RUN wget -nv http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/lm_1b/ckpt-softmax1 && mv ckpt-softmax1 /workspace/data/
RUN wget -nv http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/lm_1b/ckpt-softmax2 && mv ckpt-softmax2 /workspace/data/
RUN wget -nv http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/lm_1b/ckpt-softmax3 && mv ckpt-softmax3 /workspace/data/
RUN wget -nv http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/lm_1b/ckpt-softmax4 && mv ckpt-softmax4 /workspace/data/
RUN wget -nv http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/lm_1b/ckpt-softmax5 && mv ckpt-softmax5 /workspace/data/
RUN wget -nv http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/lm_1b/ckpt-softmax6 && mv ckpt-softmax6 /workspace/data/
RUN wget -nv http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/lm_1b/ckpt-softmax7 && mv ckpt-softmax7 /workspace/data/
RUN wget -nv http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/lm_1b/ckpt-softmax8 && mv ckpt-softmax8 /workspace/data/
RUN wget -nv http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/lm_1b/graph-2016-09-10.pbtxt && mv graph-2016-09-10.pbtxt /workspace/data/
RUN wget -nv http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/lm_1b/vocab-2016-09-10.txt && mv vocab-2016-09-10.txt /workspace/data/

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

RUN cd /workspace && \
    bazel build -c opt lm_1b/...

EXPOSE 5000

CMD cd workspace/ && python app.py
