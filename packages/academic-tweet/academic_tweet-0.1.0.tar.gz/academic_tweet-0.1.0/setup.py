from setuptools import setup

setup(
    name='academic_tweet',
    version='0.1.0',    
    description='An API wrapper for academic track access to the v2 Twitter API',
    url='https://github.com/A-Lohse/academic_tweet',
    download_url = "https://github.com/A-Lohse/academic_tweet/archive/refs/tags/v0.2.tar.gz",
    author='August Lohse',
    author_email='al@augustlohse.com',
    license='MIT',
    license_files = "license.txt",
    packages=['academic_tweet'],
    install_requires= ['requests', 'time'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',    
        'Programming Language :: Python :: 3.7',],
)