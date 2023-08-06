# Core CLI v0.1.3

## Prerequisites

The following packages are used across python repositories. A global install of them all is *highly* recommended.

* [Poetry](https://python-poetry.org/docs/#installation)
* [Invoke](https://www.pyinvoke.org/installing.html)
* [Kubefwd](https://kubefwd.com)

A running cluster from [Local
Helm](https://github.com/NEOM-KSA/neos-core-platform/tree/main/demo/helm) with
`gateway` service port forwarded. Details on port forwarding below.

### WSL

If running on Windows, you may need to install `distutils` to install the service.

```bash
$ sudo apt-get install python3.10-distutils
```

## Initial setup

```bash
$ invoke install-dev
```

## Code Quality

### Tests

```bash
invoke tests
invoke tests-coverage
```

## Linting

```bash
invoke check-style
invoke isort
```

## Running locally

### Port forwarding

To access the gateway api locally, you will need to connect to the pod inside
the cluster using `kubefwd`.

```bash
$ sudo kubefwd svc -n core -c ~/.kube/config
```

### Neosctl

#### Prerequisite

```bash
$ poetry shell
```

#### Initialize profile

```bash
$ neosctl -p my-profile profile init
Initialising [default] profile.
Gateway API url [http://core-gateway.core-gateway:9000/api/gateway]: <http://gateway_api_url:port>
Registry API url [http://neos-registry.registry:80/api/registry]: <http://registry_api_url:port>
Username: <username>
Auth flow [keycloak]: <basic|keycloak>
```

```bash
$ cat ~/.neosctl
```

#### Login

```bash
$ neosctl -p=<my-profile> auth login
```

#### Commands to work with data products

```bash
$ neosctl product --help
$ neosctl metadata --help
```

## Releases

Release management is handled using `bump2version`. The below commands will tag
a new release. This will also update the helm chart version, this should not be
manually changed.

```bash
$ invoke bump-patch
$ invoke bump-minor
$ invoke bump-major
> vX.Y.Z
```
