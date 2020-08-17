from django.test import TestCase

# Create your tests here.

from fdfs_client.client import Fdfs_client,get_tracker_conf
trackers = get_tracker_conf(r'/home/wangjun/my_projects/drf_meiduo/drf_meiduo/utils/fastdfs/client.conf')
client = Fdfs_client(trackers)
ret = client.upload_by_filename('/home/wangjun/my_projects/drf_meiduo/drf_meiduo/static/hg.jpg')
print(ret)