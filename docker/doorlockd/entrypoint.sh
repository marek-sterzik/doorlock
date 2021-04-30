#!/bin/bash

if [ -z "$DOORLOCK_KEY" ]; then
    /app/doorlockd -p 80 -d
else
    /app/doorlockd -p 80 -d -k "$DOORLOCK_KEY"
fi
