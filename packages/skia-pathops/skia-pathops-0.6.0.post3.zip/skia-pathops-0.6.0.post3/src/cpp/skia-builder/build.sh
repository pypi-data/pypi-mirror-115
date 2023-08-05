#!/bin/bash

set -e

SRC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BUILD_DIR="${SRC_DIR}/build"
DIST_DIR="${SRC_DIR}/dist"

PYTHON2_EXE=${PYTHON2_EXE:-python2}
ARCH=${ARCH:-x64}

if [ "$(uname)" == "Darwin" ]; then
    PLAT=mac
else
    PLAT=linux
fi

LIBSKIA_ZIP="${DIST_DIR}/libskia-${PLAT}-${ARCH}.zip"

mkdir -p "${DIST_DIR}"

"${PYTHON2_EXE}" "${SRC_DIR}/build_skia.py" \
    --target-cpu ${ARCH} \
    ${BUILD_SKIA_OPTIONS} \
    --archive-file "${LIBSKIA_ZIP}" \
    "${BUILD_DIR}"

ls "${LIBSKIA_ZIP}"
