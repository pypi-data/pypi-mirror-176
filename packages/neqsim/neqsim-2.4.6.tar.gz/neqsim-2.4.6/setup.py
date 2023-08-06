import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="neqsim",
    version="2.4.6",
    author="Even Solbraa",
    author_email="esolbraa@gmail.com",
    description="NeqSim is a tool for thermodynamic and process calculations",
    long_description="NeqSim (Non-Equilibrium Simulator) is a library for estimation of fluid behaviour for oil and gas production. The basis for NeqSim is fundamental mathematical models related to phase behaviour and physical properties of oil and gas.",
    long_description_content_type="text/markdown",
    url="https://github.com/Equinor/neqsimpython",
    packages=setuptools.find_packages(),
    package_data={'neqsim': ['lib/*.jar','lib/libj8/*.jar']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=['jpype1', 'pandas', 'tabulate'],
    python_requires='>=3'
)
