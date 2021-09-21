### Only kept for reference - currently travis takes care of building the wheel

To create a new release, you can use this docker to build the wheel and add
to the release.

The `docker build` command builds the wheel and integrated the build-args for
the github release.

The `docker run` command creates the build and uploads the
previously created wheel as asset.


```
git clone git@github.com:mundialis/actinia-stac-plugin.git
cd actinia-stac-plugin

tag=0.0
credentials=mygithubuser:mygithubpw

docker build --file docker/release/Dockerfile --build-arg tag=$tag --build-arg credentials=$credentials --tag actinia-stac-plugin:build .

docker run --rm actinia-stac-plugin:build
```
