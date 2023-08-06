from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='Keep4183',
    description='demo example',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=['Development Status :: 1 - Planning', 'Programming Language :: Python :: 3.10'],
    url='https://github.com/moralesveratom/locatePath',
    author='tmorales',
    author_email='moralesveratomas@gmail.com',
    keywords=['python', 'path', 'locate', 'locator', 'pathLocator', 'pathLocate', 'locatorPath'],
    license='MIT',
    install_requires=[],
    include_package_data=True,
    zip_safe=False
)
