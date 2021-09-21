## actinia-core process-chain templating

You can run actinia-module-plugin in multiple ways (see README.md). If actinia-module-plugin is installed as actinia-core plugin, endpoints for module self-description are added. These modules are a collection of common GRASS GIS modules (grass-module) and of specific actinia-modules. While GRASS GIS is able to tell input/output parameters for a certain GRASS GIS module via `--interface-description` which can easily be converted to JSON, actinia-modules are more complex.

Most of these actinia-modules are stored as process-chain template. Process-chains are a way to tell actinia-core what needs to be processed and are mostly a list of GRASS commands in a defined JSON format.

This readme explains the module self-description which actinia provides as well as process-chain templates and the combination of self-description for temlpates. Last but not least conventions for template creation are listed.

Content:
1. Module self-description
1. Process-chain templates
1. Template self-description
1. Hints for template creation
1. Conventions for template creation
1. Overview of endpoints for self-description


### 1. Module self-description

One grass-module self-description can be requested as follows:

`curl -X GET http://127.0.0.1:8088/api/v1/modules/v.buffer`

One example response to describe the GRASS GIS module "v.buffer" looks like this:

```
{
  "categories": [
    "area",
    "buffer",
    "circle",
    "geometry",
    "grass-module",
    "grow",
    "line",
    "shrink",
    "vector"
  ],
  "description": "Creates a buffer around vector features of given type.",
  "id": "v.buffer",
  "parameters": {
    "angle": {
      "description": ". Angle of major axis in degrees",
      "required": false,
      "schema": {
        "default": "0",
        "type": "number"
      }
    },
    "c": {
      "description": ". Do not make caps at the ends of polylines",
      "schema": {
        "default": "False",
        "type": "boolean"
      }
    },
    "cats": {
      "description": "Category values. Example: 1,3,7-9,13",
      "required": false,
      "schema": {
        "subtype": "cats",
        "type": "string"
      }
    },
    "column": {
      "description": ". Name of column to use for buffer distances",
      "required": false,
      "schema": {
        "subtype": "dbcolumn",
        "type": "string"
      }
    },
    "distance": {
      "description": ". Buffer distance along major axis in map units",
      "required": false,
      "schema": {
        "type": "number"
      }
    },
    "help": {
      "description": ". Print usage summary",
      "schema": {
        "default": "False",
        "type": "boolean"
      }
    },
    "input": {
      "description": "Name of input vector map. Or data source for direct OGR access",
      "required": true,
      "schema": {
        "subtype": "vector",
        "type": "string"
      }
    },
    "layer": {
      "description": "Layer number or name ('-1' for all layers). A single vector map can be connected to multiple database tables. This number determines which table to use. When used with direct OGR access this is the layer name.",
      "required": false,
      "schema": {
        "default": "-1",
        "subtype": "layer_all",
        "type": "string"
      }
    },
    "minordistance": {
      "description": ". Buffer distance along minor axis in map units",
      "required": false,
      "schema": {
        "type": "number"
      }
    },
    "output": {
      "description": ". Name for output vector map",
      "required": true,
      "schema": {
        "subtype": "vector",
        "type": "string"
      }
    },
    "overwrite": {
      "description": ". Allow output files to overwrite existing files",
      "schema": {
        "default": "False",
        "type": "boolean"
      }
    },
    "quiet": {
      "description": ". Quiet module output",
      "schema": {
        "default": "False",
        "type": "boolean"
      }
    },
    "s": {
      "description": ". Make outside corners straight",
      "schema": {
        "default": "False",
        "type": "boolean"
      }
    },
    "scale": {
      "description": ". Scaling factor for attribute column values",
      "required": false,
      "schema": {
        "default": "1.0",
        "type": "number"
      }
    },
    "t": {
      "description": ". Transfer categories and attributes",
      "schema": {
        "default": "False",
        "type": "boolean"
      }
    },
    "tolerance": {
      "description": ". Maximum distance between theoretical arc and polygon segments as multiple of buffer (default 0.01)",
      "required": false,
      "schema": {
        "type": "number"
      }
    },
    "type": {
      "description": ". Input feature type",
      "required": false,
      "schema": {
        "default": "point,line,area",
        "enum": [
          "point",
          "line",
          "boundary",
          "centroid",
          "area"
        ],
        "type": "array"
      }
    },
    "verbose": {
      "description": ". Verbose module output",
      "schema": {
        "default": "False",
        "type": "boolean"
      }
    },
    "where": {
      "description": "WHERE conditions of SQL statement without 'where' keyword. Example: income < 1000 and population >= 10000",
      "required": false,
      "schema": {
        "subtype": "sql_query",
        "type": "string"
      }
    }
  }
}

```

