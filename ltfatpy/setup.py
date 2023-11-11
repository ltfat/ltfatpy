from distutils.core import setup
from subprocess import Popen, PIPE
import shutil

setup(
   name='ltfatpy',
   version='0.1',
   packages=['',],
   license='GPL3',
   long_description=open('README').read(),
)

def compile_oct_files():
    process = Popen(["./configure"], stdout=PIPE, cwd="./setup")
   # src_path = r"./libltfat/build/libltfat.a"
   # dst_path = r"./octave/ltfat/oct/libltfat.a"
   # shutil.copy(src_path, dst_path)
   # print('Copied libltfat.a ')
    stdout, stderr = process.communicate()
    print(stdout)
    process = Popen(["make"], stdout=PIPE, cwd="./setup")
    stdout, stderr = process.communicate()
    print(stdout)

def main():
    compile_oct_files()

if __name__ == "__main__":
    main()
