import sys
import os
import socket
import numpy as np
import platform
import fileinput
from sysconfig import get_paths


  
# -------------------------------------------------------
def clone_repository(path):
  """
    Clone SRoll repository from git using path given
  """
  os.system('git clone https://gitlab.ifremer.fr/iaocea/srollex.git ' +str(path)+'/srollex')
# -------------------------------------------------------
def add_host(path):
  """ 
    Function to use to add a new host in the srollex_setenv.sh 
  """

  #get host info
  hostname = socket.gethostname()
  print ("host =",hostname)  
  python_path =  str(path)+'/py_sroll/'
  print("python path =",python_path)
  
  modules =""
      
  # Read in the file
  with open(str(path)+"/srollex/srollex_setenv.sh", 'r') as file :
    filedata = file.read()

  # Replace the target string
  filedata = filedata.replace('  *)',"  "+str(hostname+"*)\n \techo \" "+hostname+" detected \" \n \texport SROLLHOST="+hostname+"\n \t "+modules+"\n \texport PYTHONPATH= "+python_path+" \n ;;\n  *)"))

  # Write the file out again
  with open(str(path)+"/srollex/srollex_setenv.sh", 'w') as file:
    file.write(filedata)
  
# -------------------------------------------------------
def init_mpi4py(path):
  """
    Download and install mpi4py and add library path to mpi libs to LD_LIBRARY_PATH
  """

  os.system('wget -P '+str(path)+'py_sroll/lib'+' https://github.com/mpi4py/mpi4py/releases/download/3.1.4/mpi4py-3.1.4.tar.gz ')
  os.system('tar -zxf '+str(path)+'py_sroll/lib/mpi4py-3.1.4.tar.gz')
  

# -------------------------------------------------------
def create_pyEnv(path):
  """
    Create sroll python virtual environement
  """

  os.system('virtualenv -p python3 ' +str(path)+'/py_sroll')
  os.system(str(path)+'/py_sroll/bin/pip install -r static/requirements.txt')

# -------------------------------------------------------
def update_Makefile(path):
  """
    Update Makefile path python and library to load for compilation
  """

  ## get python values
  id_py = platform.python_version_tuple()
  id_lib = platform.python_version()
  
  DIRPYTHONPATH = str(path)+'/py_sroll/'
  DIRPYTHONINC = '/usr/include/python3.6m'
  DIRNUMPYINC = str(path)+'/py_sroll/lib/python3.6/site-packages/numpy/core/include'
  DIRPYTHONLIB = str(DIRPYTHONPATH) + 'lib'
  LIBPYTHONLIB = 'python3.6m'
  OPTIONPYTHON = '-DPYTHON3'
  PYTHONCONF = '`python-config --ldflags` `python-config --cflags`'
  

  ## replace values in Makefile
  #for line in fileinput.input(["/export/home/tfoulquier/workspace/sroll_package/test_Makefile"], inplace=True):
  for line in fileinput.input([str(path)+"/srollex/sroll4/Makefile"], inplace=True):
      if line.strip().startswith('DIRPYTHONPATH :='):
          line = 'DIRPYTHONPATH := '+str(DIRPYTHONPATH)+'\n'
      if line.strip().startswith('DIRPYTHONINC :='):
          line = 'DIRPYTHONINC := '+str(DIRPYTHONINC)+'\n'
      if line.strip().startswith('DIRNUMPYINC :='):
          line = 'DIRNUMPYINC := '+str(DIRNUMPYINC)+'\n'
      if line.strip().startswith('DIRPYTHONLIB :='):
          line = 'DIRPYTHONLIB := '+str(DIRPYTHONLIB)+'\n'
      if line.strip().startswith('DIRPYTHONLIB :='):
          line = 'DIRPYTHONLIB := '+str(DIRPYTHONLIB)+'\n'
      if line.strip().startswith('LIBPYTHONLIB :='):
          line = 'LIBPYTHONLIB := '+str(LIBPYTHONLIB)+'\n'
      if line.strip().startswith('OPTIONPYTHON :='):
          line = 'OPTIONPYTHON := '+str(OPTIONPYTHON)+'\n'
      if line.strip().startswith('PYTHONCONF :='):
          line = 'PYTHONCONF := '+str(PYTHONCONF)+'\n'
  
      sys.stdout.write(line)


  #print python values  
  python_params = 'DIRPYTHONPATH := '+str(DIRPYTHONPATH) +'\n'+'DIRPYTHONINC := '+str(DIRPYTHONINC)+'\n'+'DIRNUMPYINC := '+str(DIRNUMPYINC)+'\n'+'DIRPYTHONLIB := '+str(DIRPYTHONLIB)+'\n'+'LIBPYTHONLIB := '+str(LIBPYTHONLIB)+'\n'+'OPTIONPYTHON := '+str(OPTIONPYTHON)+'\n'+'PYTHONCONF := '+str(PYTHONCONF) 
  print(python_params)

# -------------------------------------------------------
def install(path):
  """
    Run all routine to install SRoll at the path given
  """

  print('#########################\n## Start install SRoll ##\n#########################\n')
  
  ## git clone
  clone_repository(path)

  ##create pyEnv
  create_pyEnv(path)
  
  ## add host to srollex_setenv.sh
  add_host(path)  

  ## update Makefile -> init python path
  update_Makefile(path)  

  
# -------------------------------------------------------






