# Copy daemon script
chmod +x launch.bash
cp launch.bash /usr/sbin/inpaint

# Register service
chmod +x service.bash
cp service.bash /etc/init.d/inpaint
update-rc.d inpaint defaults
service inpaint start