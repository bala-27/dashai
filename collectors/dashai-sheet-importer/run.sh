#!/bin/bash

if [ -n "$SHEETS_INFLUX_CLIENT_SECRET_JSON" ]; then
    echo "$SHEETS_INFLUX_CLIENT_SECRET_JSON" > ./client_secret.json
fi

if [ -n "$SHEETS_INFLUX_TOKEN_JSON" ]; then
    echo "$SHEETS_INFLUX_TOKEN_JSON" > ./token.json
fi

shift
go-wrapper run "$@"
