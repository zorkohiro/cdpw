HOW tO BUILD

1. Install and run on Ubuntu 24.04. Set up as some
non-orthanc name as the build user, Your favorite
login name is fine.

2. Make a password-less sudo for the whoever is the build user.

This is unfortunately now required for building the OHIF
plugin for orthanc.

3. Install these packages with apt:

	build-essential
	cmake
	libboost-all-dev
	libcharls-dev
	libcurl4-openssl-dev
	libdcmtk-dev
	libgtest-dev
	libjpeg-dev
	libjsoncpp-dev
	liblua5.3-dev
	libpng-dev
	libpugixml-dev
	libsqlite3-dev
	libssl-dev
	libwrap0-dev
	locales
	mercurial
	orthanc-dev
	patch
	protobuf-compiler
	unzip
	uuid-dev
	zlib1g-dev

4. Set up docker for users to run

Install docker, such that you as a normal user can run docker.

sudo apt install -y curl apt-transport-https ca-certificates software-properties-common
sudo apt install -y docker.io
sudo usermod -aG docker $USER
<reboot>
docker run hello-world

5. At this directory level, issue the command 'make'

The packages needed for installation on a prepared USB key
running Ubuntu 24.04 will end up in the created artifacts
directory.
