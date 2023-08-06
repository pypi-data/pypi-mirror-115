import setuptools



setuptools.setup(
    name="vinca",
    version="1.1.105",
    author="Oscar Laird", 
    include_package_data = True,
    packages=setuptools.find_packages(),
    install_requires=[ 
        'readchar',
    ],
    scripts = ['scripts/vinca','scripts/vinca_debug']
)
