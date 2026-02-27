# Adobe Journey Optimizer (AJO) Support

The `aepp` library includes a client module for the Adobe Journey Optimizer (AJO) API.
The module lives at `aepp/ajo.py` and exposes a `JourneyOptimizer` class that follows
the same patterns as other `aepp` service classes (`Schema`, `Catalog`, etc.).

## Installation

AJO support uses only the dependencies already present in the base `aepp` package.
Install normally:

```shell
pip install aepp
```

A semantic optional extra is also available for tooling that needs to distinguish
AJO-specific installations:

```shell
pip install aepp[ajo]
```

## Required IMS Scopes

The AJO Journey API requires the following OAuth scopes to be configured in your
Adobe Developer Console project:

- `journey_optimizer_manage` (or a product-profile permission that includes journey read access)
- Typical base scopes: `openid`, `session`, `AdobeID`, `read_organizations`

Add these scopes to the `scopes` field of your configuration file or pass them via
`aepp.configure(scopes=...)`.

## Configuration

### Using a config file

The standard `aepp` configuration file works as-is for AJO.  AJO endpoints share the
same base URL as other AEP services (`https://platform.adobe.io` in production).

```json
{
    "org_id": "<your IMS org ID>",
    "client_id": "<your client ID>",
    "secret": "<your client secret>",
    "sandbox-name": "prod",
    "scopes": "openid,session,AdobeID,read_organizations,journey_optimizer_manage",
    "environment": "prod"
}
```

```python
import aepp
from aepp.ajo import JourneyOptimizer

aepp.importConfigFile("config.json")
ajo = JourneyOptimizer()
```

### Using `aepp.configure` programmatically

```python
import aepp
from aepp.ajo import JourneyOptimizer

config = aepp.configure(
    org_id="<your IMS org ID>",
    client_id="<your client ID>",
    secret="<your client secret>",
    sandbox="prod",
    scopes="openid,session,AdobeID,read_organizations,journey_optimizer_manage",
    connectInstance=True,
)
ajo = JourneyOptimizer(config=config)
```

### Custom AJO base URL

If your AJO instance uses a different base URL (e.g. a stage environment, regional
deployment, or an internal proxy), override it via `ajo_base_url`:

```python
config = aepp.configure(
    org_id="<your IMS org ID>",
    client_id="<your client ID>",
    secret="<your client secret>",
    sandbox="prod",
    scopes="...",
    connectInstance=True,
    ajo_base_url="https://platform-stage.adobe.io",  # override
)
ajo = JourneyOptimizer(config=config)
```

The default (`None`) means the same global endpoint as all other AEP services is used,
so existing callers are not affected.

## Listing Journeys

```python
# Fetch first page (up to 100 journeys)
response = ajo.list_journeys()
journeys = response["results"]  # list of journey dicts
total_pages = response["pages"]

# Filter by status
response = ajo.list_journeys(filter="status=live")

# Select only specific fields
response = ajo.list_journeys(fields="name,status,metadata")

# Sort results
response = ajo.list_journeys(sort="metadata.createdAt=desc")

# Paginate manually
page2 = ajo.list_journeys(page=1, page_size=20)

# Auto-paginate: collect at least 250 journeys across pages
response = ajo.list_journeys(page_size=100, n_results=250)
all_journeys = response["results"]  # up to 250 items
```

### Pagination behaviour

The AJO journey list endpoint uses **0-based page numbers**.  Response fields:

| Field | Description |
|-------|-------------|
| `results` | Array of journey objects for the current page |
| `page` | Current page number (0-based) |
| `limit` | Number of items per page |
| `pages` | Total number of pages |

When `n_results` is specified, `list_journeys` fetches successive pages automatically
until the requested number of results is reached or all pages are exhausted.

## Getting a Single Journey

```python
journey = ajo.get_journey("your-journey-id")
print(journey["name"], journey["status"])

# Include related objects (campaigns, rulesets, etc.)
journey = ajo.get_journey("your-journey-id", include="campaigns,rulesets")
```

## Extracting Journey IDs

```python
ids = ajo.get_journey_ids()
# Returns: ["id-1", "id-2", ...]
```

## API Reference

The implementation is based on the spec file
`static/journey-retrieve.yaml` in the
[AdobeDocs/journey-optimizer-apis](https://github.com/AdobeDocs/journey-optimizer-apis)
repository.

Endpoints implemented:

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/ajo/journey` | List journeys with optional pagination, filter, sort, and field selection |
| `GET` | `/ajo/journey/{id}` | Retrieve a single journey by ID with optional include |
