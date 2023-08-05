from setuptools.extension import Extension
from wheel.bdist_wheel import bdist_wheel


custom_extension = Extension(
    'tsp_algorithms.ctsp',
    sources=[
        'tsp_algorithms/lib/tsp.c',
        'tsp_algorithms/lib/algorithms.c',
        'tsp_algorithms/lib/metrics.c',
    ],
    define_macros=[('Py_LIMITED_API', '0x03060000'), ('PY_SSIZE_T_CLEAN',)],
    py_limited_api=True,
)


class bdist_wheel_abi3(bdist_wheel):
    def get_tag(self):
        python, abi, plat = super().get_tag()

        if python.startswith('cp'):
            # on CPython, our wheels are abi3 and compatible back to 3.8
            return 'cp38', 'abi3', plat

        return python, abi, plat


def build(setup_kwargs):
    """
    This is a callback for poetry used to hook in our extensions.
    """
    setup_kwargs.update(
        {
                # declare the extension so that setuptools will compile it
                'ext_modules': [custom_extension],
                'cmdclass': {'bdist_wheel': bdist_wheel_abi3},
        }
    )