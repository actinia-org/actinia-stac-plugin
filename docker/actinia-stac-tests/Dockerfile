# Exception for hadolint-docker-linter:
# DL3007: using latest is prone to errors if the image will ever update. Pin the version explicitly to a release tag
# hadolint ignore=DL3007
FROM mundialis/actinia-core:latest AS actinia_test

LABEL authors="Carmen Tawalika,Anika Weinmann"
LABEL maintainer="tawalika@mundialis.de,weinmann@mundialis.de"

ENV ACTINIA_CUSTOM_TEST_CFG /etc/default/actinia_stac_test
# TODO do not set DEFAULT_CONFIG_PATH if this is fixed
ENV DEFAULT_CONFIG_PATH /etc/default/actinia_stac_test

# install things only for tests
# DL3013 # Pin versions in pip
# DL3018: Pin versions in apk add
# hadolint ignore=DL3013,DL3018
RUN apk add --no-cache valkey valkey-cli && \
    pip3 install --no-cache-dir iniconfig colorlog pwgen pytest pytest-cov

# copy needed files and configs for test
COPY docker/actinia-stac-tests/actinia-stac-test.cfg /etc/default/actinia_stac_test

COPY . /src/actinia-stac-plugin/
WORKDIR /src/actinia-stac-plugin/
RUN chmod a+x tests_with_kvdb.sh

RUN pip install .

RUN make test
