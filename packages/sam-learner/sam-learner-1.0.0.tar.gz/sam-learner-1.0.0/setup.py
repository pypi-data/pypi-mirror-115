from distutils.core import setup

setup(name='sam-learner',
      version='1.0.0',
      python_requires=">=3.8",
      description='Safe Action Model Learner',
      author='Argaman Mordoch',
      packages=['core', 'SAM_models'],
     )