#!/bin/bash

NFSIP="10.42.0.145"  # Replace with your NFS server's IP address

if [ "$1" == "unmount" ]; then
    sudo umount -l $PWD/models
else
    sudo mount -o user -v -t nfs $NFSIP:/home/nfs/models $PWD/models
fi
