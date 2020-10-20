#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

nuctl deploy --project-name cvat \
    --path "$SCRIPT_DIR/opencv/ellipse_detection/nuclio" \
    --platform local

nuctl get function --platform local
