from setuptools import setup, find_packages

setup(
    name = "coreutils-python",
    version = "0.0.1",
    packages = find_packages(),
    entry_points = {
        "console_scripts": ["ls = coreutils.ls:main",
                            "rm = coreutils.rm:main",
                            "cp = coreutils.cp:main",
                            "mv = coreutils.mv:main",
                            "cat = coreutils.cat:main",
                            "echo = coreutils.echo:main",
                            "mkdir = coreutils.mkdir:main",
                            "rmdir = coreutils.rmdir:main"]
    }
)
