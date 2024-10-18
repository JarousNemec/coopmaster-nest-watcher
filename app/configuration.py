import os

host = "127.0.0.1"
port = 9007
hello_message = "Hello from nest watcher"

log_file_name = "nest_watcher.log"

def get_log_directory():
    return "./logs/"

def get_log_filename():
    return log_file_name