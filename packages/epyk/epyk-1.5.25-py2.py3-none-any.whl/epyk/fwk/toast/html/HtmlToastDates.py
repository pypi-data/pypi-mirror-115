from epyk.core.html import Html
from epyk.fwk.toast.options import OptToastCalendar
from epyk.fwk.toast.js import JsToastDates


class DatePicker(Html.Html):
  name = 'ToastCharts'
  requirements = ('@toast-ui/chart', )
  _option_cls = OptToastCalendar.OptionDate

  @property
  def options(self):
    """
    Description:
    -----------

    :rtype: OptToastCalendar.OptionDate
    """
    return super().options

  @property
  def js(self):
    """
    Description:
    -----------
    Javascript module of the items in the menu.

    :return: A Javascript Dom object

    :rtype: JsToastDates.DatePicker
    """
    if self._js is None:
      self._js = JsToastDates.DatePicker(self, varName=self._selector, report=self.page)
    return self._js


class DateCalendar(Html.Html):
  name = 'ToastCharts'
  requirements = ('@toast-ui/chart', )
  _option_cls = OptToastCalendar.OptionCalendar

  @property
  def options(self):
    """
    Description:
    -----------

    :rtype: OptToastCalendar.OptionCalendar
    """
    return super().options

  @property
  def js(self):
    """
    Description:
    -----------
    Javascript module of the items in the menu.

    :return: A Javascript Dom object

    :rtype: JsToastDates.Calendar
    """
    if self._js is None:
      self._js = JsToastDates.Calendar(self, varName=self._selector, report=self.page)
    return self._js


class DatePickerRange(Html.Html):
  name = 'ToastCharts'
  requirements = ('@toast-ui/chart', )
  _option_cls = OptToastCalendar.OptionDateRange

  @property
  def options(self):
    """
    Description:
    -----------

    :rtype: OptToastCalendar.OptionDateRange
    """
    return super().options

  @property
  def js(self):
    """
    Description:
    -----------
    Javascript module of the items in the menu.

    :return: A Javascript Dom object

    :rtype: JsToastDates.DatePickerRange
    """
    if self._js is None:
      self._js = JsToastDates.DatePickerRange(self, varName=self._selector, report=self.page)
    return self._js
