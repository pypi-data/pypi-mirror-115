
from epyk.core.html import Html
from epyk.fwk.toast.options import OptToastEditor
from epyk.fwk.toast.js import JsToastEditor


class Editor(Html.Html):
  name = 'ToastEditor'
  requirements = ('@toast-ui/editor', )
  _option_cls = OptToastEditor.OptionsEditor

  def __init__(self, report, width, height, html_code, options, profile):
    self.height = height[0]
    super(Editor, self).__init__(
      report, [], html_code=html_code, profile=profile, options=options, css_attrs={"width": width, "height": height})
    self.options.height = height[0]

  @property
  def options(self):
    """
    Description:
    -----------

    :rtype: OptToastEditor.OptionsEditor
    """
    return super().options

  @property
  def js(self):
    """
    Description:
    -----------
    Javascript module of the items in the menu.

    :return: A Javascript Dom object.

    :rtype: JsToastEditor.Editor
    """
    if self._js is None:
      self._js = JsToastEditor.Editor(self, varName=self._selector, report=self.page)
    return self._js

  _js__builder__ = '''
  options.el = htmlObj; const editor = new toastui.Editor(options)'''

  def __str__(self):
    self.page.properties.js.add_builders(self.build())
    return '<div %s></div>' % self.get_attrs(pyClassNames=self.style.get_classes())
