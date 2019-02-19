from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

from pathlib import Path

rootpath = Path('.')
libs = []
libs.append(rootpath / 'portal_src')

ext_modules = []
for lib in libs:
	for file in lib.glob('**/*.py'):
		file_name=file.__str__()
		name = file.parts[-1].split('.')[0]
		ext_name="lib.portal_src." + ".".join(file.parts[1:-1]) + "." + name
		ext_modules.append(Extension(ext_name, [file_name], extra_compile_args=['-DMS_WIN64'],library_dirs=['.\\..\\..\\Python37']))

setup(
  name = 'Bug0rs Portal Tool',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)
