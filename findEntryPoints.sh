#!/bin/bash

# Author: Tapti Palit
# Usage
# ./findEntryPoints.sh github.com/hashicorp/consul
# python extractsyscall.py github.com.hashicorp.consul/

set -x

toplevelpkg=$1

curdir=`pwd`

toplevelfilter="${toplevelpkg//../}"
toplevelfilter="${toplevelfilter//~/}"
echo $toplevelfilter
toplevelout="graph${toplevelfilter//\//.}"
echo $toplevelout
rm -rf $toplevelout
mkdir -p $toplevelout

#cd ~/go/src/
cd $toplevelpkg

mainpkgs=`find . -name "*.go" | xargs grep -rl " main()"`

for mainpkg in $mainpkgs
do
    echo $mainpkg
    dir="$(dirname "${mainpkg}")"
    cd $dir
    mainpkg="${mainpkg//.\//}"
    filename="${mainpkg//\//.}"
    echo $filename
    $curdir/callgraph -format=graphviz . > $curdir/$toplevelout/$filename".callgraph"
    cd $toplevelpkg
done


