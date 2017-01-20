import os
import shutil
from distutils.dir_util import copy_tree

pageList = []  # Empty list of pages
pageListWoExt = []  # Empty list of pages without extensions

for (dirpath, dirnames, filenames) in os.walk('pages'):  # Fill postList with pages' filenames
    pageList.extend(filenames)
    break

for pageName in pageList:
    pageListWoExt.append(pageName.split('.')[0])  # Fill pageListWoExt with pages' filenames w/o extensions

with open('layout.html', encoding="utf-8") as layout:  # Read layout HTML, split on content and write to layoutParts
    layoutParts = layout.read().split('{{ content }}\n')

"""
if os.path.isdir('../thedeltaproject.github.io'):  # TODO: make list noDelete
    shutil.rmtree('../thedeltaproject.github.io')  # Delete entire site folder
"""

filesToDelete =[]
dirsToDelete = []

if os.path.isdir('../thedeltaproject.github.io'):
    for (dirpath, dirnames, filenames) in os.walk('../thedeltaproject.github.io'):
        filesToDelete.extend(filenames)
        dirsToDelete.extend(dirnames)
        break
    if '.git' in dirsToDelete:
        dirsToDelete.remove('.git')
    for file in filesToDelete:
        os.remove('../thedeltaproject.github.io/' + file)
    for directory in dirsToDelete:
        shutil.rmtree('../thedeltaproject.github.io/' + directory)
else:
    os.makedirs('../thedeltaproject.github.io')  # Create new site folder

with open('index.html', encoding="utf-8") as index:  # Write index.html with layout to the site folder
    output = layoutParts[0] + index.read() + layoutParts[1]
    with open('../thedeltaproject.github.io/index.html', 'w', encoding="utf-8") as outputFile:
        outputFile.write(output)

for i in range(len(pageList)):  # Write pages with layout to the site folder
    with open('pages/' + pageList[i], encoding="utf-8") as page:
        output = layoutParts[0]+page.read()+layoutParts[1]
    os.makedirs('../thedeltaproject.github.io/' + pageListWoExt[i])
    with open('../thedeltaproject.github.io/' + pageListWoExt[i] + '/index.html', 'w', encoding="utf-8") as outputFile:
        outputFile.write(output)

copy_tree('copy', '../thedeltaproject.github.io')  # Copy non-html files to the site folder
