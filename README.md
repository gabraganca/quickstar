# QuickStar

[![codecov](https://codecov.io/gh/gabraganca/quickstar/branch/master/graph/badge.svg)](https://codecov.io/gh/gabraganca/quickstar)

QuickStar provides the [Synspec][synspec-website] software built by Dr. Ivan Hubeny and Dr. Thierry Lanz over an API which you can consume using your tool of choice. It is also possible to synthesize multiple spectra simultaneously.

[synspec-website]: http://tlusty.oca.eu/Synspec49/synspec.html

## Example

This is an example using Pythn but, since it is an API, it is langauge agnostic allowing you to use the tool of your choice (as long it makes web request available).

The API runs asynchronously, so we need to send a POST request first with the stellar parameters to trigger the Synspec calculation. We will assume that QuickStar is running locally:

```python
import json
import requests

stellar_parameters = {"teff":20000, "logg":4.0, "wstart":4460, "wend":4500}
post_response = requests.post(
    'http://localhost:8000/synspec',
    data=json.dumps(stellar_parameters)
)

if post_response.ok:
    print(post_response.text)
# {"id":"046f8aa4-d25f-4dec-b7b1-9b1c6025e2da"}
```

With the request `id`, we can get the results:

```python
result_id = json.loads(post_response.text)['id']
get_response = requests.get(f'http://localhost:8000/synspec/{result_id}')

if get_response.ok:
    print(get_response.text)
```

Which will return, by default, only the twenty first wavelength-flux pairs.

```json
{
    "id": "e5d0b55a-52f7-4c83-953e-aec86f155288",
    "status": "SUCCESS",
    "results": [
        {
            "wavelength": 4460.0,
            "flux": 33390000.0
        },
        ...
        {
            "wavelength": 4460.185,
            "flux": 33500000.0
        }
    ],
    "finished_at": "2020-06-11T23:08:36.314996",
    "total_count": 4097
}
```

To get the full spectrum, it's necessary to paginate the results. The example below shows how to paginate the results

```python
# Get the ID in the response and send a request
result_id = json.loads(post_response.text)["id"]
get_response = requests.get(f"http://localhost:8000/synspec/{result_id}")

# Get the fist part of the spectrum
spectrum = []
if get_response.ok:
    spectrum.extend(json.loads(get_response.text).get("results", []))

# Paginate to get the rest of the spectrum
while "next" in get_response.links:
    get_response = requests.get(get_response.links["next"]["url"])
    if get_response.ok:
        spectrum.extend(json.loads(get_response.text).get("results", []))
```

## API Documentation

The API documentation can be accessed in:

* <http://127.0.0.1:8000/docs>, provided by [Swagger][api-swagger].
* <http://127.0.0.1:8000/redoc>, provided by [ReDoc][api-redoc].

[api-swagger]: https://github.com/swagger-api/swagger-ui
[api-redoc]: https://github.com/Redocly/redoc

## Requirements

The API and Synspec are containerized so all you will need is:

* [Docker][docker-install]
* [Docker Compose][docker-compose-install]

[docker-install]: https://docs.docker.com/get-docker/
[docker-compose-install]: https://docs.docker.com/compose/install/

## Deploying the services

First, we need to get the atomic and atmospheric models:

```bash
./bootstrap.sh
```

The API is configured to run with Docker Compose. In your terminal, run.

```bash
docker-compose up
```

The command above will start the API with just one worker, which will not allow you to calculate multiple spectra in parallel. To start multiple workers, for example two, we need to use the following command:

```bash
docker-compose up --scale worker=2
```

This set up will allow to calculate two spectra in parallel.

Depending of how you have installed Docker and Docker Compose, it is possible that you will need to run the docker commands above with `sudo`.
