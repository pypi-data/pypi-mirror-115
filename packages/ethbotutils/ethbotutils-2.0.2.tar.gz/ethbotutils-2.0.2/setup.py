from setuptools import setup

setup(
    name='ethbotutils',
    version="2.0.2",
    author="Alberto Pirillo",
    packages=["ethbotutils"],
    install_requires=["requests~=2.25.1", "PyYAML~=5.4.1"],
    python_requires=">=3.6"
)
