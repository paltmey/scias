FROM tensorflow/tensorflow:latest

RUN mkdir -p /InferenceServer \
    && curl -SL https://github.com/tensorflow/models/archive/master.zip -o /tmp/models-master.zip \
    && unzip -q /tmp/models-master.zip -d /tmp \
    && mv -T /tmp/models-master /InferenceServer/tf_models \
    && rm /tmp/models-master.zip

RUN mkdir -p /InferenceServer/checkpoints \
    && curl -SL http://download.tensorflow.org/models/inception_v3_2016_08_28.tar.gz \
    | tar -xzC /InferenceServer/checkpoints

COPY requirements.txt /InferenceServer/
RUN pip install --requirement /InferenceServer/requirements.txt

COPY . /InferenceServer/

WORKDIR /InferenceServer
ENTRYPOINT ["gunicorn", "app", "--bind=0.0.0.0:8000", "--timeout=600"]

EXPOSE 8000
