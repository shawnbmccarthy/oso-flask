FROM ubuntu:latest
LABEL authors="shawn"

ENTRYPOINT ["top", "-b"]