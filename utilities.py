import pandas as pd
import plotly
import plotly.graph_objs as go


def warning_color_font(value):
    if isinstance(value, float):
        if value > 1.2:
            return '#339900'
        elif value > 1.0:
            return '#99cc33'
        elif value > .95:
            return '#ffcc00'
        elif value > .9:
            return '#ff9966'
        else:
            return '#cc3300'
    # Set to black font if no value
    return '#000000'


def warning_color_background(value):
    if isinstance(value, float):
        if value > 1.2:
            return '#e5ffe7'
        elif value > 1.0:
            return '#efffe5'
        elif value > .95:
            return '#fff9e5'
        elif value > .9:
            return '#fff4ef'
        else:
            return '#f9eae5'
    # Set to white background if no value
    return '#ffffff'


def add_thousand_separator(value):
    try:
        return "{:,}".format(value)
    except:
        return value


def perc_format(value):
    try:
        return "{:.2%}".format(value)
    except:
        return value


def get_unique_values(df, column):
    """
    Get unique strings from a column.
    Numeric or other types of values will error out.
    """
    unique_values = list(set(list(df[[column]][column])))
    return [value.lower() for value in unique_values]


def create_labels(df, cols):
    hover_text = list()
    for index, row in df.iterrows():
        data_point_label = ''
        for col in cols:
            data_point_label = data_point_label + col + ': ' + str(row[col]) + '<br />'
        hover_text.append(data_point_label)
    return hover_text


def produce_traces(df, button_col, buttons, segmentation_col, segments, x, y,
                   default_visibility, color_list, labels):
    df[segmentation_col] = df[segmentation_col].str.lower()
    df[button_col] = df[button_col].str.lower()
    df = df.sort_values(by=[x])
    graph_trace_dict = {}
    for button in buttons:
        segment_dict = {}
        line_color_index = 0
        for segment in segments:
            button_segment_df = get_df_subset(df, button_col, button,
                                              segmentation_col, segment)
            rows_in_df = button_segment_df.shape[0]
            if not labels:
                labels = [x, y]
            trace_hover_text = create_labels(button_segment_df, labels)
            segment_dict.update(
              {
                segment.lower(): go.Scatter(x=list(button_segment_df[x]),
                                            y=list(button_segment_df[y]),
                                            text=trace_hover_text,
                                            hoverinfo='text',
                                            name=segment.lower(),
                                            visible=(button == default_visibility),
                                            line=dict(color=color_list[line_color_index]))
              }
            )
            if rows_in_df > 0:
                # Add this so we only change color when new subset is available
                # (but not for empty subsets)
                line_color_index += 1
        graph_trace_dict.update(
            {
                button.lower(): segment_dict
            }
        )
    return graph_trace_dict


def get_df_subset(df, column_one, value_one, column_two, value_two):
    """
    Takes a dataframe and filters it based on two columns and their matching values
    """
    return df.loc[(df[column_one] == value_one) & (df[column_two] == value_two), :]


def df_list(buttons, traces_dict):
    buttons = [element.lower() for element in buttons]
    graph_trace_list = list()
    for button in buttons:
            for segment, segment_traces in traces_dict.get(button).items():
                try:
                    graph_trace_list.append(segment_traces)
                except:
                    print('missing attribute ' + segment + 'in ' + button)
    return graph_trace_list


def create_visibility_buttons_booleans(buttons, traces_dict):
    graph_visibility_by_button = dict()
    for button in buttons:
        visibility_list = list()
        for element, elements in traces_dict.items():
            for segment, segments in elements.items():
                visibility_list.append(button == element)
            graph_visibility_by_button.update(
                    {
                        button: visibility_list
                    }
                )
    return graph_visibility_by_button


def create_button_update_list(buttons, traces_dict, title):
    graph_visibility_by_button = create_visibility_buttons_booleans(buttons,
                                                                    traces_dict)
    buttons_update_list = list()
    for button in buttons:
        button_parameters = dict(label=button.capitalize(),
                                 method='update',
                                 args=[{'visible': graph_visibility_by_button.get(button)},
                                       {'title': title.capitalize() + ' ' + button.capitalize()}])
        buttons_update_list.append(button_parameters)
    return buttons_update_list


def create_update_menus(buttons, traces_dict, title):
    visibility_buttons = create_button_update_list(buttons, traces_dict, title)
    updatemenus = list([
                        dict(
                            type="buttons",
                            buttons=visibility_buttons,
                            # direction = 'left',
                            pad={'r': 30, },
                            # showactive = True,
                        )])
    return updatemenus
