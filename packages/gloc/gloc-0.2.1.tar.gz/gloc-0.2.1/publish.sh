#! /bin/bash

python -m unittest discover ./tests && flit publish
