import os
import socket

# Freebox configuration
freebox_api_version = 'v3'

# Host application configuration
app_version = '1.0'
app_name = 'freepy'
dev_name = socket.gethostname()

# Application token file name and location
app_token_filename = 'app_auth'
dirpath = os.path.dirname(os.path.abspath(__file__))
app_token_file_path = os.path.join(dirpath, app_token_filename)

# HTTP Request configuration
http_timeout = 10
