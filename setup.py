from setuptools import setup
import pathlib

cmdclass = {}

try:
    from sphinx.setup_command import BuildDoc
    cmdclass['build_sphinx'] = BuildDoc
except ImportError:
    print('WARNING: sphinx not available, not building docs')

here = pathlib.Path(__file__).parent.resolve()

name = 'nsrt_mk3_dev'

# Get the long description from the README file
long_description = (here / 'README.rst').read_text(encoding='utf-8')

setup(

    name=name,
    description='NX Solutions Work Log',
    long_description=long_description,
    long_description_content_type='text/x-rst',

    url='https://xanderhendriks.github.io/nsrt-mk3-dev',

    author='Xander Hendriks',
    author_email='xander.hendriks@nx-solutions.com',

    classifiers=[  # Optional
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
    ],

    packages=['nsrt_mk3_dev'],

    python_requires='>=3.6',
    install_requires=['pyserial'],
    setup_requires=[
        'setuptools_scm',
        'wheel',
    ],

    extras_require={
        'dev': ['check-manifest', 'flake8'],
        'test': ['pytest'],
        'doc': ['sphinx', 'sphinx-rtd-theme'],
    },

    project_urls={
        'Bug Reports': 'https://github.com/xanderhendriks/nsrt-mk3-dev/issues',
        'Source': 'https://github.com/xanderhendriks/nsrt-mk3-dev',
    },

    use_scm_version={
        'relative_to': __file__,
        'write_to': 'nsrt_mk3_dev/version.py',
        'local_scheme': 'no-local-version',
    },

    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'source_dir': ('setup.py', 'doc'),
        }
    },
)
