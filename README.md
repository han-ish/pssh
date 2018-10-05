# pssh

pssh is simple wrapper on top of pexpect. I have seen people having trouble with using pexpect, because they didn't know how to use it well, including myself. So i wrote this for myself, and if it help anyone, that is a bonus points.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

git clone

### Prerequisites

This project requires only pexpect module to run.
Added the requirement.txt

```
from psession import Session

client = Session("foo", "s3cr3t", "192.168.50.100")
stdout = client.exec_command("ls -l")
print(stdout)
```

### Installing

A step by step series of examples that tell you how to get a development env running


```
virtualenv -p python2 venv
cd venv/bin/
source activate
pip install -r requirements.txt
```

## Running the tests
I must add tests

## Authors

* **Hanish** - *Initial work*
han-solo on #freenode


## License
May add MIT license

