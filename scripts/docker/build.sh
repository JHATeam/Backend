#!/usr/bin/env bash

set -xeu
BUILD_DIR=${BUILD_DIR:-.}
CURRENT_GIT_SHA=$(git rev-parse --short HEAD)
GITHUB_SHA=${GITHUB_SHA:-$CURRENT_GIT_SHA}

BASE_IMAGE_TAG=$(echo "$GITHUB_SHA" | cut -c1-7)

# if DOCKERFILE is set add to DOCKER_BUILD_OPTS
if [[ -n "${DOCKERFILE:-}" ]]; then
  DOCKER_BUILD_OPTS="${DOCKER_BUILD_OPTS:-} -f ${DOCKERFILE}"
fi

# we want the build options to expand
# shellcheck disable=SC2086
DOCKER_BUILDKIT=1 docker build ${DOCKER_BUILD_OPTS:-} \
  --build-arg BUILDKIT_INLINE_CACHE=1 \
  -t "${IMAGE_BASE}" -t "${IMAGE_BASE}:${BASE_IMAGE_TAG}" \
  "$BUILD_DIR"

