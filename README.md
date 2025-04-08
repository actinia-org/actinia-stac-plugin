<!-- markdownlint-configure-file
{
  "MD013": { "line_length": 150 },
  "MD034": false # no-bare-urls
}
-->

# actinia-stac-plugin

You can run actinia-stac-plugin as actinia-core plugin.

## Installation

For installation or DEV setup, see docker/README.md.

## DEV notes

### Build

__insprired by https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/__

to create a shippable wheel, run

```bash
pip3 install --upgrade pip pep517
python3 -m pep517.build .
```

#### Versioning

https://semver.org/ (MAJOR.MINOR.PATCH)

#### Logging

in any module, import `from actinia_stac_plugin.resources.logging import log` and call logger with `log.info("my info i want to log")`
