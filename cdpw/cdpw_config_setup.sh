#!/bin/bash
# Make sure an empty CODE_DARK is populated correctly
PATH=/bin:/usr/sbin
export TERM=dumb

# make sure /code_dark is actually mounted first.
lsmount | grep code_dark
if [[ $? -ne 0 ]]; then
 echo code_dark not mounted
 exit 0
fi

for subdir in config/orthanc database reports logs/orthanc; do mkdir -p /code_dark/$subdir; done

if [[ ! -f /code_dark/config/configurator.json ]]; then
 echo populating configurator.json
 cp /usr/share/cdpw/configurator.json /code_dark/config
fi
if [[ ! -f /code_dark/config/cdpw/orthanc.json ]]; then
 echo populating cdpw.json
 cp /usr/share/cdpw/cdpw.json /code_dark/config/orthanc
fi
if [[ ! -f /code_dark/config/orthanc/dicom_aet_port.json ]]; then
 echo dicom_aet_port.json
 cp /usr/share/cdpw/dicom_aet_port.json /code_dark/config/orthanc
fi
echo changing mode of /code_dark
chmod 700 /code_dark
echo chowning contents of /code_dark
chown -R orthanc:orthanc /code_dark
