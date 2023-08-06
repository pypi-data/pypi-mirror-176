import PyWireframe,os
from setuptools import setup

try:os.chdir(os.path.split(__file__)[0])
except:pass

desc="""An extended version of 3D rendering package PyWireframe, with some bugs fixed.\
PyWireframe是一个使用Python turtle绘制3D图形的库, 使用简单的代码实现复杂的3D场景。\
这是PyWireframe包的扩展版本, 修复了PyWireframe的大部分bug。"""

try:
    long_desc=open("README.rst").read()
except OSError:
    long_desc=desc

setup(
  name='PyWireframe-extended',
  version=PyWireframe.__version__,
  description=desc,
  long_description=long_desc,
  author="Uploader: qfcy",
  url="https://github.com/qfcy/PyWireframe",
  packages=['PyWireframe'],
  keywords=["pywireframe","turtle","3d","graphics","绘图","render"],
  classifiers=[
      "Programming Language :: Python :: 3",
      "Operating System :: OS Independent",
      "Topic :: Multimedia :: Graphics :: 3D Rendering",
      "Topic :: Education",
      "Natural Language :: Chinese (Simplified)"],
)
