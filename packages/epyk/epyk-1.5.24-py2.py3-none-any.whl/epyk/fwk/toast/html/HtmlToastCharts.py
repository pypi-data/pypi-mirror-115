#!/usr/bin/python
# -*- coding: utf-8 -*-

from epyk.core.css import Colors
from epyk.core.html import Html
from epyk.fwk.toast.options import OptToastCharts


class Chart(Html.Html):
  name = 'ToastCharts'
  requirements = ('@toast-ui/chart', )
  _option_cls = OptToastCharts.OptionsCharts

  def __init__(self, report, width, height, html_code, options, profile):
    self.height = height[0]
    super(Chart, self).__init__(
      report, [], html_code=html_code, profile=profile, options=options, css_attrs={"width": width, "height": height})
    self.config.usageStatistics = False

  _js__builder__ = '''
    options.el = htmlObj; const editor = new toastui.Chart.lineChart(options)'''

  @property
  def data(self):
    """
    Description:
    -----------
    Return the data section from the main python options.
    """
    return self.options.data

  @property
  def config(self):
    """
    Description:
    -----------
    Returns the options option for the chart.
    """
    return self.options.config

  @property
  def options(self):
    """
    Description:
    -----------

    :rtype: OptToastCharts.OptionsCharts
    """
    return super().options

  def __str__(self):
    self.page.properties.js.add_builders(self.build())
    return '<div %s></div>' % self.get_attrs(pyClassNames=self.style.get_classes())


class ChartArea(Chart):
  name = 'ToastChartsArea'
  _js__builder__ = '''options.el = htmlObj; const editor = new toastui.Chart.areaChart(options)'''


class ChartColumn(Chart):
  name = 'ToastChartsColumn'
  _js__builder__ = '''options.el = htmlObj; const editor = new toastui.Chart.columnChart(options)'''


class ChartBar(Chart):
  name = 'ToastChartsBar'
  _js__builder__ = '''options.el = htmlObj; const editor = new toastui.Chart.barChart(options)'''


class ChartScatter(Chart):
  name = 'ToastChartsScatter'
  _js__builder__ = '''options.el = htmlObj; const editor = new toastui.Chart.scatterChart(options)'''


class ChartBubble(Chart):
  name = 'ToastChartsBubble'
  _js__builder__ = '''options.el = htmlObj; const editor = new toastui.Chart.bubbleChart(options)'''
