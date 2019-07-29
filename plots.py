# Note: This functions won't work without pandas
# import pandas as pd

from plotlyextreme import utilities


def create_big_number(title, large_number, render_func, pacing='--'):
    """
    title = description of big number
    large_number = whatever number you want to highlight
    render_func = plotly rendering function like iplot
    """
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
    return render_func(fig)


def plot_four_dimensions(df, x, y, title, segmentation_col, button_col,
                         buttons, default_visibility, trace_func, render_func,
                         x_layout='', y_layout='', labels=[]):
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
    trace_func = plotly trace function like plotly.graph_objs.Scatter
    render_func = plotly rendering function like iplot
    color_list = not required if fewer than 22 dimensions. Enables overwriting of colors.
    """
    color_list = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080']

    # Clean up some strings
    buttons = [element.lower() for element in buttons]
    button_col = button_col.lower()
    default_visibility = default_visibility.lower()

    default_title = title + ' ' + default_visibility.capitalize()
    segments = utilities.get_unique_values(df, segmentation_col)
    traces_dict = utilities.produce_traces(df=df, button_col=button_col,
                                           buttons=buttons,
                                           segmentation_col=segmentation_col,
                                           segments=segments, x=x, y=y,
                                           default_visibility=default_visibility,
                                           color_list=color_list,
                                           labels=labels, trace_func=trace_func)
    traces_list = utilities.df_list(buttons, traces_dict)
    updatemenus = utilities.create_update_menus(buttons, traces_dict, title)

    layout = dict(title=default_title,
                  showlegend=True,
                  updatemenus=updatemenus,
                  width=950,
                  height=440,
                  legend=dict(orientation='h')
                  )

    # Enable usage of plotly function like plotly.graph_objs.layout.XAxis
    if x_layout != '':
        layout.update({'xaxis': x_layout})

    if y_layout != '':
        layout.update({'yaxis': y_layout})

    fig = dict(data=traces_list, layout=layout)

    return render_func(fig)
