from setuptools import setup, find_namespace_packages

setup(
    name='Movepy',
    version='0.0.0',
    description='Python Model based on VU 3d model in Matlab',
    author='Yiyuan Li',
    email='liyiyuan0413@163.com',
    license='MIT',
    license_files=["LICENSE.txt"],
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_requires=['pytest==6.2.4'],
    test_suites='tests',
    python_requires=">=3.6",
    packages=find_namespace_packages(exclude=("tests*")),
)
