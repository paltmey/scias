FROM victorhcm/opencv:3.2.0-python2.7

COPY requirements.txt /ApplicationServer/
RUN pip install --requirement /ApplicationServer/requirements.txt

RUN python -m spacy download en_core_web_md

COPY descriptors /ApplicationServer/descriptors
WORKDIR /ApplicationServer/descriptors
RUN python setup_cython.py build_ext --inplace

RUN mkdir -p /data/uploads /data/images /data/videos

COPY . /ApplicationServer/

WORKDIR /ApplicationServer
ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]

EXPOSE 8000
