from distutils.core import setup

setup(
    name='cvpro',
    packages=['cvpro'],
    version='1.0.9',
    license='MIT',
    description='Computer Vision Helping Library',
    author='Coding Heaven',
    author_email='bmohak87@gmail.com',
    url='https://github.com/Mohak-CODING-HEAVEN/cvpro.git',
    keywords=['ComputerVision', 'HandTracking',
              'FaceTracking', 'PoseEstimation'],
    install_requires=[
        'opencv-python',
        'numpy',
        'mediapipe',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
