#!/bin/bash

which oso-cloud >/dev/null 2>&1

if [ $? -ne 0 ]; then
  echo "oso-cloud command not found. Please install oso-cloud CLI."
  curl -L https://cloud.osohq.com/install.sh | bash
  if [ $? -ne 0 ]; then
    exit 1
  fi
fi

export OSO_URL=http://localhost:9090
export OSO_AUTH=e_0123456789_12345_osotesttoken01xiIn

oso-cloud $@
