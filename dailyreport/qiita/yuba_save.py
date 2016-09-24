import sys
import time
from jubatus.recommender import client

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9199
NAME = "recommender_qiita"


r_client = client.Recommender(SERVER_IP, SERVER_PORT, NAME)
try:
	r_client.save(sys.argv[1])
except:
	r_client.save(time.strftime("%Y%m%d_%I%M%S", time.localtime()))
	
