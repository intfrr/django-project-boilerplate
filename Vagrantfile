# Vagrant Up config

Vagrant.configure("2") do |config|
    config.vm.box = "debian-72"
    config.vm.box_url = "https://dl.dropboxusercontent.com/u/197673519/debian-7.2.0.box"
    config.vm.network "forwarded_port", guest: 8000, host: 8000
    config.vm.synced_folder "src/", "/home/vagrant/src/"
end
