
from epyk.core.html.options import Options
from epyk.core.html.options import Enums


class EnumStyleOptions(Enums):

  def vertical(self):
    """
    Description:
    ------------
    Set type of curve interpolation.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/tutorial-example02-editor-with-horizontal-preview
    """
    self._set_value()

  def tab(self):
    """
    Description:
    ------------
    Set type of curve interpolation.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/tutorial-example02-editor-with-horizontal-preview
    """
    self._set_value()


class OptionsEditor(Options):
  component_properties = ("initialEditType", )

  @property
  def height(self):
    """
    Description:
    ------------
    """
    return self._config_get("500px")

  @height.setter
  def height(self, val):
    if isinstance(val, int):
      val = "%spx" % val
    self._config(val)

  @property
  def initialValue(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.editor/latest/tutorial-example02-editor-with-horizontal-preview
    """
    return self._config_get("")

  @initialValue.setter
  def initialValue(self, val):
    self._config(val)

  @property
  def language(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.editor/latest/tutorial-example16-i18n
    """
    return self._config_get()

  @language.setter
  def language(self, val):
    self._config(val)

  @property
  def placeholder(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.editor/latest/tutorial-example17-placeholder
    """
    return self._config_get()

  @placeholder.setter
  def placeholder(self, val):
    self._config(val)

  @property
  def theme(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.editor/latest/tutorial-example06-dark-theme
    """
    return self._config_get()

  @theme.setter
  def theme(self, val):
    self._config(val)

  @property
  def viewer(self):
    """
    Description:
    ------------
    """
    return self._config_get(None)

  @viewer.setter
  def viewer(self, flag):
    self._config(flag)

  @property
  def initialEditType(self):
    """
    Description:
    ------------
    """
    return self._config_get("markdown")

  @initialEditType.setter
  def initialEditType(self, val):
    self._config(val)

  @property
  def previewStyle(self):
    """
    Description:
    ------------
    """
    return self._config_get("vertical")

  @previewStyle.setter
  def previewStyle(self, val):
    self._config(val)

  @property
  def previewStyles(self):
    return EnumStyleOptions(self, "previewStyle")
