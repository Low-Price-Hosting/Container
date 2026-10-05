#!/usr/bin/env bash
build_image() {
  cp "source/Containerfiles/$VERSION/Containerfile.default" context/Dockerfile
  publish_dockerfile context/Dockerfile --build-arg "SYSBASE=$BOOTSTRAP"
}
