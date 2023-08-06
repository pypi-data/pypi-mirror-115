# Ocean Agent for Master

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
usage: Ocean-Agnet for Master [-h] CMD

positional arguments:
  CMD {setup, serve}

optional arguments:
  -h, --help  show this help message and exit
```
### setup master node
```
$ agent-master setup
```

### start master-agnet server
```
$ agent-master serve
```

### master-agnet test
```
$ agent-master hello
```