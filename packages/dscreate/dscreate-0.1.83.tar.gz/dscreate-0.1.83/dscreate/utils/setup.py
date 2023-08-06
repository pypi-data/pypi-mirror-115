import os
import subprocess
from IPython.display import clear_output


def run_bash_command(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    process.communicate()

def spark_setup():
  print('Setting up PySpark.')
  run_bash_command('pip install tqdm -q')
  from tqdm import tqdm
  pbar = tqdm(total=7)
  run_bash_command('apt -qq update ')
  clear_output()
  print('Updating system configurations.')
  pbar.update(1)
  run_bash_command('apt-get install openjdk-8-jdk-headless -qq')
  clear_output()
  print('Downloading spark-2.4.8-bin-hadoop2.')
  pbar.update(1)
  run_bash_command('wget -q https://downloads.apache.org/spark/spark-2.4.8/spark-2.4.8-bin-hadoop2.7.tgz')
  clear_output()
  print('Unzipping file')
  pbar.update(1)
  run_bash_command('tar xf spark-2.4.8-bin-hadoop2.7.tgz')
  clear_output()
  print('Installing findspark')
  pbar.update(1)
  run_bash_command('pip install -q findspark')
  clear_output()
  print('Setting environment paths.')
  pbar.update(1)

  
  os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-1.8.0-openjdk-amd64"
  os.environ["SPARK_HOME"] = "/content/spark-2.4.8-bin-hadoop2.7"
  clear_output()
  print('Running findspark')
  pbar.update(1)

  import findspark
  findspark.init()
  clear_output()
  print('Complete!')
  pbar.update(1)