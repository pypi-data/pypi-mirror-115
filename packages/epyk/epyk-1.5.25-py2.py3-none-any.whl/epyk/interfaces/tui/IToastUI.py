
from epyk.fwk.toast import html
from epyk.interfaces import Arguments


class ToastCharts:

  def __init__(self, ui):
    self.page = ui.page

  def plot(self, record=None, y=None, x=None, kind="line", profile=None, width=(100, "%"), height=(330, "px"),
           options=None, html_code=None):
    """
    Description:
    ------------

    :tags:
    :categories:

    Usage::

    Related Pages:

    Attributes:
    ----------
    :param record: List. Optional. The list of dictionaries with the input data.
    :param y: List | String. Optional. The columns corresponding to keys in the dictionaries in the record.
    :param x: String. Optional. The column corresponding to a key in the dictionaries in the record.
    :param kind: String. Optional. The chart type.
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage.
    :param width: Tuple. Optional. The width of the component in the page, default (100, '%').
    :param height: Tuple. Optional. The height of the component in the page, default (330, "px").
    :param options: Dictionary. Optional. Specific Python options available for this component.
    :param html_code: String. Optional. An identifier for this component (on both Python and Javascript side).
    """
    if y is not None and not isinstance(y, list):
      y = [y]
    return getattr(self, kind)(record=record, y_columns=y, x_axis=x, profile=profile, width=width, height=height,
                               options=options, html_code=html_code)

  def line(self, record=None, y_columns=None, x_axis=None, profile=None, width=(100, "%"), height=(330, "px"),
           options=None, html_code=None):
    """

    https://nhn.github.io/tui.chart/latest/LineChart

    :param record:
    :param y_columns:
    :param x_axis:
    :param profile:
    :param width:
    :param height:
    :param options:
    :param html_code:
    """
    width = Arguments.size(width, unit="%")
    height = Arguments.size(height, unit="px")
    dfl_options = {"series": []}
    dfl_options.update({'y_columns': y_columns or [], 'x_axis': x_axis, 'commons': {'fill': None}})
    if options is not None:
      dfl_options.update(options)
    data = self.page.data.chartJs.y(record or [], y_columns, x_axis)
    chart = html.HtmlToastCharts.Chart(self.page, width, height, html_code, dfl_options, profile)
    return chart

  def spline(self, record=None, y_columns=None, x_axis=None, profile=None, width=(100, "%"), height=(330, "px"),
           options=None, html_code=None):
    pass

  def area(self, record=None, y_columns=None, x_axis=None, profile=None, width=(100, "%"), height=(330, "px"),
           options=None, html_code=None):
    width = Arguments.size(width, unit="%")
    height = Arguments.size(height, unit="px")
    dfl_options = {"series": []}
    dfl_options.update({'y_columns': y_columns or [], 'x_axis': x_axis, 'commons': {'fill': None}})
    if options is not None:
      dfl_options.update(options)
    data = self.page.data.chartJs.y(record or [], y_columns, x_axis)
    chart = html.HtmlToastCharts.ChartArea(self.page, width, height, html_code, dfl_options, profile)
    return chart

  def bullet(self, record=None, y_columns=None, x_axis=None, profile=None, width=(100, "%"), height=(330, "px"),
           options=None, html_code=None):
    pass

  def bubble(self, record=None, y_columns=None, x_axis=None, profile=None, width=(100, "%"), height=(330, "px"),
             options=None, html_code=None):
    width = Arguments.size(width, unit="%")
    height = Arguments.size(height, unit="px")
    dfl_options = {"series": []}
    dfl_options.update({'y_columns': y_columns or [], 'x_axis': x_axis, 'commons': {'fill': None}})
    if options is not None:
      dfl_options.update(options)
    data = self.page.data.chartJs.y(record or [], y_columns, x_axis)
    chart = html.HtmlToastCharts.ChartBubble(self.page, width, height, html_code, dfl_options, profile)
    return chart

  def box(self, record=None, y_columns=None, x_axis=None, profile=None, width=(100, "%"), height=(330, "px"),
           options=None, html_code=None):
    pass

  def bar(self, record=None, y_columns=None, x_axis=None, profile=None, width=(100, "%"), height=(330, "px"),
           options=None, html_code=None):
    pass
    width = Arguments.size(width, unit="%")
    height = Arguments.size(height, unit="px")
    dfl_options = {"series": []}
    dfl_options.update({'y_columns': y_columns or [], 'x_axis': x_axis, 'commons': {'fill': None}})
    if options is not None:
      dfl_options.update(options)
    data = self.page.data.chartJs.y(record or [], y_columns, x_axis)
    chart = html.HtmlToastCharts.ChartColumn(self.page, width, height, html_code, dfl_options, profile)
    return chart

  def hbar(self, record=None, y_columns=None, x_axis=None, profile=None, width=(100, "%"), height=(330, "px"),
           options=None, html_code=None):
    width = Arguments.size(width, unit="%")
    height = Arguments.size(height, unit="px")
    dfl_options = {"series": []}
    dfl_options.update({'y_columns': y_columns or [], 'x_axis': x_axis, 'commons': {'fill': None}})
    if options is not None:
      dfl_options.update(options)
    data = self.page.data.chartJs.y(record or [], y_columns, x_axis)
    chart = html.HtmlToastCharts.ChartBar(self.page, width, height, html_code, dfl_options, profile)
    return chart

  def scatter(self, record=None, y_columns=None, x_axis=None, profile=None, width=(100, "%"), height=(330, "px"),
              options=None, html_code=None):
    width = Arguments.size(width, unit="%")
    height = Arguments.size(height, unit="px")
    dfl_options = {"series": []}
    dfl_options.update({'y_columns': y_columns or [], 'x_axis': x_axis, 'commons': {'fill': None}})
    if options is not None:
      dfl_options.update(options)
    data = self.page.data.chartJs.y(record or [], y_columns, x_axis)
    chart = html.HtmlToastCharts.ChartScatter(self.page, width, height, html_code, dfl_options, profile)
    return chart

  def pie(self, record=None, y_columns=None, x_axis=None, profile=None, width=(100, "%"), height=(330, "px"),
           options=None, html_code=None):
    pass

  def donut(self, record=None, y_columns=None, x_axis=None, profile=None, width=(100, "%"), height=(330, "px"),
           options=None, html_code=None):
    pass

  def radial(self, record=None, y_columns=None, x_axis=None, profile=None, width=(100, "%"), height=(330, "px"),
           options=None, html_code=None):
    pass

  def gauge(self, record=None, y_columns=None, x_axis=None, profile=None, width=(100, "%"), height=(330, "px"),
           options=None, html_code=None):
    pass

  def heatmap(self, record=None, y_columns=None, x_axis=None, profile=None, width=(100, "%"), height=(330, "px"),
           options=None, html_code=None):
    pass

  def treetmap(self, record=None, y_columns=None, x_axis=None, profile=None, width=(100, "%"), height=(330, "px"),
           options=None, html_code=None):
    pass


