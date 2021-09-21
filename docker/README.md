# actinia-module-plugin

You can run actinia-module-plugin as actinia-core plugin.
To run actinia-module-plugin with actinia-core, see https://github.com/mundialis/actinia_core/blob/master/docker/README.md#Local-dev-setup-with-docker
Mind that it needs to be registered in the actinia-core config under API.plugins

## DEV notes

__test endpoints__
```
http://127.0.0.1:8088/api/v1/grassmodules
http://127.0.0.1:8088/api/v1/grassmodules/d.barscale
http://127.0.0.1:8088/api/v1/grassmodules/d.barscale3

http://127.0.0.1:8088/api/v1/actiniamodules
http://127.0.0.1:8088/api/v1/actiniamodules/vector_area

http://127.0.0.1:8088/api/v1/modules
http://127.0.0.1:8088/api/v1/modules/d.barscale
http://127.0.0.1:8088/api/v1/modules/vector_area
http://127.0.0.1:8088/api/v1/modules/vector_area5

http://127.0.0.1:8088/api/v1/swagger.json

```

## Create API docs
```
wget -O /tmp/actinia-module.json http://127.0.0.1:8088/api/v1/swagger.json
```
Run spectacle docker image to generate the HTML documentation
```
docker run -v /tmp:/tmp -t sourcey/spectacle \
  spectacle /tmp/actinia-module.json -t /tmp

# or with local installation (npm install -g spectacle-docs, python2 required)
cd actinia_stac_plugin/static
spectacle /tmp/actinia-module.json -t .

# to build all in one file:
spectacle -1 /tmp/actinia-module.json -t .
```
beautify css
```
sed -i 's+<link rel="stylesheet" href="stylesheets/spectacle.min.css" />+<link rel="stylesheet" href="stylesheets/spectacle.min.css" />\n    <link rel="stylesheet" href="stylesheets/actinia.css" />+g' index.html
```


## Copy&Paste one-liner:
```
wget -O /tmp/actinia-module.json http://127.0.0.1:8088/api/v1/swagger.json && spectacle /tmp/actinia-module.json -t . && mv public/index.html index.html && rm -r public && sed -i 's+<link rel="stylesheet" href="stylesheets/spectacle.min.css" />+<link rel="stylesheet" href="stylesheets/spectacle.min.css" />\n    <link rel="stylesheet" href="stylesheets/actinia.css" />+g' index.html
```
