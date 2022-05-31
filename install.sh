#!/bin/bash
###################

echo -e "\n\033[0;32m >> Install Requirements\033[0m"

if ! hash ansible >/dev/null 2>&1; then
    echo "Installing Ansible..."
    sudo apt-get update  2>&1 >/dev/null
    sudo apt-get install software-properties-common ansible git python3 python3-pip -y
    # sudo /usr/bin/pip install -U ansible prompter
    # sudo /usr/bin/pip install -U ansible
else
    echo "Ansible already installed"
fi
sudo apt-get install nano -y

#if [ ! -d "$HOME/ansible-telepito" ]; then
if [ ! -d "/opt/Ansible_Ubuntu_Admin_crypt_root" ]; then
        echo -e  "\n\033[0;32m >> Clone Ansible_Ubuntu_Admin\033[0m"
        git clone https://github.com/dynerose/Ansible_Ubuntu_Admin_crypt_root.git "/opt/ansible_setup"
else
        echo -e "\n\033[0;32m >> Ansible_Ubuntu_Admin is already available\033[0m"
fi
cd "/opt/Ansible_Ubuntu_Admin_crypt_root"
# echo -e "\n\033[0;32m >> Run Wizard\033[0m"
# python scripts/wizard.py <&1
echo -e "\n\033[0;32m >> Installing ...\033[0m"
#ansible-playbook -i inventory/server-headless -c local -K htpc-server.yml

#####################################
# Display real installation process #
echo ""
echo "Customize the playbook playbook.yml to suit your needs, then run ansible with :"
echo "  ansible-playbook playbooks/0.Test.yml --ask-become-pass"
echo ""
