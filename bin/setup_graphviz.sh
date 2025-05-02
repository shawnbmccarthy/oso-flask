#!/bin/bash

# this is simple script to setup graphviz on mac
# only really needed if we want to generate erd
# TODO: validate testing as needed
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

. .venv/bin/activate

GRAPHVIZ_PREFIX=$(brew --prefix graphviz)

pip install --use-pep517 \
    --config-settings="--global-option=build_ext" \
    --config-settings="--global-option=-I$GRAPHVIZ_PREFIX/include/" \
    --config-settings="--global-option=-L$GRAPHVIZ_PREFIX/lib/" \
    pygraphviz

pip install -r requirements-dev.txt

deactivate