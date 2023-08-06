# Splunk AppInspect

This repo is hosted [here on Gitlab](https://cd.splunkdev.com/appinspect/appinspect-cli)
and configured to mirror (push to) the [repo on Github](https://github.com/splunk/appinspect)
to make use of the Github Windows runner for testing on Windows.

All commits should be made to the repo on Gitlab.

## Build Status

![Pipeline Status](https://cd.splunkdev.com/appinspect/appinspect-cli/badges/main/pipeline.svg)

## Overview

AppInspect is a tool for assessing a Splunk App's compliance with Splunk recommended development practices, by using static analysis. AppInspect is open for extension, allowing other teams to compose checks that meet their domain specific needs for semi- or fully-automated analysis and validation of Splunk Apps.

## Documentation

You can find the documentation for Splunk AppInspect at http://dev.splunk.com/goto/appinspectdocs.

## Local Development

Use the following steps to setup AppInspect for local development.
### Install from source
* Checkout the source code
* Create and activate a [virtual env](http://docs.python-guide.org/en/latest/dev/virtualenvs)
* Build and install from source
	- install libmagic (`brew install libmagic` on macOS)
	- `make install`, if you see any error like `ValueError: bad marshal data`, try run `find ./ -name '*.pyc' -delete` first.
	**Caution**: Do not delete the pyc file below which is used for tests.
	 `test/unit/packages/has_disallowed_file_extensions/has_pyc_file/configuration_parser.pyc`
	- That's it. The `splunk-appinspect` tool is installed into your virtualenv. You can verify this by running the following commands:
   		- `splunk-appinspect`
    	- `splunk-appinspect list version`

### Run CLI directly from codebase
* Install all dependencies, `pip install -r (windows|darwin|linux).txt`, it depends on your system platform
* Add current folder into PYTHONPATH, `export PYTHONPATH=$PYTHONPATH:.`
* Run the CLI, `scripts/splunk-appinspect list version`

### Build the distribution package
* Create a distribution of AppInspect
    - `make build` 
    - after running the above command, an installation package with name like `splunk-appinspect-<version>.tar.gz` is created under the `dist` folder
* Install the distro previously created
    - `pip install dist/splunk-appinspect-<version>.tar.gz`


### Run tests
Once you have the `splunk-appinspect` tool installed, you can run tests by following the steps below.

* Install the Unit & Integration Test Requirements
    - `pip install -r test/(windows|darwin|linux).txt`, it depends on your system platform
* Ensure the Unit tests pass
    - `pytest -v test/unit/`
