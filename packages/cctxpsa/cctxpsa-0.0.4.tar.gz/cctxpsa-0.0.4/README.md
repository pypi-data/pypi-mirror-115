# cctx-pcap-safe-analyser
[![](https://shields.io/pypi/v/cctxpsa)](https://pypi.org/project/cctxpsa/)

# Pcap-analyser

> This repository concerns only on extracting features from pcap files.
>
> The code which is used to pull feed and save them into database is in another repository.
>
> Please checkout support-email-extractor brunch which can be used to test. The master brunch is used for front-end and isn't completed.

## Getting Started 使用指南

### Prerequisites

```
python 3.8.6
```

### Usage

- install from pip

```sh
pip install cctxpsa
```

- usage

```sh
usage: cctxpsa.py [-h] [-cf CUCKOOFILTERFILE] [-amd AIMODELDIR] [--progress] [-f PCAPFILE] [-o OUTPUTFILE] [-ocd OUTPUTCSVDIRECTORY]

optional arguments:
  -h, --help            show this help message and exit
  -cf CUCKOOFILTERFILE, --cuckoofilterfile CUCKOOFILTERFILE
                        CuckooFilter pickle file
  -amd AIMODELDIR, --aimodeldir AIMODELDIR
                        Trained AI model directories
  --progress            Print progress, if open, maybe lead slow extract speed.
  -f PCAPFILE, --pcapfile PCAPFILE
                        Pcap file need to parse!
  -o OUTPUTFILE, --outputfile OUTPUTFILE
                        A file to store output report
  -ocd OUTPUTCSVDIRECTORY, --outputcsvdirectory OUTPUTCSVDIRECTORY
                        A directory to store output csv file

```

### Usage example 使用示例

- Running code directly
    ```shell
    # only use filter
    python -m cctxpsa.cctxpsa -cf merge_filter.pickle -f ddos1.pcap --progress
    
    # use ai model and filter
    python -m cctxpsa.cctxpsa -amd ai_models -cf merge_filter.pickle  -f ddos1.pcap --progress
    ```

- Running cmd tool
    ```shell
    # only use filter
    cctxpsa -cf merge_filter.pickle -f ddos1.pcap --progress
    
    # use ai model and filter
    cctxpsa -amd ai_models -cf merge_filter.pickle  -f ddos1.pcap --progress
    ```


### Report example

```json
{
  "totalPacket": 19408,
  "totalIPAddress": 111,
  "totalIPv6Address": 2,
  "totalIPPacket": 19340,
  "totalIPv6Packet": 6,
  "duration": 258.7739198207855,
  "totalTCPFlowNum": 43,
  "totalHTTPNum": 6,
  "totalFTPNum": 0,
  "totalEmailNum": 0,
  "totalFileNum": 3,
  "totalDomainNum": 252,
  "totalMatchIpAddress": 2,
  "totalMatchIpv6Address": 0,
  "totalMatchEmailNum": 0,
  "totalMatchDomain": 7,
  "totalMatchFileHash": 0,
  "totalMatchUri": 0,
  "startTime": 1621386457.158518,
  "endTime": 1621386715.932438,
  "emailRecords": [],
  "fileHashRecords": [],
  "httpRecords": [
    {
      "request": {
        "uri": "/",
        "method": "GET",
        "headers": {
          "host": "fotoeuropa.ro",
          "upgrade-insecure-requests": "1",
          "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
          "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
          "accept-language": "zh-cn",
          "accept-encoding": "gzip, deflate",
          "connection": "keep-alive"
        },
        "version": "1.1",
        "domain": "fotoeuropa.ro",
        "url": "http://fotoeuropa.ro/"
      },
      "response": {
        "status": "301",
        "reason": "Moved Permanently",
        "headers": {
          "connection": "Keep-Alive",
          "keep-alive": "timeout=5, max=100",
          "x-powered-by": "PHP/7.0.33",
          "content-type": "text/html; charset=UTF-8",
          "location": "https://fotoeuropa.mediaro.ro/",
          "cache-control": "public, max-age=0",
          "expires": "Wed, 19 May 2021 01:10:21 GMT",
          "content-length": "0",
          "date": "Wed, 19 May 2021 01:10:21 GMT",
          "server": "LiteSpeed"
        },
        "version": "1.1"
      },
      "observables": [
        {
          "observableType": "domain",
          "value": "fotoeuropa.ro"
        }
      ],
      "srcIP": "192.168.1.100",
      "srcPort": 60775,
      "dstIP": "188.213.19.167",
      "dstPort": 80
    },
    {
      "request": {
        "uri": "/",
        "method": "GET",
        "headers": {
          "host": "123.57.185.66",
          "upgrade-insecure-requests": "1",
          "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
          "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
          "accept-language": "zh-cn",
          "accept-encoding": "gzip, deflate",
          "connection": "keep-alive"
        },
        "version": "1.1",
        "domain": "123.57.185.66",
        "url": "http://123.57.185.66/"
      },
      "response": {
        "status": "404",
        "reason": "Not Found",
        "headers": {
          "date": "Wed, 19 May 2021 01:11:20 GMT",
          "content-type": "text/plain",
          "content-length": "0",
          "server": "cloudflare"
        },
        "version": "1.1"
      },
      "observables": [
        {
          "observableType": "domain",
          "value": "123.57.185.66"
        },
        {
          "observableType": "ipv4-addr",
          "value": "123.57.185.66"
        }
      ],
      "srcIP": "192.168.1.100",
      "srcPort": 60926,
      "dstIP": "123.57.185.66",
      "dstPort": 80
    },
    {
      "request": {
        "uri": "/favicon.ico",
        "method": "GET",
        "headers": {
          "host": "123.57.185.66",
          "connection": "keep-alive",
          "accept": "*/*",
          "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
          "accept-language": "zh-cn",
          "referer": "http://123.57.185.66/",
          "accept-encoding": "gzip, deflate"
        },
        "version": "1.1",
        "domain": "123.57.185.66",
        "url": "http://123.57.185.66/favicon.ico"
      },
      "response": {
        "status": "404",
        "reason": "Not Found",
        "headers": {
          "date": "Wed, 19 May 2021 01:11:20 GMT",
          "content-type": "text/plain",
          "content-length": "0",
          "server": "cloudflare"
        },
        "version": "1.1"
      },
      "observables": [
        {
          "observableType": "domain",
          "value": "123.57.185.66"
        },
        {
          "observableType": "ipv4-addr",
          "value": "123.57.185.66"
        }
      ],
      "srcIP": "192.168.1.100",
      "srcPort": 60927,
      "dstIP": "123.57.185.66",
      "dstPort": 80
    }
  ],
  "domainRecords": [
    {
      "domain": "kgtwiakkdooplnihvali.com",
      "domain_type": "A",
      "value": "198.54.117.244",
      "timestamp": 1621386563.829686,
      "observables": [
        {
          "observableType": "domain",
          "value": "kgtwiakkdooplnihvali.com"
        }
      ],
      "srcIP": "219.223.223.2",
      "dstIP": "192.168.1.100"
    },
    {
      "domain": "kgtwiakkdooplnihvali.com",
      "domain_type": "A",
      "value": "198.54.117.244",
      "timestamp": 1621386564.47294,
      "observables": [
        {
          "observableType": "domain",
          "value": "kgtwiakkdooplnihvali.com"
        }
      ],
      "srcIP": "10.6.15.16",
      "dstIP": "192.168.1.100"
    },
    {
      "domain": "www.alam-group.com",
      "domain_type": "A",
      "value": "51.75.190.140",
      "timestamp": 1621386613.520531,
      "observables": [
        {
          "observableType": "domain",
          "value": "www.alam-group.com"
        }
      ],
      "srcIP": "10.6.15.16",
      "dstIP": "192.168.1.100"
    },
    {
      "domain": "fotoeuropa.ro",
      "domain_type": "A",
      "value": "188.213.19.167",
      "timestamp": 1621386621.302886,
      "observables": [
        {
          "observableType": "domain",
          "value": "fotoeuropa.ro"
        }
      ],
      "srcIP": "10.6.15.16",
      "dstIP": "192.168.1.100"
    }
  ]
}
```

### Compile self and upload to PyPI

- Fist, modify `setup.py`

- Second, compile and upload

```sh
python setup.py sdist bdist_wheel
twine upload dist/*
```

## Authors 作者

* **Yangyi Zou**

