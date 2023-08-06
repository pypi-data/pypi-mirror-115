import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='vissccnet',  
     version='0.1', 
     scripts=['vissccnet'] , #List of executable files. 
     author="Ya-Lin Huang", 
     author_email="bai06hua28lin.bt06@nctu.edu.tw",
     description="A CNN model training and weight visualization toolbox",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/skywalkerylh/visSCCNet",
     install_requires=['mne', 'numpy', 'scipy', 'matplotlib', 'tkinter'],
     packages=setuptools.find_packages(), #Use for other package dependencies.
     classifiers=[
        #'Development Status :: 3 - Alpha',  #not sure 

        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        'Topic :: Software Development :: Build Tools',

        "Topic :: Scientific/Engineering :: Artificial Intelligence",

        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
    ],
    keywords='eeg deep-learning brain-state-decoding',
    include_package_data=False, # 沒有其他打包文件
    zip_safe=False, #whether the package is installed in compressed mode or regular mode.
)