# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Tech Writer Portfolio'
copyright = '2025, Llama techwriter'
author = 'Llama techwriter'


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinxcontrib.plantuml',
    'sphinx_tabs.tabs', # Это расширение позволяет создавать вкладки для демонстрации различных примеров кода или информации.
    'sphinx_design', # Это расширение позволяет создавать карточки, баннеры и другие визуальные элементы.
   #'sphinxcontrib.youtube', # внедряет видео с YouTube.
    'sphinx.ext.githubpages', # Это расширение помогает добавлять ссылки на issues и pull requests в вашей документации.
    'jupyter_sphinx', # интерактивные блоки кода, которые пользователи могут выполнять прямо в браузере
    'sphinx_tags', # Это расширение позволяет добавлять теги и категории к страницам документации, что упрощает навигацию.
    'sphinxcontrib.mermaid', # Mermaid — это инструмент для создания диаграмм внутри Markdown/Sphinx.
    'sphinx.ext.mathjax',  # Для поддержки математических формул
        # Sphinx's own extensions
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    # External stuff
    "sphinx_copybutton",
    'sphinx-jsonschema',  # Расширение для JSON Schema
    "sphinxcontrib.openapi",  # Расширение для OpenAPI
    'myst_parser',  # Поддержка Markdown

]


# Укажите путь к plantuml.jar и команду для его запуска
# plantuml = 'java -Djava.awt.headless=true -jar plantuml/plantuml.jar'


# Укажите URL публичного сервера PlantUML
plantuml = 'https://www.plantuml.com/plantuml/svg/'

# Настройка тегов
tags_create_tags = True
tags_page_title = "Теги"
tags_overview_template = "tags_overview.html"

templates_path = ['_templates']
exclude_patterns = []

language = 'ru'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_title = "Tech Writer Portfolio"
html_static_path = ['_static']
html_logo = "_static/logo.jpg"

def setup(app):
    app.add_css_file('custom.css')
    app.add_js_file('print_button.js')
    app.add_js_file('export_pdf.js')
