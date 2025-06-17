  Alpha 1.0 Notes, version 2
 Mon Jun 16 05:40:12 PM PDT 2025


This is the source repository for building kp-report which is
the add on software to an Ubuntu 24.04 based system that
will run Orthanc for the Code Dark PACS Workstation project
at Kaiser Northern California.

Documentation over what Code Dark is may be found under
the Documentation directory.

This source tree can be built under Ubuntu 24.04 and a
bootable USB key can be made from it. Instructions
for making the key is also under Documentation.

Code DARK PACS Workstation requires an additional
USB storage device which is a secure APRICORN device
which has a key pad to unlock. This is for patient
data storage. That needs to be formatted a
specific way. Instructions under Documentation.

BUILD INSTRUCTIONS

The entire package consists of the 3 main pieces:

 1 Build kp-report package

   See OHIFPlugin/BUILD and ReportPlugin/BUILD for
   build requirements for building under Ubuntu 24.04.
   It should go without saying that this is a system
   separate from CDPW- a real workstation with a real
   disk. Any reasonable 64 bit Intel/AMD system will do.
   You type 'make' in this directory and the output
   should be a .deb file in this directory.

 2 Build modified kernel drivers for Barco adapters
   <This documentation does not exist yet> the
   output of this will be a tarball of .deb packages
   for installing on the USB key Ubuntu system.

 3 Ubuntu USB key

   A Ubuntu 24.04 system loaded onto a USB key and
   then modified in certain specific ways to accommodate
   the somewhat transient requirements of CDPW.
   See Documentation for instructions.

   The documentation will instruct you how to install to
   a USB key Ubuntu 24.04, take the kp-report package built
   above and install it, add the kernel driver changes needed
   and do additional changes that the Ubuntu system needs to
   run the code developed here.

   The resultant USB key may be considered a 'gold' image
   for a specific release and copied off to a disk file
   and archived and either via the disk file or copying
   the actual created USB key may be replicated and sent
   out to stay with each reserved CDPW workstation for
   use when needed.
