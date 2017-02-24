import os
import shutil
from distutils.dir_util import copy_tree

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pageList = []  # Empty list of pages
pageListWoExt = []  # Empty list of pages without extensions

for (dirpath, dirnames, filenames) in os.walk('../site-source-code/pages'):  # Fill postList with pages' filenames
    pageList.extend(filenames)
    break

for pageName in pageList:
    pageListWoExt.append(pageName.split('.')[0])  # Fill pageListWoExt with pages' filenames w/o extensions

with open('../site-source-code/layout.html', encoding="utf-8") as layout:  # Read layout HTML, split on content and write to layoutParts
    layoutParts = layout.read().split('{{ content }}\n')

"""
if os.path.isdir('../delta.im'):  # TODO: make list noDelete
    shutil.rmtree('../delta.im')  # Delete entire site folder
"""

filesToDelete =[]
dirsToDelete = []

if os.path.isdir('../delta.im'):
    for (dirpath, dirnames, filenames) in os.walk('../delta.im'):
        filesToDelete.extend(filenames)
        dirsToDelete.extend(dirnames)
        break
    if '.git' in dirsToDelete:
        dirsToDelete.remove('.git')
    for file in filesToDelete:
        os.remove('../delta.im/' + file)
    for directory in dirsToDelete:
        shutil.rmtree('../delta.im/' + directory)
else:
    os.makedirs('../delta.im')  # Create new site folder

with open('../site-source-code/index.html', encoding="utf-8") as index:  # Write index.html with layout to the site folder
    output = layoutParts[0] + index.read() + layoutParts[1]
    with open('../delta.im/index.html', 'w', encoding="utf-8") as outputFile:
        outputFile.write(output)

for i in range(len(pageList)):  # Write pages with layout to the site folder
    with open('../site-source-code/pages/' + pageList[i], encoding="utf-8") as page:
        output = layoutParts[0]+page.read()+layoutParts[1]
    os.makedirs('../delta.im/' + pageListWoExt[i])
    with open('../delta.im/' + pageListWoExt[i] + '/index.html', 'w', encoding="utf-8") as outputFile:
        outputFile.write(output)

copy_tree('../site-source-code/copy', '../delta.im')  # Copy non-html files to the site folder

print('Success!')
