# RelevanceAI Explore App SDK

This repo is for managing/configuring deployables through a Python SDK.

# How to

## Eplore

Instantiate the Client

```python
from src import Client

client = Client(token=os.getenv("TOKEN"))}
```

Load your most recently updated deployable...

```python
deployable = client.recent()
```

...or call it with its unique `deployabled_id`.

```python
deployable = client.Deployable(deployabled_id="")
```

Make edits to the `config` as you see fit.
Once done, simply...

```python
deployable.push()
```

To retrieve edits made in the browser...

```python
deployable.pull()
```

## Data Report

```python
from src.tabs import DataReport

deployable = client.recent()

text = """# Header
## sub heading
this is what **I** want to *say*"""

tab = DataReport.from_markdown(
    title="Example",
    text=text,
)

deployable.append(tab)

deployable.push()

```

## Document View

TBA

## Category View

TBA

## Chart View

TBA
