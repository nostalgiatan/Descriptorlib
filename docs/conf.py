import os
import sys
sys.path.insert(0, os.path.abspath('..'))


# -- 项目信息 -----------------------------------------------------

project = 'Descriptorlib'
copyright = '2023, 解文'
author = 'snow'
release = '0.1.0'

# -- 常规配置 ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.ifconfig',
]


# 添加任何包含模板的路径，相对于这个目录。
templates_path = ['_templates']

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints']

# -- HTML 输出选项 -------------------------------------------------

# HTML 和 HTML 帮助页面使用的主题。
html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'canonical_url': '',
    'analytics_id': '',
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    # Toc 选项
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# 添加任何包含自定义静态文件（如样式表）的路径，相对于这个目录。
# 它们将在内置静态文件之后被复制，因此名为 "default.css" 的文件将覆盖内置的 "default.css"。
html_static_path = ['_static']

# 自定义侧边栏模板，必须是一个将文档名称映射到模板名称的字典。
html_sidebars = {
    '**': [
        'relations.html',
        'searchbox.html',
    ]
}

# -- LaTeX 输出选项 ------------------------------------------------

latex_elements = {
    # 纸张大小 ('letterpaper' 或 'a4paper')。
    'papersize': 'a4paper',

    # 字体大小 ('10pt', '11pt' 或 '12pt')。
    'pointsize': '10pt',
}

# 将文档树分组到 LaTeX 文件中。元组列表
# (源起始文件, 目标名称, 标题, 作者, 文档类 [howto/manual])。
latex_documents = [
    (master_doc, 'Descriptorlib.tex', 'Descriptorlib Documentation',
     'snow', 'manual'),
]

# -- 手册页输出选项 ------------------------------------------

# 每个手册页一个条目。元组列表
# (源起始文件, 名称, 描述, 作者, 手册节)。
man_pages = [
    (master_doc, 'Descriptorlib', 'Descriptorlib Documentation',
     [author], 1)
]

# -- Texinfo 输出选项 ----------------------------------------------
master_doc = 'index'
# 将文档树分组到 Texinfo 文件中。元组列表
# (源起始文件, 目标名称, 标题, 作者,
#  目录菜单条目, 描述, 类别)
texinfo_documents = [
    (master_doc, 'Descriptorlib', 'Descriptorlib Documentation',
     author, 'Descriptorlib', 'Descriptorlib is a Python library that provides a series of powerful descriptors for enhancing the attribute functionality of Python classes.',
     'Miscellaneous'),
]

# -- Epub 输出选项 -------------------------------------------------

# Dublin Core 书目信息。
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

# 文本的唯一标识符。这可以是 ISBN 号码
# 或项目的主页。
epub_identifier = 'https://github.com/nostalgiatan/Descriptorlib'

# 文本的唯一识别码。
epub_uid = 'Descriptorlib'

# 不应打包进 epub 文件的文件列表。
epub_exclude_files = ['search.html']

# -- 扩展配置 -------------------------------------------------

# -- intersphinx 扩展选项 ---------------------------------------

# intersphinx 的配置，引用 Python 标准库。
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}

# -- todo 扩展选项 ----------------------------------------------

todo_include_todos = True

# -- autodoc 扩展选项 ------------------------------------------

autoclass_content = 'both'

# -- napoleon 扩展选项 ------------------------------------------
napoleon_include_private_with_doc = False

# -- ifconfig 扩展选项 ------------------------------------------

# 默认设置是不渲染指令的内容。
ifconfig_debug = False

# -- HTML 输出选项 -------------------------------------------------

# HTML 帮助构建器的输出文件基本名称。
htmlhelp_basename = 'Descriptorlib'

