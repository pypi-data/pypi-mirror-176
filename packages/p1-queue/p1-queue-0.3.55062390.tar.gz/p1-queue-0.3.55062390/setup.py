from setuptools import setup, find_packages

setup(name='p1-queue',
      version='0.3.55062390',
      description='Messaging abstraction for AMQP',
      author='Turfa Auliarachman',
      author_email='turfa_auliarachman@rocketmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'google-cloud-pubsub==1.7.2'
      ],
      zip_safe=False,
      include_package_data=True,
      classifiers=[
          'Intended Audience :: Developers',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3'
      ])
