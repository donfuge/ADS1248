#!/bin/bash
source $(dirname $0)/LOG_CONFIG

TEMP=$($GET_TEMP)
rrdtool update $RRD_DB N:$TEMP 