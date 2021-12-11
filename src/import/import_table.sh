#!/bin/bash

file=$1
name=$2
sqlite3 WCA.db <<EOF
.mode ascii
.separator "\t" "\n"
.import ${file} ${name}
.quit
EOF


