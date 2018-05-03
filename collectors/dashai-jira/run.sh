#!/bin/bash

if [ -n "$JIRA_INFLUX_CONFIG_JSON" ]; then
    echo "$JIRA_INFLUX_CONFIG_JSON" > ./config.json
fi

go-wrapper run
