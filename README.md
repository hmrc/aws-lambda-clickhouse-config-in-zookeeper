# clickhouse-config-in-zookeeper-lambda


[![Brought to you by Telemetry Team](https://img.shields.io/badge/MDTP-Telemetry-40D9C0?style=flat&labelColor=000000&logo=gov.uk)](https://confluence.tools.tax.service.gov.uk/display/TEL/Telemetry)

Zookeeper obtains the configuration for certain Clickhouse configuration files via a lambda which injects the
'remote-servers' config into Zookeeper

## Running tests

The target runtime for this lambda varies from Python version 3.6 -> 3.8. Separate Dockerfiles were added to cover these
various Python runtime versions so assurance that the tests work in all scenarios is achieved.

```bash
$ make build test
```

# References
[Runbook - Clickhouse](https://confluence.tools.tax.service.gov.uk/display/TEL/RUNBOOK+-+Clickhouse)

### License

This code is open source software licensed under the [Apache 2.0 License]("http://www.apache.org/licenses/LICENSE-2.0.html").
