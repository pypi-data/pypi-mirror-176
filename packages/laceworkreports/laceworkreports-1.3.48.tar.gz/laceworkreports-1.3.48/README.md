# Lacework Reports CLI/SDK

<div align="center">

[![Build status](https://github.com/laceworkps/laceworkreports/workflows/build/badge.svg?branch=main&event=push)](https://github.com/laceworkps/laceworkreports/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/laceworkreports.svg)](https://pypi.org/project/laceworkreports/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/laceworkps/laceworkreports/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/laceworkps/laceworkreports/blob/main/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/laceworkps/laceworkreports/releases)
[![License](https://img.shields.io/github/license/laceworkps/laceworkreports)](https://github.com/laceworkps/laceworkreports/blob/main/LICENSE)
![Coverage Report](assets/images/coverage.svg)

laceworkreports is a Python cli/package for creating reports from Lacework data.

</div>

## 🚀 Features

- Retrieve Lacework API data from activities, entities, queries, configs
- Save results as csv, json, or to postgres
- Transform results using jinja template
- Override returned field names using field_map (supports nested json notation: parent.child.value)
- Stores complex json objects as JSONB in postgres
- Flatten json structures before writing

## CLI Usage

```bash
laceworkreports export vulnerabilities hosts csv --file-path="export.csv"
```

![laceworkreports](assets/images/laceworkreports.gif)

See [CLI README](README-CLI.md) for details.

## SDK Usage

```python
from laceworkreports import common
from laceworkreports.sdk.DataHandlers import (
    DataHandlerTypes,
    ExportHandler,
    QueryHandler,
)

eh = ExportHandler(
    format=DataHandlerTypes.CSV,
    results=QueryHandler(
        client=LaceworkClient(),
        type=common.ObjectTypes.Activities.value,
        object=common.ActivitiesTypes.DNSSummaries.value,
        filters=[{"field": "mid", "expression": "eq", "value": 851}],
        returns=["fqdn"],
    ).execute(),
    file_path="export.csv",
).export()
```

See [example.py](examples/sdk/example.py) for details.

## Installation

```bash
pip install -U laceworkreports
```

or install with `Poetry`

```bash
poetry add laceworkreports
```

Then you can run

```bash
laceworkreports --help
```

or with `Poetry`:

```bash
poetry run laceworkreports --help
```

or run with `docker`:

```bash
docker run --rm -it --name laceworkreports \
    -v ~/.lacework.toml:/home/user/.lacework.toml -v $(pwd)/reports:/app/reports \
    laceworkps/laceworkreports:latest --help
```

or run with `docker` and start a shell:

```bash
docker run --rm --entrypoint="/bin/bash" -it --name laceworkreports \
    -v ~/.lacework.toml:/home/user/.lacework.toml -v $(pwd)/reports:/app/reports \
    laceworkps/laceworkreports:latest --help
```

or run with `docker` and force uid:gid on the volume mount (may be required for write permissions):

```bash
docker run --rm -it \
    --name laceworkreports \
    -v ~/.lacework.toml:/home/user/.lacework.toml \
    -v $(pwd)/reports:/app/reports \
    --env=HOME=/home/user \
    --user $UID:$GID \
    laceworkps/laceworkreports:latest
```

## 📈 Releases

You can see the list of available releases on the [GitHub Releases](https://github.com/laceworkps/laceworkreports/releases) page.

We follow [Semantic Versions](https://semver.org/) specification.

We use [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). As pull requests are merged, a draft release is kept up-to-date listing the changes, ready to publish when you’re ready. With the categories option, you can categorize pull requests in release notes using labels.

### List of labels and corresponding titles

|               **Label**               |  **Title in Releases**  |
| :-----------------------------------: | :---------------------: |
|       `enhancement`, `feature`        |       🚀 Features       |
| `bug`, `refactoring`, `bugfix`, `fix` | 🔧 Fixes & Refactoring  |
|       `build`, `ci`, `testing`        | 📦 Build System & CI/CD |
|              `breaking`               |   💥 Breaking Changes   |
|            `documentation`            |    📝 Documentation     |
|            `dependencies`             | ⬆️ Dependencies updates |

## 🛡 License

[![License](https://img.shields.io/github/license/laceworkps/laceworkreports)](https://github.com/laceworkps/laceworkreports/blob/main/LICENSE)

This project is licensed under the terms of the `BSD-3` license. See [LICENSE](https://github.com/laceworkps/laceworkreports/blob/main/LICENSE) for more details.

## 📃 Citation

```bibtex
@misc{laceworkreports,
  author = {Lacework Inc.},
  title = {laceworkreports is a Python cli/package for creating reports from Lacework data.},
  year = {2022},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/laceworkps/laceworkreports}}
}
```
