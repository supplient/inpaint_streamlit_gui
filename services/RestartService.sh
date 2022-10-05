sudo cp ./inpaint.service /etc/systemd/system
sudo chkconfig inpaint --add

sudo service inpaint restart