# find-gcp-ips
Attempts to find all private and public/ephemeral IPs within a GCP project.  I started working ont his because of [this issue](https://issuetracker.google.com/issues/11917861).  It seems kind of silly that Google wouldn't make a command that can get all this info.  I have worked with [Cloud Asset API](https://cloud.google.com/asset-inventory/docs/apis) before so I'd try and build a tool with it that can query all this information for the user in a nice tabular format.

- List of [supported asset types](https://cloud.google.com/asset-inventory/docs/supported-asset-types)

## How-to Use
```
export GCP_PROJECT='your_gcp_project_id'
```

```
python main.py
```

- sample output
```
+----+---------------------------------------+-------------------------------------------+---------------------------+----------------------------+
|    | ASSET TYPE                            | DISPLAY NAME                              | LOCATION                  | IP ADDRESS(ES)             |
|----+---------------------------------------+-------------------------------------------+---------------------------+----------------------------|
|  0 | compute.googleapis.com/ForwardingRule | a434d6b1c45e8467b843fe592fbd6abcd         | northamerica-northeast1   | 34.234.56.78               |
|  1 | compute.googleapis.com/Address        | default-ip-range                          | global                    | 172.19.176.0               |
|  2 | compute.googleapis.com/Instance       | gke-playground-preempt-pool-e6602b85-qhmc | northamerica-northeast1-c | 192.168.0.8, 35.123.45.67  |
|  3 | compute.googleapis.com/Instance       | random-app                                | northamerica-northeast2-a | 10.188.0.3                 |
|  4 | compute.googleapis.com/Instance       | rundeck-plugin-tester                     | us-central1-a             | 10.128.0.30                |
|  5 | compute.googleapis.com/Instance       | findingwaldo                              | northamerica-northeast2-a | 10.188.0.2, 34.123.234.123 |
|  6 | tpu.googleapis.com/Node               | node-1                                    | us-central1-b             | 10.1.10.34                 |
|  7 | container.googleapis.com/Cluster      | playground                                | northamerica-northeast1-c | 35.123.12.12               |
+----+---------------------------------------+-------------------------------------------+---------------------------+----------------------------+
```

## Known Issues
- [IssueTracker#207842547](https://issuetracker.google.com/issues/207842547)

## TODO
- add more resources/assets
- refactor code
