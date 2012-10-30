Vagrant::Config.run do |config|

  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  config.vm.network :hostonly, "10.10.10.10"

  config.vm.customize ["modifyvm", :id, "--rtcuseutc", "on"]
  config.vm.share_folder("v-root", "/vagrant", ".", :nfs => true)

  config.vm.provision :chef_solo do |chef|

    chef.cookbooks_path = "cookbooks"

    chef.add_recipe "main"
    chef.add_recipe "python"
    chef.add_recipe "postgresql"

    chef.json.merge!({
      :project_name => "pypit",
      :user => {
        :username => "vagrant",
        :group => "user",
        :ssh_key => "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAyvlx1vsA7Bkf5gM/88GtMhHAuQjNa//eD/Yoz+xPS7u7YF5gBnRh/0K+Jw10EMF0njQpOO1iH1RjMPQyrSZ/X0bwta7wHiTy+ET7PlPkwlzF2rFzDxuPxelzd3qo7AzkWrXwl27JRlTZpoh84ZmXWdQqF1JFog1vJbfR01mqO6//iHy9f8PIIHp+nnzWG17zZNnVHBhYRh4KKLMCeaUQYtYs8rIEl+kF+XZ59TFBDieZ6/vU0XBYS/PfFNpayxdUsyNcBcCrmHbKybuQ7skeJXIkSiFDqDnclKajtOTSTIJPOjL2uSZWFfeh4+XMJEe6XE1b/stg19HB4nJWxOiniQ== dougal85@gmail.com",
      },
    })

  end

end