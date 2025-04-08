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
RUN apk add --no-cache redis==7.2.7-r0
RUN pip3 install --no-cache-dir iniconfig==2.0.0 colorlog==6.8.2 pwgen==0.8.2 pytest==8.3.5 pytest-cov==6.0.0

# uninstall actinia core from FROM-image
#RUN pip3 uninstall actinia-core -y

COPY docker/actinia-stac-tests/start.sh /src/start.sh

ENTRYPOINT ["/bin/sh"]
CMD ["/src/start.sh"]

# copy needed files and configs for test
COPY docker/actinia-stac-tests/actinia-stac-test.cfg /etc/default/actinia_stac_test
COPY . /src/actinia-stac-plugin/

WORKDIR /src/actinia-stac-plugin/

RUN chmod a+x tests_with_redis.sh

RUN make install

RUN make test