class Components:

  def __init__(self, page):
    self.page = page

  def date(self, profile=None, width=(100, "%"), height=(330, "px"), options=None, html_code=None):
    if html_code is None:
      html_code = "tui_date_%s" % id(self)

    self.page.cssImport.add("tui-date-picker")
    self.page.jsImports.add("tui-date-picker")
    schema = {"type": 'div', 'css': None, 'children': [
      {"type": 'div', 'css': None, 'class': "tui-datepicker-input tui-datetime-input tui-has-focus", 'children': [
        {"type": 'input', "args": {"html_code": "%s_input" % html_code}, 'css': None,
         'arias': {"label": "Date-Time"}},
        {"type": 'span', 'class': "tui-ico-date", 'css': None},
      ]},
      {"type": 'div', "args": {"html_code": html_code}, 'css': None},
    ]}
    html_button = self.page.ui.composite(schema, options={"reset_class": True})
    html_button.set_builder('''var datepicker = new tui.DatePicker('#%(html_code)s', {
    date: new Date(),
    input: {element: '#%(html_code)s_input', format: 'yyyy-MM-dd'}
})''' % {"html_code": html_code})
    return html_button

  def calendar(self, profile=None, width=(100, "%"), height=(330, "px"), options=None, html_code=None):
    self.page.cssImport.add("tui-calendar")
    self.page.jsImports.add("tui-calendar")
    schema = {"type": 'div', 'css': None}

    html_button = self.page.ui.composite(schema, options={"reset_class": True})
    html_button.set_builder('''
var calendar = new tui.Calendar('#%(html_code)s', {
  defaultView: 'month',
  taskView: true,
  template: {
    monthDayname: function(dayname) {
      return '<span class="calendar-week-dayname-name">' + dayname.label + '</span>';
    }
  }
});    
''' % {"html_code": html_button.htmlCode})
    return html_button

  @property
  def charts(self):
    """
    Description:
    ------------

    https://nhn.github.io/tui.chart/latest/
    """
    return ToastCharts(self)

  def editor(self, value=None, profile=None, width=(100, "%"), height=(330, "px"), options=None, html_code=None):
    """
    Description:
    ------------

    :param value:
    :param profile:
    :param width:
    :param height:
    :param options:
    :param html_code:
    """
    dfl_options = {}
    if options is not None:
      dfl_options.update(options)
    editor = html.HtmlToastEditor.Editor(self.page, width, height, html_code, dfl_options, profile)
    if value is not None:
      editor.options.initialValue = value
    return editor
