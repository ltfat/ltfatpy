from distutils.core import setup
import subprocess
import shutil

setup(
   name='ltfatpy',
   version='0.1',
   packages=['',],
   license='GPL3',
   long_description=open('README').read(),
)

def compile_oct_files():
    #subprocess.Popen(["./configure"], stdout=subprocess.PIPE, cwd="./setup")
    subprocess.Popen(["make"], stdout=subprocess.PIPE, cwd="./setup")
   # src_path = r"./libltfat/build/libltfat.a"
   # dst_path = r"./octave/ltfat/oct/libltfat.a"
   # shutil.copy(src_path, dst_path)
   # print('Copied libltfat.a ')

def main():
    compile_oct_files()

if __name__ == "__main__":
    main()
