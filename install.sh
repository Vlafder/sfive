#!/bin/bash -i

DIR="$( cd "$( dirname "$0" )" && pwd )"

#sudo apt update
#sudo apt -y upgrade

sudo apt install python3-venv
sudo apt install python3-pyqt5
sudo gpasswd --add ${USER} dialout

sudo apt install pyqt5-dev-tools


#create virtual inviorment
python3 -m venv .venv

#enter virtual inviorment
source .venv/bin/activate 
    pip install numpy
    pip install matplotlib
    pip install pyqt5
    pip install pyqt5-tools
    pip install pyyaml
    pip install pyqtgraph
    pip install control
    pip install QtAwesome
    pip install pyserial
    pip install pyqtgraph
    pip install xlwt
 



cd /etc/udev/rules.d
sudo touch sfive.rules
echo 'KERNEL=="ttyACM0", MODE="0666"' | sudo tee sfive.rules
sudo chmod 666 /dev/ttyACM0


FILE="sfive.desktop"

if [ -f "$FILE" ] ; then
    rm "$FILE"
fi

echo -e "[Desktop Entry]" >> $FILE
echo -e "Version=1.0" >> $FILE
echo -e "Encoding=UTF-8" >> $FILE
echo -e "Type=Application" >> $FILE
echo -e "Terminal=false" >> $FILE
echo -e "Name=sFive" >> $FILE
echo -e "Exec=$DIR/startup.sh" >> $FILE
echo -e "Comment='semester five common gui'" >> $FILE
echo -e "Icon=$DIR/icons/sfive.png" >> $FILE
echo -e "Name[en]=sFive" >> $FILE

sudo chmod +x "sfive.desktop"
cp $FILE ~/Desktop
sudo cp $FILE /usr/share/applications
rm "$FILE"