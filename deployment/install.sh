# bash <(curl https://raw.githubusercontent.com/hardworkingcoder/dw_experiments/master/deployment/install.sh)
git clone git@github.com:hardworkingcoder/dw_experiments.git dw_experiments_dev
cd ~/dw_experiments_dev
virtualenv --python=/usr/bin/python2 env
source env/bin/activate
python -m pip install -r requirements.txt
sudo cp ~/dw_experiments_dev/deployment/etc_nginx_sites_available_dw_experiments_dev_hardworkingcoder_com /etc/nginx/sites-available/dw_experiments_dev.hardworkingcoder.com
sudo ln -s /etc/nginx/sites-available/dw_experiments_dev.hardworkingcoder.com /etc/nginx/sites-enabled/dw_experiments_dev.hardworkingcoder.com
sudo mkdir /etc/uwsgi/
sudo mkdir /etc/uwsgi/sites
sudo cp ~/dw_experiments_dev/deployment/dw_experiments_dev.ini /etc/uwsgi/sites/dw_experiments_dev.ini
sudo cp ~/dw_experiments_dev/deployment/uwsgi.service /etc/systemd/system/uwsgi.service
sudo systemctl daemon-reload
sudo systemctl restart uwsgi
sudo service nginx restart