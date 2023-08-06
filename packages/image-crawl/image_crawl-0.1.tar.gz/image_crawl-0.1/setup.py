from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(name='image_crawl',
      version='0.1',
      description='Crawl and transform images',
      url='https://github.com/les-41-plats/image_crawl',
      author='Les 41 Plats',
      author_email='les41plats.work@gmail.com',
      license='MIT',
      packages = find_packages(),
      entry_points ={
            'console_scripts': [
                'bcrawl = image_crawl.src.collect:main'
            ]
        },
      install_requires = requirements,
      zip_safe=False)