### 2. Process-chain templates
An example process-chain looks like this:

```
{
    "list": [
        {
            "id": "add_column_for_area",
            "module": "v.db.addcolumn",
            "inputs": [
                {
                    "param": "map",
                    "value": "polygons"
                },
                {
                    "param": "columns",
                    "value": "area_h DOUBLE PRECISION"
                }
            ]
        },
        {
            "id": "caulate_area",
            "module": "v.to.db",
            "inputs": [
                {
                    "param": "map",
                    "value": "polygons"
                },
                {
                    "param": "column",
                    "value": "area_h"
                },
                {
                    "param": "option",
                    "value": "area"
                },
                {
                    "param": "unit",
                    "value": "h"
                }
            ]
        },
        {
            "id": "v_db_select",
            "module": "v.db.select",
            "inputs": [
                {
                    "param": "map",
                    "value": "polygons"
                },
                {
                    "param": "column",
                    "value": "area_h"
                }
            ]
        }
    ],
}

```

There are some reasons why it might be useful to store a process chain and create a template out of it:
* If this process-chain is applied multiple times to different input data, most of it won't change, but the user needs to store the process-chain itself and change the values.
* The user might not know how to formulate a whole process-chain but wishes to use predefined ones and only change some parameters.
* A client with autogenerated requests talks to the API directly and needs a consistent way to adress predefined processes.
Therefore actinia-module-plugin is able to store process-chain templates and the user only needs to enter certain values. A template might look like this:


```
{
    "id": "vector_area",
    "description": "Computes the areas in h for selected map.",
    "template": {
        "list": [
            {
                "id": "add_column_for_area",
                "module": "v.db.addcolumn",
                "inputs": [
                    {
                        "param": "map",
                        "value": "{{ name }}"
                    },
                    {
                        "param": "columns",
                        "value": "{{ column }}"
                    }
                ]
            },
            {
                "id": "calculate_area",
                "module": "v.to.db",
                "inputs": [
                    {
                        "param": "map",
                        "value": "{{ name }}"
                    },
                    {
                        "param": "columns",
                        "value": "{{ column_name }}"
                    },
                    {
                        "param": "option",
                        "value": "area"
                    },
                    {
                        "param": "unit",
                        "value": "h"
                    }
                ]
            },
            {
                "id": "v_db_select",
                "module": "v.db.select",
                "inputs": [
                    {
                        "param": "map",
                        "value": "{{ name }}"
                    },
                    {
                        "param": "columns",
                        "value": "{{ column_name }}"
                    }
                ]
            }
        ],
        "version": "1"
    }
}


```
This way, the user only needs to set values for the defined variables. The user doesn't even need to know the whole template. Actinia-module-plugin will translate it into one actinia-module, exploiting only the values necessary for input:

```
{
        "list": [
            {
                "id": "vector_area",
                "module": "vector_area",
                "inputs": [
                    {
                        "param": "v.db.addcolumn_map",
                        "value": "{{ name }}"
                    },
                    {
                        "param": "v.db.addcolumn_columns",
                        "value": "{{ columns }}"
                    },
                    {
                        "param": "v.to.db_map",
                        "value": "{{ name }}"
                    },
                    {
                        "param": "v.to.db_columns",
                        "value": "{{ column_name }}"
                    },
                    {
                        "param": "v.db.select_map",
                        "value": "{{ name }}"
                    },
                    {
                        "param": "v.db.select_columns",
                        "value": "{{ column_name }}"
                    }
                ]
            }
        ],
        "version": "1"
    }
```

For the user this looks like one module in the process-chain. In further development, it will be shrinked even more to not exploit the same variable twice. This might then look like this:

```
{
        "list": [
            {
                "id": "vector_area",
                "module": "vector_area",
                "inputs": [
                    {
                        "param": "v.db.addcolumn_map",
                        "value": "{{ name }}"
                    },
                    {
                        "param": "v.db.addcolumn_columns",
                        "value": "{{ columns }}"
                    },
                    {
                        "param": "v.to.db_columns",
                        "value": "{{ column_name }}"
                    }
                ]
            }
        ],
        "version": "1"
    }

```


