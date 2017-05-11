import re
import os
import shutil


class Page:
    def __init__(self):
        self.name = 'noname'
        self.type = 'notype'
        self.content = 'nocontent'

    def __str__(self):
        return '"' + self.name + '" ' + self.type
    __repr__ = __str__

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        return self.name == other.name

    def get_variables(self):
        pattern = '---\n(.+=.*\n)+---\n'  # Front matter
        match = re.match(pattern, self.content)
        if match:
            self.content = self.content[len(match.group(0)):]
            entries = re.split("\n", match.group(0)[4:-4])
            if entries[-1] == '':
                entries.pop()
            for i in range(len(entries)):
                entry = re.split("=", entries[i])
                setattr(self, entry[0], entry[1])


def import_page(page_list, page_type, directory, file_name):
    with open(directory + '/' + file_name, encoding="utf-8") as file:
        a = Page()
        a.type = page_type
        a.content = file.read()
        a.name = file_name.split('.')[0]
        a.get_variables()
        page_list.append(a)


def import_pages(page_list, page_type, directory):
    for file_name in next(os.walk(directory))[2]:
        if file_name.endswith(".html"):
            import_page(page_list, page_type, directory, file_name)


def dissect(content, string, string_index):
    first_part = content[:string_index]
    newline_index = first_part.rindex('\n')
    indent_string = first_part[newline_index + 1:]
    first_part = first_part[:newline_index + 1]
    second_part = content[string_index + len(string):]
    return first_part, second_part, indent_string


def wrap_pages():
    for page in pages:
        split = page.content.split('\n')
        if split[-1] == '':
            split.pop()
        new_split = ''
        for line in split:
            new_split += layout_indent + line + '\n'
        page.content = layout_top + new_split + layout_bottom


def process_table():
    string = '{{table}}\n'

    table = ['<ol>\n']
    for page in pages:
        if page.type == 'normal':
            table.append('  <li><a href="/' + page.name + '">' + page.name + '</a></li>\n')
    table.append('</ol>\n')

    for page in pages:
        string_index = page.content.find(string)
        if string_index > 0:
            top, bottom, indent = dissect(page.content, string, string_index)
            indented_table = []
            for line in table:
                indented_table.append(indent + line)
            indented_table = ''.join(indented_table)
            page.content = top + indented_table + bottom


def process_variables():
    for page in pages:
        if hasattr(page, 'twitter_card') and page.twitter_card != '':
            page.content = page.content.replace('{{card}}', page.twitter_card, 1)
        else:
            page.content = page.content.replace('{{card}}', 'summary_large_image', 1)  # Default value

        if hasattr(page, 'twitter_title') and page.twitter_title != '':
            page.content = page.content.replace('{{title}}', page.twitter_title, 1)
        else:
            page.content = page.content.replace('{{title}}', 'The Delta Project', 1)  # Default value

        if hasattr(page, 'twitter_description') and page.twitter_description != '':
            page.content = page.content.replace('{{description}}', page.twitter_description, 1)
        else:
            page.content = page.content.replace('{{description}}', 'Про науку, трансгуманизм и светлое будущее', 1)  # Default value

        if hasattr(page, 'twitter_image') and page.twitter_image != '':
            page.content = page.content.replace('{{image}}', page.twitter_image, 1)
        else:
            page.content = page.content.replace('{{image}}', 'https://delta.im/img/cover.png', 1)  # Default value


def delete_old():
    if os.path.isdir(website_dir):
        for dir_name in next(os.walk(website_dir))[1]:
            if dir_name != '.git':
                shutil.rmtree(website_dir + '/' + dir_name)
        for file_name in next(os.walk(website_dir))[2]:
            os.remove(website_dir + '/' + file_name)
    else:
        os.makedirs(website_dir)


def export_pages():
    for page in pages:
        if page.type != 'index':
            os.makedirs(website_dir + '/' + page.name)
            with open(website_dir + '/' + page.name + '/index.html', 'w', encoding="utf-8") as file:
                file.write(page.content)
        else:
            with open(website_dir + '/index.html', 'w', encoding="utf-8") as file:
                file.write(page.content)


def copy_files():
    for dir_name in next(os.walk(copy_dir))[1]:
        shutil.copytree(copy_dir + "/" + dir_name, website_dir + "/" + dir_name)

# Main directories
website_dir = os.path.abspath('../delta.im')
script_dir = os.path.abspath('.')
source_dir = os.path.abspath('../site-source-code')
# Other directories
pages_normal_dir = source_dir + "/pages"
pages_test_dir = source_dir + "/pages-test"
copy_dir = source_dir + "/copy"
# Important files
index_file = source_dir + "/index.html"
layout_file = source_dir + "/layout.html"

# Import pages
pages = []
import_page(pages, 'index', source_dir, 'index.html')
import_pages(pages, 'normal', pages_normal_dir)
import_pages(pages, 'test', pages_test_dir)
pages.sort()

# Process pages
with open(layout_file, encoding="utf-8") as layout:
    layout_content = layout.read()
layout_top, layout_bottom, layout_indent = dissect(layout_content, '{{content}}\n',
                                                   layout_content.index('{{content}}\n'))
wrap_pages()
process_table()
process_variables()

# Delete old website
delete_old()

# Generate new website
export_pages()
copy_files()

for i in range(len(pages)):
    if pages[i].name == 'test':
        print(pages[i].__dict__)
        print()
        for key in pages[i].__dict__:
            print(key)
