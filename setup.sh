#!/bin/bash

if ! [ -d "ClusterSubmission" ] ; then
    git clone https://github.com/LEAF-HQ/ClusterSubmission.git
    user=$(whoami)
    cp ClusterSubmission/Settings_exampleuser.json ClusterSubmission/Settings_${user}.json
    sed -i 's/first.lastname@cern.ch//' ClusterSubmission/Settings_${user}.json
    sed -i "s/\"username\",/\"${user}\",/" ClusterSubmission/Settings_${user}.json
    mkdir jobout
fi

export PYTHON3PATH="$(pwd)/ClusterSubmission/:$PYTHON3PATH"
cd ClusterSubmission
source setup.sh
cd -
