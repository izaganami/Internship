## Show doc
#firefox https://docs.opencv.org/master/d7/d9f/tutorial_linux_install.html &

## Clean standard version
#dnf erase opencv -y

## Download opencv
#mkdir /local/data/line/opencv/
#cd /local/data/line/opencv/
#git clone https://github.com/opencv/opencv.git
#git clone https://github.com/opencv/opencv_contrib.git

## Install 
#cd /local/data/line/opencv/opencv
#git checkout 4.2.0
#/bin/rm -rf build
#mkdir build
#cd build
#cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local .. 2>&1 | tee cmake.log.txt
#make | tee -a cmake.log.txt
# sudo make install

## Test
opencv_version


