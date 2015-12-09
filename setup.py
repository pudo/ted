from setuptools import setup, find_packages

setup(
    name='ted',
    version='0.1',
    description="A scraper for EU Tenders Electronic Daily.",
    long_description='',
    classifiers=[],
    keywords='',
    author='',
    author_email='friedrich@pudo.org',
    url='http://ted.openspending.org',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=[],
    include_package_data=False,
    zip_safe=False,
    install_requires=[
    ],
    tests_require=[],
    entry_points=""" """,
)
