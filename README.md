# Try_hard_Code
tesst
# cài zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

nano ~/.zshrc   => tìm ZSH_THEME="robbyrussell"   và đổi thành => ZSH_THEME="agnoster"

#cài giao diện cho vps linux
sudo apt update
sudo apt install xfce4 xfce4-goodies -y

sudo apt install xrdp -y
sudo systemctl enable xrdp
sudo systemctl start xrdp

sudo ufw allow 3389/tcp

