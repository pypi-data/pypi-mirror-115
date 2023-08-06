from setuptools import setup, find_packages

setup(name="geots2img",
      version="0.1.1",
      description="Geo Time Series to Image",
      url="https://github.com/juliandehoog/geo-timeseries-to-image",
      author="Julian de Hoog",
      author_email='julian@dehoog.ca',
      license="MIT",
      packages=find_packages(),
      install_requires=[
            'pandas',
            'setuptools',
            'numpy',
            'matplotlib',
            'scipy',
            'Pillow',
            'pytz',
      ],
      zip_safe=False)
