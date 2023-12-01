#!/bin/bash

rm -rf workdir || echo "Nothing to clean"
mkdir workdir && cp -a src/* workdir/ 
docker run --rm -ti -u 1000:1000 -v `pwd`/workdir:/AFLplusplus/workdir -w /AFLplusplus/workdir aflplusplus/aflplusplus
