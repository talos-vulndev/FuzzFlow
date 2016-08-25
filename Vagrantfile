Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  #config.vm.network "forwarded_port", guest: 80, host: 1080
  #config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.network "private_network", type: "dhcp"
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    vb.cpus = "2"
    #vb.customize ["modifyvm", :id, "--nictype1", "Am79C973"]
    #vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    #vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
  end

  config.vm.provision "shell", privileged: false, path: "vagrant.sh"
end