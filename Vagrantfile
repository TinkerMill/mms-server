# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.define "puzzleClient" do |pc|
    pc.vm.box = "ubuntu"
    pc.vm.box_url = "http://goo.gl/8kWkm"

    config.vm.provision :shell, :inline => "/usr/bin/apt-get update"
    
    #pc.vm.provision "puppet" do |p|
    #  p.manifest_file = "desktop.pp"
    #end

    pc.vm.network    "private_network", ip: "192.168.0.30"
    pc.vm.hostname = "dooraccess"
  end


end
