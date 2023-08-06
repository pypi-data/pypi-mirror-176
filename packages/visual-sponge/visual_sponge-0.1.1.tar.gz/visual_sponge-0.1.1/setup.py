from setuptools import setup, find_packages
from setuptools.command.egg_info import egg_info

class MyEggInfo(egg_info):
    def run(self):
        super().run()
        self.filelist.include("visual_sponge/static/*")
        self.filelist.include("visual_sponge/templates/*")

setup(name="visual_sponge",
      version="0.1.1",
      description="A python package to do the visualization for molecular simulations",
      author="Yijie Xia",
      author_email="yijiexia@pku.edu.cn",
      packages=find_packages(),
      install_requires = ["flask", "Xponge"],
      cmdclass={"egg_info": MyEggInfo},
      long_description=open('README.md').read(),
      entry_points = {
        "console_scripts": ["vsponge = visual_sponge.__main__:main"]},
      classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        'Development Status :: 5 - Production/Stable',
        "Operating System :: OS Independent",
        ],
      )