from setuptools import setup, find_packages

setup(
    name='LibertyDreamer',
    version='1.0.0',
    license='MIT License',
    author='Benfica',
    keywords=['chatbot', 'liberty', 'freedom', 'bot', 'chat'],
    description='Free yourself with tools that increase the ease and possibilities of your project.',
    packages=find_packages(),
    install_requires=['fuzzywuzzy', 'python-Levenshtein'],
)