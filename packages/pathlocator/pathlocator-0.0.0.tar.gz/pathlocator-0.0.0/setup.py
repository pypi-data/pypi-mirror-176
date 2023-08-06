from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='pathlocator',
    description='demo example',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[''],
    url='',
    author='tmorales',
    author_email='moralesveratomas@gmail.com',
    keywords=['python', 'path', 'locate', 'locator', 'pathLocator', 'pathLocate', 'locatorPath'],
    license='MIT',
    packages=[''],
    include_package_data=True,
    zip_safe=False
)
