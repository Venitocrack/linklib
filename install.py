import os
import inspect
import sys

init_file = open('linklib\\__init__.py')
utils_file = open('linklib\\utils.py')
connects_file = open("linklib\\connects.py")

print('copyng files')
files = {
  "init":init_file.read(),
  "utils":utils_file.read(),
  "connects":connects_file.read()
}

init_file.close()
utils_file.close()
connects_file.close()

def get_libdir():
  if not('LIB' in os.environ):
    os_dir = inspect.getfile(os)
    os_dir += '\\site-packages\\'
    return os_dir 
  else:
    return os.environ['LIB']

print('installing...')
dir = f'{get_libdir()}\\linklib'
os.makedirs(f'dir',exists_ok=True)
init_file = open(dir + '\\__init__.py','w')
utils_file = open(dir + '\\utils.py','w')
connects_file = open(dir + '\\connects.py','w')

print('extracting...')
init_file.write(files['init'])
utils_file.write(files['utils'])
connects_file.write(files['connects'])

print('succes!!!')

