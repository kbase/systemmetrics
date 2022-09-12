FROM python:3.10.7-slim

# Build arguments passed into the docker command for image metadata
ARG BUILD_DATE
ARG COMMIT
ARG BRANCH

RUN apt-get update -y && \
    apt-get install -y wget && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install requests

COPY bin /root/bin
RUN cd /root/bin && wget https://github.com/kbase/dockerize/raw/master/dockerize-linux-amd64-v0.6.1.tar.gz && \
    tar xzf dockerize-linux-amd64-v0.6.1.tar.gz && \
    rm dockerize-linux-amd64-v0.6.1.tar.gz 

COPY source /root/source
WORKDIR /root/source

# The *.egg directories in /kb/runtime/lib/python3.7/site-packages didn't come
# through the installer, so they aren't automatically added to sys.path. Put a
# modified version of the narrative containers easy-install.pth file into the
# the default search path so that the eggs are picked up by this container's
# python interpreter

ENV PATH="/root/bin:/root/source:${PATH}"

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.vcs-url="https://github.com/kbase/SystemMetrics" \
      org.label-schema.vcs-ref=$COMMIT \
      org.label-schema.schema-version="1.0.0-rc1" \
      us.kbase.vcs-branch=$BRANCH  \
      maintainer="Steve Chan sychan@lbl.gov"

ENTRYPOINT [ "/bin/bash" ] 