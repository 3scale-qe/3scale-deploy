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

If all the requirements are met then the pod can successfully deploy 3scale.

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

## Variables

In order to run, the container needs following variables set:

| Variable                | Availability | Description                                                                                                                                   |
|-------------------------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| `AWS_ACCESS_KEY_ID`     | **Required** | IAM Key id used for authentication to AWS (create bucket, connect 3scale to bucket and remove bucket)                                         |
 | `AWS_SECRET_ACCESS_KEY` | **Required** | IAM secret key                                                                                                                                |
 | `AWS_REGION`            | **Required** | AWS region where the bucket will be created                                                                                                   |
 | `DEPL_PROJECT_NAME`     | **Required** | Namespace where the 3scale will be deployed                                                                                                   |
 | `DEPL_BUCKET_NAME`      | **Required** | Name of bucket created for 3scale                                                                                                             |
| `DEPL_ROUTE_PREF`       | *Optional*   | If set prefix for the route creation by 3scale will be added e.g. routes will be created in `*.${DEPL_ROUTE_PREF}.${CLUSTER_WILDCARD_DOMAIN}` |
 | `DEPL_CLUSTER_WILD`     | *Optional*   | If set, the resolution of `CLUSTER_WILDCARD_DOMAIN` is skipped and this value is used. See above.                                             |