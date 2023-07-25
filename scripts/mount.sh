#!/bin/bash

NFSIP="10.42.0.145"  # StarlightX NFS IP for models. Only available to StarlightX team on an internal network. For external users, please use your own NFS, or place models in ./models/ directory.

if [ "$1" == "unmount" ]; then
    sudo umount -l $PWD/models
else
    sudo mount -o user -v -t nfs $NFSIP:/home/nfs/models $PWD/models
fi
