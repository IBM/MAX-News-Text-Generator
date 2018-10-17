FROM codait/max-base

RUN mkdir -p /workspace/data

RUN wget -nv --show-progress --progress=bar:force:noscroll http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/lm_1b/data.tar.gz && mv data.tar.gz /workspace/data/
RUN tar -x -C /workspace/ -f /workspace/data/data.tar.gz -v && rm /workspace/data/data.tar.gz

COPY requirements.txt /workspace
RUN pip install -r requirements.txt

COPY . /workspace
RUN md5sum -c md5sums.txt # check file integrity

EXPOSE 5000

CMD python app.py
