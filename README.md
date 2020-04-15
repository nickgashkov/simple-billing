# Simple Billing API [![Build Status](https://github.com/nickgashkov/simple-billing/workflows/build/badge.svg)]

**Simple Billing API** is a sample application showcasing Python and PostgreSQL
as backend technologies to build financial applications.

## Prerequisites

To run **Simple Billing API**, [Docker](https://docs.docker.com/install/) must be
installed.

## Building

**Simple Billing API** can be built using `make`:

```
$ make build
```

## Running

**Simple Billing API** can be run using `make` as well:

```
$ make run
```

Before running, this command will build Docker container and run pending
migrations if any exists. 

API can be accessed at http://localhost:8080.

### Examples

API can be interacted with via cURL, HTTPie, Postman or via Swagger at
http://localhost:8080/api/doc/. Also, quick API showcase can be found at YouTube:

[![Simple Billing API Showcase](https://img.youtube.com/vi/e9FFsZTtBNc/0.jpg)](https://www.youtu.be/e9FFsZTtBNc)
