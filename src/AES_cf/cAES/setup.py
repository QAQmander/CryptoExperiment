from distutils.core import setup, Extension
MOD = 'cAES'
setup(name=MOD, ext_modules=[Extension(MOD, sources=['cAES.c', 'aes.c', 'gf242.c'])])
