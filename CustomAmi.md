# CustomAmi #

This document outlines the steps required to create a custom Ubuntu-based AMI to run fb2pdf service.

## Install AWS command-line tools ##

From synaptics package manager, select and install ruby. Make sure the following packages are being installed:

  * libruby1.8
  * ruby1.8
  * libopenssl-ruby
  * libopenssl-ruby1.8

Set environment variable in .bashrc:

  * `export RUBYLIB=/usr/lib/ruby/1.8:/usr/local/lib/1.8/i486-linux:/usr/lib/site_ruby`

Install alien package converter application:

  * `sudo apt-get install alien`

Download ec2 tools rpm:

  * http://developer.amazonwebservices.com/connect/entry.jspa?entryID=368&ref=featured

Convert rpm to deb and install:

  * `sudo alien -k ec2-ami-tools.noarch.rpm`
  * `sudo dpkg -i *.deb`

## Create Ubuntu-based AMI ##

Install Ubuntu on the disk image:

  * `dd if=/dev/zero of=ubuntu.fs count=1024 bs=1M`
  * `mke2fs -F -j ubuntu.fs`
  * `sudo mount -o loop ubuntu.fs /mnt`
  * `sudo apt-get install debootstrap`
  * `sudo debootstrap dapper /mnt`
  * `sudo cp /etc/apt/sources.list /mnt/etc/apt/sources.list`

Chroot into the image and install required packages:

  * `sudo chroot /mnt`
  * `passwd`
  * `aptitude update`
  * `aptitude upgrade`
  * `aptitude install openssh-server`
  * `aptitude install tetex-base tetex-bin tetex-extras tetex-eurosym`
  * `aptitude install python-imaging`

Create system config files:

  * `cat > /etc/network/interfaces`
```
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet dhcp
^D
```
  * `cat > /etc/fstab`
```
/dev/sda2       /mnt    ext3    defaults        1 2
/dev/sda3       swap    swap    defaults        0 0
^D
```
Download and install boto and fb2pdf:

  * http://code.google.com/p/boto/
  * http://code.google.com/p/fb2pdf/

Unmount the image:

  * `exit`
  * `sudo umount /mnt`

Initialize, upload and register the AMI:

  * `ec2-bundle-image -i ubuntu.fs -k [KEYFILE] -u [USERID]`
  * `ec2-upload-bundle -b my-ubuntu -m image.manifest -a [PUBLICKEY] -s [SECRETKEY]`
  * `ec2-register my-ubuntu/image.manifest`

## Links ##

  1. http://docs.amazonwebservices.com/AmazonEC2/dg/2006-10-01/
  1. http://developer.amazonwebservices.com/connect/thread.jspa?messageID=42535&#42535
  1. http://blog.atlantistech.com/index.php/2006/10/04/amazon-elastic-compute-cloud-walkthrough/
  1. http://www.ioncannon.net/system-administration/115/creating-your-own-fc6-instance-for-ec2/
  1. http://www.ioncannon.net/system-administration/118/debian-ec2-ami/

