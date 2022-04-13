## Deploying Prometheus and Graphana
Running the bundle:

```
juju add-model fioparser
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
juju config prometheus --file postprocessing/fioparser_target.yaml
```

