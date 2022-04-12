## Deploying Prometheus and Graphana
Running the bundle:

```
juju deploy ./postprocessing/bundle.yaml
```


Getting graphana password:

```
juju run-action grafana/0 get-login-info --wait

```
## Adding Prometheus target

Set proper IP address and port in `fioparser_target.yaml`
Run following command

```
juju config prometheus scrape-jobs=$(cat <path to fioparser_target.yaml>)
```

