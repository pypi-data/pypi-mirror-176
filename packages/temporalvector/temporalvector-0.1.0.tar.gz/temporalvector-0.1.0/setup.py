from setuptools import setup

setup(
        name='temporalvector',
        version='1.0.0',
        packages=['temporalvector'],
        url='https://git.jetbrains.space/cmckay/advanced-simulation/pkg_temporal_vector.git',
        license='MIT',
        install_requires=['numpy>=1.23.4'],
        author='Chris McKay',
        author_email='crmckay55@gmail.com',
        description='Temporally aware vector of values that can be aggregated using different methods over different'
                    'time periods'
)
