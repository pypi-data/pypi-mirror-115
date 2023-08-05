
from epyk.core.html.options import Options


class OptionDateRange(Options):

  @property
  def date(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.date-picker/latest/Calendar
    """
    return self._config_get("")

  @date.setter
  def date(self, val):
    self._config(val)

  @property
  def type(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.date-picker/latest/Calendar
    """
    return self._config_get("")

  @type.setter
  def type(self, val):
    self._config(val)

  @property
  def language(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.date-picker/latest/Calendar
    """
    return self._config_get("")

  @language.setter
  def language(self, val):
    self._config(val)

  @property
  def showToday(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.date-picker/latest/Calendar
    """
    return self._config_get(True)

  @showToday.setter
  def showToday(self, flag):
    self._config(flag)

  @property
  def showJumpButtons(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.date-picker/latest/Calendar
    """
    return self._config_get(True)

  @showJumpButtons.setter
  def showJumpButtons(self, flag):
    self._config(flag)

  @property
  def usageStatistics(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.date-picker/latest/Calendar
    """
    return self._config_get(True)

  @usageStatistics.setter
  def usageStatistics(self, flag):
    self._config(flag)

  @property
  def weekStartDay(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.date-picker/latest/Calendar
    """
    return self._config_get('Sun')

  @weekStartDay.setter
  def weekStartDay(self, value):
    self._config(value)


class OptionDate(Options):

  @property
  def defaultView(self):
    """
    Description:
    ------------
    """
    return self._config_get("")

  @defaultView.setter
  def defaultView(self, val):
    self._config(val)


class OptionCalendar(Options):

  @property
  def defaultView(self):
    """
    Description:
    ------------
    """
    return self._config_get("")

  @defaultView.setter
  def defaultView(self, val):
    self._config(val)

  @property
  def taskView(self):
    """
    Description:
    ------------
    """
    return self._config_get("")

  @taskView.setter
  def taskView(self, val):
    self._config(val)
