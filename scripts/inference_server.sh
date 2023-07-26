if [ ! -d "lib" ]; then
    echo "Please run this in the root directory, with ./scripts/inference_server.sh."
    exit
fi

if [ "$1" == "install" ]; then
    mkdir ./models
    ./scripts/mount.sh
    cp ./models/llama-13B.q4_0.bin ..
    ./scripts/mount.sh unmount
elif [ "1" == "mount-only" ]; then
    mkdir ./models
    ../scripts/mount.sh
fi

pwd
ls

if [ "$1" == "cpu" ]; then
    ./lib/cpuserver -m ./models/llama-13B.q4_0.bin -c 2048 -t $2
elif [ "$1" == "gpu" ]; then
    ./lib/gpuserver -m ./models/llama-13B.q4_0.bin -c 2048 -t $2 -ngl $3
else
    echo "Please Specify Device"
fi