# ABRicateToPhandango
A script to convert an [ABRicate](https://github.com/tseemann/abricate) summary to a suitable format for [phandango](https://jameshadfield.github.io/phandango/#/) visualisation.

### Required input

This script requires a summary.tsv file created using the `--summary` flag with ABRicate and also a specified cut off value for the %COVERAGE for a gene to be considered present.

### Usage

`abricate_to_phandango.py -i summary.tsv -o output -c 95`
