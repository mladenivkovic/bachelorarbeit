#!/bin/bash

#since git has trouble with following symbolic links
#and I can't put on a hart link on selfmade executables
#because they're on another device, this script will
#copy all the selfmade executables here.


cp /zbox/user/mivkov/source/executables/selfmade/* .
echo "done"
