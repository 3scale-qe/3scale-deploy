# 3scale deployer

This project aims to create simple containerized tool to deploy 3scale into a OpenShift cluster.
To run this container you need to specify variables as seen in the `env-file.txt`.

## Prerequisites

In order to successfully deploy 3scale you need to meet following criteria:

* You have AWS access key with rights to create s3 bucket
* Serviceaccount under which identity the pod is started has rights to target namespace 
  * Specifically to create secret
  * and create, read, modify and delete apimanager object
  * In case of wildcard autodiscovery read access to `config.openshift.io/v1 Ingress cluster` needs to be
    added as well. Otherwise `DEPL_CLUSTER_WILD` environment variable must be set.
* The pod has exported environment variables as defined in `env-file.txt`.

If all of the requirements are met then the pod can successfully deploy 3scale.

## Deployment

Create pod with prerequisites specified above, the command should be following

```yaml
    spec:
      containers:
      - command:
        - deploy
        - install
```

This will deploy create AWS S3 bucket with appropriate settings and deploy 3scale using it.

## Removal

To remove installation just run the pod configured in the same manner as for deployment (e.g. using same 
environment variables) and change command to following

```yaml
    spec:
      containers:
      - command:
        - deploy
        - remove 
```

### Verbosity

In case of problems the tool can be set to use more verbose logging. In order to enable it add option `-v` or `-vv`
as a second argument of command `deploy`.

```yaml
    spec:
      containers:
      - command:
        - deploy
        - -vv
        - remove
```