### 3. Template self-description

Mapping the process-chain template to a self-description will look as follows and the user won't feel the difference between a grass-module and an actinia-module anymore:

```
{
  "categories": [
    "actinia-module"
  ],
  "description": "Copies zipcodes_wake and compute the areas in h.",
  "id": "vector_area",
  "parameters": {
    "v.db.addcolumn_columns": {
      "description": "Name and type of the new column(s) ('name type [,name type, ...]'). Types depend on database backend, but all support VARCHAR(), INT, DOUBLE PRECISION and DATE. Example: 'label varchar(250), value integer'",
      "required": true,
      "schema": {
        "type": "array"
      }
    },
    "v.db.addcolumn_map": {
      "description": "Name of vector map. Or data source for direct OGR access",
      "required": true,
      "schema": {
        "subtype": "vector",
        "type": "string"
      }
    },
    "v.to.db_columns": {
      "description": "Name of attribute column(s) to populate. Name of attribute column(s)",
      "required": true,
      "schema": {
        "subtype": "dbcolumn",
        "type": "array"
      }
    }
  }
}


```
### 4. Hints for template creation


* __It is not allowed to manipulate existing maps__
This leads to an error for ephemeral and persistent processing. E.g. `v.db.addcolumn` is not working and leads to `"ERROR: Vector map <elev_points> not found in current mapset"`. Therefore copy it first (in the same processchain!) with g.copy. If it is done in a separate process chain and even exists in the user mapset, it is still not working.

* __Map search order__
On persistent processing, name of map will be first searched in PERSISTENT mapset, then in user mapset. If both exist and user mapset should be used, this can be overwritten by mymap@mymapset.


### 5. Conventions for template creation

* __Only use placeholder for a whole value of a GRASS GIS attribute.__

* __Do not use placeholder for only part of a value of a GRASS GIS attribute.__
E.g. not like this:
`{param: "g.copy_vector", value: "zipcodes_wake,{{ name }}" }`
As the self-desription will display the data type of the whole parameter, placeholder of only one part of the value could lead to weird results.
Exceptions might be ok for filesystem-paths. TODO discuss.

* __Make use of importer and exporter where possible, especially for Landsat / Sentinel data.__
Both are special modules from actinia-core. Safety mechanisms are already implemented and optimized, e.g. clean up of download cache from node / feature to block download if it threatenes health of node...


#### Conventions to be disucssed

* __If data should be imported or exported, do not do this in template but leave to importer / exporter module for user__
TODO discuss

* __To be able to use all templates either for ephemeral or for persistent processing, always define an export.__
TODO discuss




### 5. Overview of endpoints for module self-description and execution

List / Describe only GRASS Modules

* GET /grass_modules
* GET /grass_modules/d.barscale
* GET /grass_modules/d.barscale3

List / Describe only Modules (process-chain templates)

* GET /actinia_modules
* GET /actinia_modules/vector_area

List / Describe combined

* GET /modules
* GET /modules/d.barscale
* GET /modules/vector_area
* GET /modules/vector_area5

Execute module

* POST /locations/{location_name}/processing_export
* POST /locations/{location_name}/mapsets/{mapset_name}/processing (TODO)

Full API docs

* GET /swagger.json



### 6. Additional Notes

#### The self-description tries to comply the [openEO API](https://open-eo.github.io/openeo-api/apireference/#tag/Process-Discovery/paths/~1processes/get) where applicable.
At some points, however, we have to divert from their API:

* `returns` section may contain multiple outputs and has the same structure
as the `parameters` sections.

A parameter will only be added to the `returns` section if it contains the property `gisprompt.@age` and only if that value equals `'new'`. In all other cases, the parameter will be added to the `parameters` section.

* the importer and exporter modules have additional attributes (import_descr / export)

#### Importer and exporter
These are neiher fully grass-modules nor fully actinia-modules. They need to be added to GRASS GIS with g.extension (originally for ace usage) but are extended by actinia-module-plugin. The GRASS interface description does not describe import_descr and export as seen in API docs, so this is extended. It is possible to extend all GRASS modules by importer/exporter attributes if applicable (e.g. output of v.buffer can directly be exported with "export" attribute inside module)
