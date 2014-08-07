# Vagrant Up config

Vagrant.configure("2") do |config|
    config.vm.box = "chef/debian-7.4"
    config.vm.network "forwarded_port", guest: 8000, host: 8000
    config.vm.synced_folder "src/", "/home/vagrant/src/"
end
