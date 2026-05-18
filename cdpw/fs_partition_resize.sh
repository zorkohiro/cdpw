#!/bin/bash
export PATH=/usr/sbin:/usr/bin:/usr/local/bin
LOG=/tmp/fs_resize_partition.log
{
  # lsmount won't work without TERM being set (!!)
  export TERM=dumb
  set -o pipefail
  # Find out whether there is any code_dark device available
  cfull=$(blkid|grep CODE_DARK|sed 's/:.*$//')
  if [[ -z "${cfull}" ]]; then
    echo No CODE_DARK labeled device seen
    exit 0
  fi
  # See if we are inhibited from resize
  if [[ -f /noresize ]]; then
    echo Resizing inhibited
    exit 0
  fi
  # Find the code_dark device and find out whether it has any unpartioned space to fill
  echo code_dark full device is $cfull
  cdev=$(echo $cfull | sed 's/[1-9]*$//')
  echo code_dark base device is $cdev 
  part=$(echo $cfull | sed "s,$cdev,,")
  echo code_dark part is $part
  unpartitioned_space=$(sfdisk $cdev --list-free |grep Unpart|awk ' { print $(NF-1)}')
  echo unpartitioned space in sectors is $unpartitioned_space
  if [[ $unpartitioned_space -eq 0 ]]; then
    echo "no unpartitioned space to add"
    exit 0
  fi
  o_active=$(systemctl is-active orthanc.service)
  if [[ $o_active == "active" ]]; then
    echo "attempting to stop orthanc"
    systemctl stop orthanc
    if [[ $? -ne 0 ]]; then
      echo "was unable to stop orthanc service"
      exit 1
    fi
  else
    echo "orthanc not active"
  fi

  is_mounted=no
  lsmount | grep -q code_dark
  if [[ $? -eq 0 ]]; then
    echo "attempting to unmount /code_dark"
    is_mounted=yes
    umount /code_dark
    if [[ $? -ne 0 ]]; then
      echo "was unable to unmount /code_dark"
      exit 1
    fi
  else
    echo "/code_dark not mounted"
  fi

  echo make sure GPT is correct
  echo w | fdisk $cdev

  echo attempting to resize $cdev part $part
  parted -s $cdev resizepart $part 100%
  if [[ $? -ne 0 ]]; then
    echo did not resize the partition successfully
    exit 1
  fi

  e2fsck -y -f $cfull
  if [[ $? -ne 0 ]]; then
    echo did not pass e2fsck of $cfull
    exit 1
  fi

  resize2fs $cfull
  if [[ $? -ne 0 ]]; then
    echo did not pass resize2fs of $cfull
    exit 1
  fi
  if [[ $is_mounted == "yes" ]]; then
    echo attempting to remount /code_dark
    mount /code_dark
    if [[ $? -ne 0 ]]; then
      echo was not able to remount /code_dark
      exit 1
    fi
  fi
  if [[ $o_active == "active" ]]; then
    echo attempting to restart orthanc
    systemctl restart orthanc
    if [[ $? -ne 0 ]]; then
      echo was not able to restart orthanc
      exit 1
    fi
  fi
  exit 0
} > $LOG 2>&1
