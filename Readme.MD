# .adicht Signal to .csv Exporter

[![GitHub Release](https://img.shields.io/github/release/science-open/adicht-signal-to-csv-exporter.svg?style=flat)](https://github.com/SCIENCE-OPEN/adicht-signal-to-csv-exporter/releases)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-3.0.en.html)
[![Ask Me Anything !](https://img.shields.io/badge/Ask%20about-anything-1abc9c.svg)](https://github.com/adicht-signal-to-csv-exporter/adicht-signal-to-csv-exporter/issues/new/choose)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
![Badge](https://hitscounter.dev/api/hit?url=https%3A%2F%2Fgithubcom%2Fscience-open%2Fadicht-signal-to-csv-exporter&label=Visitors&icon=suit-heart-fill&color=%23e35d6a)

The script requires first argument directory where recursivelly find `.adicht` files or is required path to single `.adicht` file. Second argument is required output directory. For each `.adicht` file on the input the script exports the channels according to provided channel-suffix mapping to separated `.csv` files to the output directory. Nested structure from the input to output is not followed!

The names of created `.csv` files will be taken from the name of `.adicht` file according to default channel-suffix mapping `r:0,g:2` and the default delimeter `,` (e.g. the `channel 0` if not evaluated as flat from the file `AC17654r, AC17657g.adicht` will be written to the file `AC17654.csv` and `channel 2` to `AC17657.csv`).

# Features

- When splitting by separator found only 1 specimen ID (e.g. using default comma separator and filename `AC17654r.adicht`) and mapping point to flat signal, then is assigned first not flat signal

# Usage

```
root@a55904f85091:/src# wine python adicht-signal-to-csv-exporter.py --help
usage: adicht-signal-to-csv-exporter.py [-h] [--sep SEP] [--suffix-map SUFFIX_MAP] src_path dest_dir_path

positional arguments:
  src_path              Path to source directory or single .adicht file
  dest_dir_path         Path to destination directory for .csv output file or files

options:
  -h, --help            show this help message and exit
  --sep SEP             Delimiter used to split specimen entries in filenames (default is comma)
  --suffix-map SUFFIX_MAP
                        Mapping of specimen suffixes to channel numbers, e.g. r:0,g:2
```

# Changelog

[CHANGELOG.md](CHANGELOG.md)

# Dependencies

- python3.11

and

- adi-reader (requires Windows)
- pandas
- numpy

For python dependencies, take a look at [requirements.txt](requirements.txt).

# Requirements

- [Windows](#Windows)

or

- using [Docker](#Docker) (recommended)

or

- using [CrossOver](#CrossOver)

# Installation

## Windows

### Using Conda (recommended)

- create conda env for python3.11 `$ conda create --name myenv python=3.11` (python3.11 is necessary because pip package [adinstruments_sdk_matlab](https://github.com/JimHokanson/adinstruments_sdk_matlab) is built for python3.11)
- activate conda env `$ conda activate myenv`
- install pip packages `$ pip install -r requirements.txt`

## Docker

- build container `$ docker build -t for-adicht-signal-to-csv-exporter .` from the [Dockerfile](Dockerfile) (when moving to another directory make sure the script `adicht-signal-to-csv-exporter.py` and files `requirements.txt` and `requirements.windows.txt` were passed inside)
- run container `$ docker rm -f for-adicht-signal-to-csv-exporter && docker run -p 5000:5000 -it --name for-adicht-signal-to-csv-exporter -v ./examples/:/src/examples/for-adicht-signal-to-csv-exporter`
- run inside container `$ mkdir output && wine python /src/adicht-signal-to-csv-exporter.py ...`

The [Dockerfile](Dockerfile) is prepared for running a `python3` code with possibility debug it using port `5678`, just uncomment lines below marks `#debugging only` (e.g. VS code is able attach to running container and use breakpoints).

## CrossOver

- setup [CrossOver](https://www.codeweavers.com/crossover)
- create bottle Windows10 64-bit (**when using a free trial is required to repeat steps starting this one after 14 days**)
- install [python-3.11.9-amd64](python-3.11.9-amd64.exe) using CrossOver custom application .exe feature (python3.11 is necessary because pip package [adinstruments_sdk_matlab](https://github.com/JimHokanson/adinstruments_sdk_matlab) is built for python3.11)
- install [Git-2.47.0.2-64-bit.exe](Git-2.47.0.2-64-bit.exe) (or get newest [here](https://git-scm.com/downloads/win)) using CrossOver custom application .exe feature (reboot when progress was stuck at post-install helped)

- move [get-pip.py](get-pip.py) (or get newest [here](https://bootstrap.pypa.io/get-pip.py)) to folder `~/Downloads` of laptop to which one was installed CrossOver
- move [requirements.txt](requirements.txt) to folder `~/Downloads` of laptop to which one was installed CrossOver
- move [adicht-signal-to-csv-exporter.py](adicht-signal-to-csv-exporter.py) to folder `~/Downloads` of laptop to which one was installed CrossOver

- open inside CrossOver Git Cmd `$ cd C:\users\crossover\Downloads`
- install pip `$ python3 get-pip.py`
- install pip packages `$ pip3 install -r requirements.txt`

# Examples

```
root@a55904f85091:/src# wine python adicht-signal-to-csv-exporter.py examples examples --sep=";" --suffix-map="r:2,g:0"
Loaded examples\subdir\G81r; G94g.adicht
Created examples\G81.csv
Created examples\G94.csv

root@a55904f85091:/src# wine python adicht-signal-to-csv-exporter.py examples examples --sep=";" --suffix-map="r:2"
Loaded examples\subdir\G81r; G94g.adicht
Created examples\G81.csv

root@a55904f85091:/src# wine python adicht-signal-to-csv-exporter.py examples examples --sep=";" --suffix-map="r:1"
Loaded examples\subdir\G81r; G94g.adicht
Error accessing channel 1 in examples\subdir\G81r; G94g.adicht: # of samples requested is less than 1
? Skipping G81r; G94g: no usable signal found.

root@5af19b760131:/src# wine python adicht-signal-to-csv-exporter.py examples examples --suffix-map="r:1"
Loaded examples\subdir\CP058R.adicht
Error accessing channel 1 in examples\subdir\CP058R.adicht: # of samples requested is less than 1
No suffix match. Trying fallback for single ID: CP058R
Created examples\CP058R.csv (from channel 0)
```

# TODO:

## CrossOver

- `$ git bash` does not open inside crossover, display error with title `mintty`, `Font not found, using system substitute: Courier New` (does not work autocompletion of dir names)