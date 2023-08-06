# FSCLI

### Thank you for visiting! ![](https://visitor-badge.glitch.me/badge?page_id=fluidstackio.fscli)

FSCLI is a module that simplifies starting, stopping & deleting servers based on server_id and email.

## Installation

### Using `pip3`

You can install the FSCLI package using `pip3`. If there are any errors or issues with `pip3`, then you can install it using Git(down below).

```shell
~$ pip3 install --upgrade fscli
```

## Usages

These are different commands that you can run, replace the word inside the <> with the replacement value.

```shell
~$ python3 -m fscli --start --email <email> --server_id <server id>
~$ python3 -m fscli --stop_all --email <email>
~$ python3 -m fscli --stop --email <email> --server_id <server id>
~$ python3 -m fscli --destroy_all --email <email>
~$ python3 -m fscli --destroy --email <email> --server_id <server_id>
~$ python3 -m fscli --fraud_set --email <email>
```

## Installation From Source

### Cloning the Repository

If you are installing from source, be sure to have `git` installed on your machine.

```shell
~$ git clone https://github.com/fluidstackio/fscli.git
```

### Installing the packages

You can use `pip3` to install the packages required to run the package.

```shell
~$ cd FSCLI && sudo pip3 install -r requirements.txt
```
