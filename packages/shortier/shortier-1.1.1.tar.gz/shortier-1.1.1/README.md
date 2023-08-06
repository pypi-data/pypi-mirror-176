# Shortier

A Link shortener with support for various providers.

# Installation

The CLI tool can be installed by runnning `pip install shortier`

# How to use

To use just provide the link to be shortened.

```shell
shortier azure.microsoft.com
```

You can also define whgich service to use by adding `--type` argument.
For example to use clckru use

```shell
shortier azure.microsoft.com --type clckru
```

Shortier currently supports the following providers:

* chilpit
* clckru
* dagd
* isgd
* osdb
* tinyurl
