## Adding Prometheus target

Set proper IP address and port in fioparser_target.yaml
Run following command

juju config prometheus scrape-jobs=$(cat <path to fioparser_target.yaml>)
