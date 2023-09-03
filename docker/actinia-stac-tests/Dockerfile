FROM mundialis/actinia-core:latest as actinia_test

LABEL authors="Carmen Tawalika,Anika Weinmann"
LABEL maintainer="tawalika@mundialis.de,weinmann@mundialis.de"

ENV ACTINIA_CUSTOM_TEST_CFG /etc/default/actinia_stac_test

# TODO do not set DEFAULT_CONFIG_PATH if this is fixed
ENV DEFAULT_CONFIG_PATH /etc/default/actinia_stac_test

# install things only for tests
RUN apk add redis
RUN pip3 install iniconfig colorlog

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
