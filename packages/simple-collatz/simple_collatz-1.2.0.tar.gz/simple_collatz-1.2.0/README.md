# Simple Collatz

A simple python package for plotting the collatz conjecture.
*Warning: may be pointless*

## Development

To setup a dev environment:

  - Clone this repo
  - (Optional) setup a Python virtual environment
  - `pip install -r requirements.txt`

## Installation and Usage

### Installation

Simple Collatz can be installed by running `pip install simple-collatz`, or by installing from a wheel package, included in the latest release.

If you can't wait for the latest *hotness* and want to install from GitHub, use:

pip install `git+git://github.com/appcreatorguy/collatz`

### Alternative Installation

For a python-free installation, the standalone binaries can be downloaded from the latest release and run in the same way.

### Usage

To get started:

```sh
simple_collatz
```

If this doesn't work, you can try running Simple Collatz as a script instead:

```sh
python -m simple_collatz
```

The program will then begin to iterate over the collatz conjecture.
To stop and view your results at any time, raise a keyboard interrupt with `Ctrl + C`. The 2 graphs will then populate *(this may take some time depending on the amount of iterations you have computed!*) with the stopping time and the values of the collatz conjecture so far.

## Change Log
See [CHANGES.md](https://github.com/appcreatorguy/collatz/blob/master/CHANGES.md)