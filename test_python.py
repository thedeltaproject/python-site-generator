import os

for (dirpath, dirnames, filenames) in os.walk('../thedeltaproject.github.io'):
    print(dirpath, dirnames, filenames, sep='\n', end='\n\n')
