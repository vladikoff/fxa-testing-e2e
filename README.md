# fxa-testing-e2e

> A set of end-to-end tests that make sure that Firefox Accounts and Firefox Sync do not regress.

[![CircleCI](https://circleci.com/gh/vladikoff/fxa-testing-e2e/tree/master.svg?style=svg)](https://circleci.com/gh/vladikoff/fxa-testing-e2e/tree/master)

# Usage

Make sure you have Python's `virtualenv` installed.
Get latest Firefox Nightly and all the tools using by running:

```
./setup.sh
```

## Run tests

### Linux
```
./run.sh
```

### OS X 
```
./run-osx.sh
```

# Other information

* Do not defocus the Firefox browser while it is running the tests!
