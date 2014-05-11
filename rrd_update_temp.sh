#!/bin/bash
source LOG_CONFIG

TEMP=$($GET_TEMP)
rrdtool update $RRD_DB N:$TEMP 