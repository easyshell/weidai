
PATH="/usr/lib64/qt-3.3/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin"
export $PATH
export LD_LIBRARY_PATH=/usr/local/lib
root=$(cd "$(dirname "$0")"; pwd)
project_home=$root
cd $project_home;
rm -f weidaiweb.log
nohup scrapy crawl weidaiweb > weidaiweb.log  2>&1 &
sleep 10m
python weidai_crawl_monitor.py
