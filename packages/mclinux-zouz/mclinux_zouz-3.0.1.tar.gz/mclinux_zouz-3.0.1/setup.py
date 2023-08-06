from setuptools import setup, Distribution


class BinaryDistribution(Distribution):
    def has_ext_modules(foo):
        return True


setup(
    name='mclinux_zouz',
    version='3.0.1',
    description='Algotirhm to find maximalclique',
    packages=['MCMC'],
    package_data={
        'MCMC': ['*.pyd', '*.so'],
    },
    distclass=BinaryDistribution)
