import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name='sharingiscaring',
    version='0.0.5',
    author='Sander de Ruiter',
    author_email='sdr@concordium-explorer.nl',
    description='Initial version',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/sderuiter/sharingiscaring',
    project_urls={
    },
    license='MIT',
    packages=['sharingiscaring'],
    install_requires=['rich', 'python-dateutil', 'base58', 'pysha3', 'pytest'],
)