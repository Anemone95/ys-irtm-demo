export INSTALL_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
sudo pip3 install -r $INSTALL_DIR/requirements.txt
chmod +x $INSTALL_DIR/light_mqtt.py
sudo ln -f $INSTALL_DIR/lightmqtt.service /etc/systemd/system/lightmqtt.service
sudo ln -s -f $INSTALL_DIR/light_mqtt.py /usr/local/bin/light_mqtt
sudo chmod 777 /usr/local/bin/light_mqtt

sudo systemctl daemon-reload
sudo systemctl enable lightmqtt.service
sudo systemctl start lightmqtt.service 
