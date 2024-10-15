import subprocess
import os

class Timer():
  def __init__(self,command,block=False,python=False) -> None:
    self.notrun=True  
    if not python:
      self.command=command
    else:
      self.command=['python',command]
    # self.command=r'C:\Users\Administrator\AppData\Roaming\Essence Goldminer3\essence.exe'
    self.pathdir= os.path.dirname(command)
    self.block=block

  def run(self)->bool:
    os.chdir(self.pathdir)
    if self.block:
      process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,encoding="utf-8")
      stdout, stderr = process.communicate()
      returncode = process.returncode
      print(stdout)
      print(stderr)
      if returncode==0:
        self.notrun=False
        return True
    else:
      process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True,encoding="utf-8")
      self.notrun=False
      return True
    return False
