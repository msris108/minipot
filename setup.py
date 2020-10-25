from setuptools import setup


def readme_file_contents():
    with open('README.rst') as readme_file:
        data = readme_file.read()
    return data


setup(
    name='minipot',
    version='1.0.0.0',
    description='A simple honey pot for reverse tcp shell attacks, netcat reverse shell attacks ...',
    long_description=readme_file_contents(),
    author='msris108',
    author_email='msris108@gmail.com',
    license='MIT',
    packages=['minipot'],
    zip_safe=False,
    install_requires=[]
)
