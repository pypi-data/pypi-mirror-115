from setuptools import setup, find_packages

setup(
    name = 'DistTestKeithCBetterVersion',
    version = '1.2',
    author = 'Keith Cressman',
    author_email = "keith.cressman@duke.edu",
    packages = find_packages(),
    url= "https://github.com/KeithCressman/test",
    entry_points = {"console_scripts":["runKeithsDemo=MainFolder.doStuff:main"]}
)