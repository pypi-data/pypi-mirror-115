import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='mrdrone',
    version='0.0.1',
    author='C灵C',
    author_email='c0c@cocpy.com',
    description='Control Tello or Folk drone with Python3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cocpy/Tello-Python',
    packages=setuptools.find_packages(),
    install_requires=[
        'opencv-python', 'flask', 'pyfolk', 'greenlet==0.4.16', 'pillow'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)