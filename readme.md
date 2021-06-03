# worker.home

This python application is used to collect periodically hardware informations.\
These informations can be consume through a web socket.

> Need Python 3.8

# Configuration

```bash
pip install distro, psutil, websockets
python startup.py
```

# Data exemple sended through the web socket

```json
{
  "static": {
    "cpuName": "Intel(R) Core(TM) i5-6300U CPU @ 2.40GHz",
    "operatingSystem": "Windows 10",
    "kernel": "10.0.19042"
  },
  "periodic": [
    {
      "memoryInfo": {
        "total": 16968880128,
        "available": 11326070784,
        "percent": 33.3,
        "used": 5642809344,
        "free": 11326070784
      },
      "cpuInfo": {
        "frequence": {
          "current": 2400,
          "min": 0,
          "max": 2501
        },
        "percent": 100,
        "cores": 2,
        "threads": 4
      },
      "networkInfo": {
        "sentPerSec": 0,
        "recvPerSec": 0
      },
      "processInfo": [
        {
          "memory_percent": 0.0000482766095240578,
          "pid": 0,
          "create_time": 0,
          "cpu_percent": 0,
          "username": "NT AUTHORITY\\SYSTEM",
          "name": "System Idle Process",
          "memory_used": 819200
        }
      ],
      "diskInfo": [
        {
          "total": 243354562560,
          "used": 230136930304,
          "free": 13217632256,
          "percent": 94.6,
          "mountpoint": "C:\\"
        }
      ],
      "time": 1622748840000
    }
  ]
}
```
