# ECMind blue client: Spring

Helper module for spring alike configuration loading plus spring cloud config client

## Installation

`pip install ecmind_spring_config`

## Usage

```python
from ecmind_spring_config.config import Config

config = Config()

eureka_service_url = config['eureka.client.service-url.defaultZone']
```

The following happens:

* All Environement Parameter will be loaded
* For each location (default are ./ and ./config/)
  * If location is a file path
    * Load file and patch the configuration
  * If location is a directory path
    * Load application.yml  and patch the configuration if exists
    * For each Profile (default is 'default')
      * Load application-{profile}.yml and patch the configuration if exists
* If key `spring.cloud.config.uri` and `spring.application.name` is set
  * Load configuration from spring cloud config service and path configuration
