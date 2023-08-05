## Installation

```
pip install scamadviser_client
```

or

```
poetry add scamadviser_client
```

## Usage

```python
from scamadviser_client import FeedAPI

api = FeedAPI(apikey=[your_apikey])

api.list(params={"type": "daily"})
api.download(params={"path": "/5-minute/1602245968.json"})
```

## Development

You may install [Nix](https://nixos.org/download.html) to have fully env settings by running `nix-shell`,
or simply use `poetry shell` to bootstrap this package if you would like to join our development.

We also use [justfile](https://github.com/casey/just) to provide some simple commands, you may use

```bash
just default
```

to check all of these available commands.

### start the environment (poetry)

```bash
just up
```

### stop the environment (poetry)

```bash
just down
```

### test

```bash
just test
```

### make the code prettier

```bash
just be-pretty
```
