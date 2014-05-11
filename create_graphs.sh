#!/bin/bash
source LOG_CONFIG

HOUR=3600
DAY=$((24*$HOUR))
YEAR=$((365*$DAY))

COLOR="#CC0000"

# past hour
rrdtool graph $GRAPH_DIR/hourly.png  \
--width 800 --height 200 \
--start -$HOUR  --end -1 \
--vertical-label "Temperature" \
--title "Inside temperature" \
DEF:temperature=$RRD_DB:temperature:AVERAGE \
LINE1:temperature$COLOR:"Temperature"
 
# past day
rrdtool graph $GRAPH_DIR/daily.png \
--width 800 --height 200 \
--start -$DAY  --end -1 \
--vertical-label "Temperature" \
--title "Inside temperature" \
DEF:temperature=$RRD_DB:temperature:AVERAGE \
LINE1:temperature$COLOR:"Temperature"