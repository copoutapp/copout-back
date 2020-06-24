`eb ssh`

add ssh to load balancer, then add https in security group inbound

source /opt/python/run/venv/bin/activate
cd /opt/python/current/app

sudo yum -y update
sudo yum-config-manager --enable epel
sudo yum -y install make automake gcc gcc-c++ libcurl-devel proj-devel geos-devel
cd /tmp
curl -L http://download.osgeo.org/gdal/2.4.4/gdal-2.4.4.tar.gz | tar zxf -
cd gdal-2.4.4/
./configure --prefix=/usr/local --without-python
make -j4
sudo make install

aws s3 cp /usr/lib64/libproj.so s3://elasticbeanstalk-us-east-2-722334429213/gdal/

cd /tmp/
aws s3 cp s3://elasticbeanstalk-us-east-2-722334429213/gdal/gdal-2.4.4-amz1.tar.gz .
sudo tar -xf gdal-2.0.0-amz1.tar.gz -C /usr/local
aws s3 cp s3://elasticbeanstalk-us-east-2-722334429213/gdal/libproj.so /usr/lib64/
export LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"
sudo ldconfig



container_commands:
  01_install_gdal:
    command: |
      source /opt/python/run/venv/bin/activate
      cd /tmp/
      aws s3 cp s3://elasticbeanstalk-us-east-2-722334429213/gdal/libproj.so .
      sudo cp libproj.so /usr/lib64/
      aws s3 cp s3://elasticbeanstalk-us-east-2-722334429213/gdal/gdal-2.4.4-amz1.tar.gz .
      sudo tar -xf gdal-2.4.4-amz1.tar.gz -C /usr/local
      export LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"
      sudo ldconfig


sudo /usr/local/bin/supervisorctl -c /opt/python/etc/supervisord.conf
