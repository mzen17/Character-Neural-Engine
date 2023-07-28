#!/bin/bash
# StarlightX NFS IP for models. Only available to StarlightX team on an internal network. For external users, please use your own NFS, or place models in ./models/ directory.

NFSIP="10.42.0.145" 

if [ "$1" == "unmount" ]; then
    sudo umount -l $PWD/models
else
    sudo mount -o user -v -t nfs $NFSIP:/home/nfs/models $PWD/models
fi

# Note: It is not a good idea to keep the model on the NFS. Copy the model out of the NFS and then use it instead of using it as a NAS.
