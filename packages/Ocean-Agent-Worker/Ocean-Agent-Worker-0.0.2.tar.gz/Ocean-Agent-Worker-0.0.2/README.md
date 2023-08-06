# Ocean Agent for Worker

## initial development setup
For linux/mac
```
$ ./boot.sh
$ source venv/bin/activate
```
For windows
```
> ./boot.bat
> venv\Scripts\activate.bat
```

## usage
```
usage: Ocean Agent Clinet [-h] CMD

positional arguments:
  CMD {hello, join}

optional arguments:
  -h, --help  show this help message and exit
```
### setup and join worker node
```
$ agent-master join
```

### master-agnet test
```
$ agent-master hello
```
