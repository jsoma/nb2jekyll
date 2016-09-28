# file __init__.py
import os
import os.path
import re

from traitlets.config import Config
from nbconvert.exporters.markdown import MarkdownExporter

def base64image(image):
    possibles = ["image/png", "image/jpeg", "image/svg+xml", "image/gif"]
    for possible in possibles:
        if possible in image['data'].keys():
            mimetype = possible
    return 'data:' + mimetype + ";base64," + image['data'][mimetype]

#-----------------------------------------------------------------------------
# Classes
#-----------------------------------------------------------------------------

class JekyllExporter(MarkdownExporter):
    """
    Converters to Jekyll-friendly markdown
    """

    def _file_extension_default(self):
        """
        The new file extension is `.md`
        """
        return '.md'

    @property
    def default_config(self):
        c = Config({'ExtractOutputPreprocessor':{'enabled':False}})
        # c.merge(super(JekyllExporter,self).default_config)
        return c

    @property
    def template_path(self):
        """
        We want to inherit from HTML template, and have template under
        `./templates/` so append it to the search path. (see next section)
        """
        return super().template_path+[os.path.join(os.path.dirname(__file__), "templates")]

    def _template_file_default(self):
        """
        We want to use the new template we ship with our library.
        """
        return 'jekyll' # full

    def from_notebook_node(self, nb, resources=None, **kw):
        self.register_filter('base64image', base64image)
        full_path = os.path.join(os.getcwd(), resources['metadata']['path'], resources['metadata']['name'] + '.ipynb')
        resources['metadata']['title'] = re.sub(r"\s*\d+[\s\-]+","", resources['metadata']['name'])
        resources['metadata']['full_path'] = full_path
        code_blocks = [cell['source'] for cell in nb['cells'] if cell['cell_type'] == 'code']
        loc = sum([(block.count("\n") + 1) for block in code_blocks])
        resources['metadata']['loc'] = loc
        return super(JekyllExporter, self).from_notebook_node(nb, resources, **kw)
