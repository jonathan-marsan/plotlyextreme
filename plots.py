import pandas as pd
from plotly.offline import iplot
import plotly.graph_objs as go
import plotly

import utilities


def create_big_number(title, large_number, pacing='--'):
    pacing_font_color = utilities.warning_color_font(pacing)
    background_color = utilities.warning_color_background(pacing)
    fig = {
        "data": [
          {
            "values": [100],
            "labels": [
              "Results"
            ],
            "hoverinfo":'none',
            'textinfo':'none',
            "hole": 1.0,
            "type": "pie"

          }],
        "layout": {
              "title": title,
              "titlefont": {
                "size": 30
              },
              "showlegend": False,
              "height": 300,
              "width": 280,
              "paper_bgcolor": background_color,
              "annotations": [
                      {
                          "font":
                              {
                                  "size": 40,
                                  "family": 'Arial'
                              },
                          "showarrow": False,
                          "text": utilities.add_thousand_separator(large_number),
                          "x": 0.5,
                          "y": 0.5
                      },
                      {
                          "font":
                              {
                                  "size": 18,
                                  "color": pacing_font_color
                              },
                          "showarrow": False,
                          "text": utilities.perc_format(pacing) + ' of pacing',
                          "x": 0.5,
                          "y": 0.02
                      }
                  ]
          }
      }
    return iplot(fig)


def plot_four_dimensions(df, x, y, title, segmentation_col, button_col, buttons,
                         default_visibility, labels=[], y_tick_format=''):
    """
    Plot four dimensions using a plotly line chart and buttons
    df = dataframe with four dimensions, typically time, metric, and two categorical variables
    x = column for x-axis
    y = column for y-axis
    title = default title for graph
    segmentation_col = third dimension in the graph, segmenting the data
    button_col = fourth dimension in the graph showing a subset of x, y and segmentation_col based on this column
    buttons = enables ordering the buttons
    default_visibility = enables selection of which graph is shown on load
    color_list = not required if fewer than 22 dimensions (and you shouldn't be making a graph if you have more than that). Enables overwriting colors.
    """
    color_list = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080']

    # Clean up some strings
    buttons = [element.lower() for element in buttons]
    button_col = button_col.lower()
    default_visibility = default_visibility.lower()

    default_title = title + ' ' + default_visibility.capitalize()
    segments = utilities.get_unique_values(df, segmentation_col)
    traces_dict = utilities.produce_traces(df, button_col, buttons, segmentation_col, segments, x, y, default_visibility, color_list, labels)
    traces_list = utilities.df_list(buttons, traces_dict)
    updatemenus = utilities.create_update_menus(buttons, traces_dict, title)

    layout = dict(title=default_title,
                  showlegend=True,
                  updatemenus=updatemenus,
                  yaxis=go.layout.YAxis(tickformat=y_tick_format),
                  # xaxis = go.layout.XAxis(tickformat = '%Y-%m-%d'),
                  width=950,
                  height=440,
                  legend=dict(orientation='h'),
                  # margin=dict(t=0, b=0, l=0, r=0)
                  )

    fig = dict(data=traces_list, layout=layout)
    return iplot(fig)
