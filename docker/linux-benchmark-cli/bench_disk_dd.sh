#!/bin/bash
pth=$*

if [ "$EUID" -ne 0 ]
  then echo "[Error] Please run as root"
  exit
fi

if ! test -d ${pth}; then
  echo "Benchmark disk read/write performance by using dd on a file"
  echo "Specify directory_path as an existing folder on a mounted device"
  echo "usage: $0 directory_path"
  exit
fi

pth+="/bench_test_file.temp"

if test -f ${pth}; then
	echo "[Error] File ${pth} already exists, please check!"
	exit
fi

echo -n "Write: "
dd if=/dev/zero of=${pth} bs=2G count=1 oflag=dsync 2>&1 | grep "copied"

echo -n "Read: "
echo 3 | tee /proc/sys/vm/drop_caches > /dev/null
dd if=${pth} of=/dev/null bs=8k 2>&1 | grep "copied"
rm ${pth}
