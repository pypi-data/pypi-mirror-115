
from epyk.core.html.options import Options


class OptionsChartDataSeries(Options):
  @property
  def name(self):
    """
    Description:
    ------------

    Related Pages:


    """
    return self._config_get()

  @name.setter
  def name(self, text):
    self._config(text)

  @property
  def data(self):
    """
    Description:
    ------------

    Related Pages:


    """
    return self._config_get()

  @data.setter
  def data(self, values):
    self._config(values)

  @property
  def visible(self):
    """
    Description:
    ------------

    Related Pages:


    """
    return self._config_get()

  @visible.setter
  def visible(self, flag):
    self._config(flag)

  @property
  def stackGroup(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.chart/latest/tutorial-example02-17-bar-groupStack-chart-basic
    """
    return self._config_get()

  @stackGroup.setter
  def stackGroup(self, text):
    self._config(text)


class OptionsChartData(Options):

  @property
  def categories(self):
    """
    Description:
    ------------

    Related Pages:


    """
    return self._config_get()

  @categories.setter
  def categories(self, values):
    self._config(values)

  def add_series(self, name, data):
    """
    Description:
    -----------

    Related Pages:



    :rtype: OptionsChartDataSeries
    """
    new_series = self._config_sub_data_enum("series", OptionsChartDataSeries)
    new_series.name = name
    new_series.data = data
    return new_series


class OptionsChartAttrs(Options):

  @property
  def title(self):
    """
    Description:
    ------------

    Related Pages:


    """
    return self._config_get()

  @title.setter
  def title(self, values):
    self._config(values)

  @property
  def width(self):
    """
    Description:
    ------------

    Related Pages:


    """
    return self._config_get()

  @width.setter
  def width(self, num):
    self._config(num)

  @property
  def height(self):
    """
    Description:
    ------------

    Related Pages:


    """
    return self._config_get()

  @height.setter
  def height(self, num):
    self._config(num)


class OptionsTitle(Options):
  @property
  def text(self):
    """
    Description:
    ------------

    Related Pages:


    """
    return self._config_get()

  @text.setter
  def text(self, value):
    self._config(value)


class OptionsAxisLabel(Options):

  @property
  def interval(self):
    """
    Description:
    ------------

    Related Pages:


    """
    return self._config_get()

  @interval.setter
  def interval(self, num):
    self._config(num)


class OptionsScale(Options):

  @property
  def min(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.chart/latest/tutorial-example02-15-bar-stack-chart-dataLabels
    """
    return self._config_get()

  @min.setter
  def min(self, num):
    self._config(num)

  @property
  def max(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.chart/latest/tutorial-example02-15-bar-stack-chart-dataLabels
    """
    return self._config_get()

  @max.setter
  def max(self, num):
    self._config(num)

  @property
  def step(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.chart/latest/tutorial-example17-03-scale
    """
    return self._config_get()

  @step.setter
  def step(self, num):
    self._config(num)


class OptionsAxis(Options):

  @property
  def label(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.chart/latest/tutorial-example02-06-bar-chart-centerYAxis

    :rtype: OptionsAxisLabel
    """
    return self._config_sub_data("label", OptionsAxisLabel)

  @property
  def tick(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.chart/latest/tutorial-example17-04-tick-label-interval
    
    :rtype: OptionsAxisLabel
    """
    return self._config_sub_data("tick", OptionsAxisLabel)

  @property
  def scale(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.chart/latest/tutorial-example02-06-bar-chart-centerYAxis

    :rtype: OptionsScale
    """
    return self._config_sub_data("scale", OptionsScale)

  @property
  def title(self):
    """
    Description:
    ------------

    Related Pages:


    :rtype: OptionsTitle
    """
    return self._config_sub_data("title", OptionsTitle)

  def add_title(self, text):
    """
    Description:
    ------------

    Related Pages:


    :rtype: OptionsTitle
    """
    title = self._config_sub_data("title", OptionsTitle)
    title.text = text
    return title

  @property
  def align(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.chart/latest/tutorial-example02-06-bar-chart-centerYAxis
    """
    return self._config_get()

  @align.setter
  def align(self, text):
    self._config(text)

  @property
  def pointOnColumn(self):
    """
    Description:
    ------------

    """
    return self._config_get()

  @pointOnColumn.setter
  def pointOnColumn(self, flag):
    self._config(flag)


class OptionsDataLabels(Options):

  @property
  def visible(self):
    """
    Description:
    ------------

    """
    return self._config_get()

  @visible.setter
  def visible(self, flag):
    self._config(flag)

  @property
  def offsetY(self):
    """
    Description:
    ------------

    """
    return self._config_get()

  @offsetY.setter
  def offsetY(self, num):
    self._config(num)


class OptionsChartStack(Options):

  @property
  def type(self):
    """
    Description:
    ------------

    # normal, percent
    """
    return self._config_get()

  @type.setter
  def type(self, text):
    self._config(text)

  @property
  def connector(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.chart/latest/tutorial-example02-14-bar-stack-chart-connector
    """
    return self._config_get()

  @connector.setter
  def connector(self, flag):
    self._config(flag)


class OptionsChartSeries(Options):


  @property
  def dataLabels(self):
    """

    Related Pages:


    :rtype: OptionsDataLabels
    """
    return self._config_sub_data("dataLabels", OptionsDataLabels)

  @property
  def diverging(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.chart/latest/tutorial-example02-05-bar-chart-diverging
    """
    return self._config_get()

  @diverging.setter
  def diverging(self, flag):
    self._config(flag)

  @property
  def eventDetectType(self):
    """
    Description:
    ------------

    """
    return self._config_get()

  @eventDetectType.setter
  def eventDetectType(self, text):
    self._config(text)

  @property
  def selectable(self):
    """
    Description:
    ------------

    """
    return self._config_get()

  @selectable.setter
  def selectable(self, flag):
    self._config(flag)

  @property
  def shift(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.chart/latest/tutorial-example06-02-column-chart-liveUpdate
    """
    return self._config_get()

  @shift.setter
  def shift(self, flag):
    self._config(flag)

  @property
  def stack(self):
    """
    Description:
    ------------

    Related Pages:


    :rtype: OptionsChartStack
    """
    return self._config_sub_data("stack", OptionsChartStack)

  @property
  def spline(self):
    """
    Description:
    ------------

    """
    return self._config_get()

  @spline.setter
  def spline(self, flag):
    self._config(flag)

  @property
  def showDot(self):
    """
    Description:
    ------------

    """
    return self._config_get()

  @showDot.setter
  def showDot(self, flag):
    self._config(flag)

  @property
  def zoomable(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.chart/latest/tutorial-example01-09-area-chart-zoomable
    """
    return self._config_get()

  @zoomable.setter
  def zoomable(self, flag):
    self._config(flag)


class OptionsThemeSeries(Options):

  @property
  def areaOpacity(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.chart/latest/tutorial-example01-12-area-chart-theme
    """
    return self._config_get()

  @areaOpacity.setter
  def areaOpacity(self, num):
    self._config(num)

  @property
  def barWidth(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.chart/latest/tutorial-example02-10-bar-chart-theme
    """
    return self._config_get()

  @barWidth.setter
  def barWidth(self, num):
    self._config(num)

  @property
  def colors(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.chart/latest/tutorial-example01-12-area-chart-theme
    """
    return self._config_get()

  @colors.setter
  def colors(self, values):
    self._config(values)

  @property
  def dashSegments(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.chart/latest/tutorial-example01-12-area-chart-theme
    """
    return self._config_get()

  @dashSegments.setter
  def dashSegments(self, array):
    self._config(array)

  @property
  def lineWidth(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.chart/latest/tutorial-example01-12-area-chart-theme
    """
    return self._config_get()

  @lineWidth.setter
  def lineWidth(self, num):
    self._config(num)


class OptionsTheme(Options):

  @property
  def series(self):
    """

    Related Pages:

      https://nhn.github.io/tui.chart/latest/tutorial-example01-12-area-chart-theme

    :rtype: OptionsThemeSeries
    """
    return self._config_sub_data("series", OptionsThemeSeries)


class OptionsLegend(Options):

  @property
  def align(self):
    """
    Description:
    ------------

    Related Pages:

      https://nhn.github.io/tui.chart/latest/tutorial-example02-10-bar-chart-theme
    """
    return self._config_get()

  @align.setter
  def align(self, text):
    self._config(text)


class OptionsTooltip(Options):
  def formatter(self):
    """
    Related Pages:

      https://nhn.github.io/tui.chart/latest/tutorial-example08-04-line-chart-spline

    """
    pass


class OptionsChartOpts(Options):

  @property
  def chart(self):
    """

    Related Pages:


    :rtype: OptionsChartAttrs
    """
    return self._config_sub_data("chart", OptionsChartAttrs)

  @property
  def legend(self):
    """

    Related Pages:


    :rtype: OptionsLegend
    """
    return self._config_sub_data("legend", OptionsLegend)

  @property
  def tooltip(self):
    """
    Related Pages:


    :rtype: OptionsLegend
    """
    return self._config_sub_data("tooltip", OptionsTooltip)

  @property
  def theme(self):
    """
    Related Pages:


    :rtype: OptionsTheme
    """
    return self._config_sub_data("theme", OptionsTheme)

  @property
  def series(self):
    """
    Related Pages:


    :rtype: OptionsChartAttrs
    """
    return self._config_sub_data("series", OptionsChartSeries)

  @property
  def xAxis(self):
    """
    Related Pages:


    :rtype: OptionsAxis
    """
    return self._config_sub_data("xAxis", OptionsAxis)

  @property
  def yAxis(self):
    """
    Related Pages:


    :rtype: OptionsAxis
    """
    return self._config_sub_data("yAxis", OptionsAxis)

  @property
  def usageStatistics(self):
    """
    Description:
    ------------

    """
    return self._config_get(False)

  @usageStatistics.setter
  def usageStatistics(self, flag):
    self._config(flag)


class OptionsCharts(Options):

  @property
  def config(self):
    """

    Related Pages:


    :rtype: OptionsChartOpts
    """
    return self._config_sub_data("options", OptionsChartOpts)

  @property
  def data(self):
    """

    Related Pages:


    :rtype: OptionsChartData
    """
    return self._config_sub_data("data", OptionsChartData)

