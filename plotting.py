import pandas as pd
import plotly.subplots as sp
import plotly.graph_objects as go
import data_retrieval as dr

GRID_COLOR = '#32383e'
GRID_WIDTH = 1


class Options:
    def __init__(self, add_deltas: bool):
        self.add_deltas = add_deltas


class Column:
    """
    Class to store the column names of the telemetry data.
    """

    def __init__(self, pretty_name, data_name, units, min_value, max_value):
        self.pretty_name = pretty_name
        self.data_name = data_name
        self.units = units
        self.min_value = min_value
        self.max_value = max_value

""" UNUSED """
def columns_exist(lap: dr.Lap, columns):
    """
    Checks if the columns exist in the dataframe.
    """
    df = lap.processed_lap_data
    for column in columns:
        if column not in df.columns:
            print(f"Column '{column}' does not exist in the lap: {lap.print_lap_name()}")
            return False
    return True


def get_default_fig():
    """
    Returns a figure with default formatting.
    """
    fig = go.Figure()

    return fig

def are_same_lap(lap_one: dr.Lap, lap_two: dr.Lap):
    """
    Checks if two laps are the same. This is done by checking if the lap names are the same.
    """
    return lap_one.print_lap_name() == lap_two.print_lap_name() and lap_one.lap_number == lap_two.lap_number


def add_lap_delta(ref_lap, compare_lap):
    ref = ref_lap.processed_lap_data
    lap1 = compare_lap.processed_lap_data

    ref_lap_distances = ref['Distance'].astype(float).to_list()
    ref_lap_velocities = ref['Ground Speed'].astype(float).to_list()

    lap1_distances = lap1['Distance'].astype(float).to_list()
    lap1_velocities = lap1['Ground Speed'].astype(float).to_list()

    deltas = []

    for i in range(len(ref['Time'])):
        try:
            d1 = ref_lap_distances[i]
            d2 = lap1_distances[i]

            v1 = ref_lap_velocities[i] * 1000 / 3600
            v2 = lap1_velocities[i] * 1000 / 3600
            cur_delta = (((d1 - d2) / v2) + ((d1 - d2) / v1)) / 2
            deltas.append(cur_delta)
        except:
            pass
    while (len(lap1['Time']) != len(deltas)):
        deltas.append(deltas[len(deltas) - 1])
    lap1['Delta'] = deltas
    compare_lap.processed_lap_data = lap1
    return compare_lap


def add_deltas(laps):
    ref_lap = laps[0]
    delta_added_laps = [ref_lap]
    for lap_no in range(len(laps)):
        if lap_no != 0:
            # print(f"Adding delta for {lap.print_lap_name()}")
            delta_added_laps.append(add_lap_delta(ref_lap, laps[lap_no]))
    return delta_added_laps


def process_options(laps, options: Options):
    if options.add_deltas:
        laps = add_deltas(laps)

    return laps


def generate_plot(laps, columns, options: Options = None):
    if Options is not None:
        laps = process_options(laps, options)

    fig = get_default_fig()
    fig.set_subplots(rows=len(columns), cols=1, shared_xaxes=True, vertical_spacing=0.005,
                     row_width=[0.2, 0.12, 0.12, 0.12, 0.2, 0.30])
    colours = ['rgba(0, 210, 190, 0.9)', 'rgba(220, 0, 0, 0.9)', 'rgba(6, 0, 239, 0.9)']
    for lap_no, cur_lap in enumerate(laps):
        lap = cur_lap.processed_lap_data
        for row, telem_column in enumerate(columns):
            if telem_column not in lap.columns:
                # print(f"Column '{telem_column}' does not exist in the lap: {cur_lap.print_lap_name()}")
                continue

            trace = go.Scatter(x=lap['Distance'], y=lap[telem_column], mode='lines', name=cur_lap.print_lap_name(),
                               legendgroup=lap_no, showlegend=True if row == 0 else False, line_color=colours[lap_no])
            fig.add_trace(trace, row=row + 1, col=1)
            fig.update_yaxes(range=[lap[telem_column].min(), lap[telem_column].max()], title_text=telem_column,
                             nticks=10, row=row + 1, col=1, showgrid=False, zeroline=True)
            # fig.update_xaxes(
            #     tickmode='array',
            #     tickvals=[270, 500, 950, 1430],
            #     ticktext=['T1', 'Str', 'T2', 'Str']
            # )
    fig.update_layout(
        xaxis_showticklabels=True,
        # xaxis_title_text="Distance (m)",
        # xaxis_side="top",
        # xaxis4_title_text="Distance (m)",
        margin=dict(t=4, l=4, r=16, b=4),
        # """ SIZE NEEDS FIXING """
        height=900,
        width=1200,
        autosize=False,
    )
    # fig.update_layout(
    #     xaxis=dict(
    #         tickmode='array',
    #         tickvals=[270, 500, 950, 1430],
    #         ticktext=['T1', 'Str', 'T2', 'Str']
    #     )
    # )
    fig.update_layout(
        showlegend=True  # Disable the default legend
    )
    fig.update_layout(legend=dict(
        orientation="h",
        entrywidth=150,
        yanchor="bottom",
        y=1,
        xanchor="right",
        x=0.5
    ))

    fig.update_yaxes(
        gridwidth=GRID_WIDTH,
        gridcolor=GRID_COLOR,
        showline=False,
        zeroline=False
    )

    fig.update_xaxes(
        gridwidth=GRID_WIDTH,
        gridcolor=GRID_COLOR,
    )
    fig.show()


# TESTING CODE

# raw_stint1 = pd.read_csv('Test Data/Id Files/230814/spa_nissan_wec_20hz_stint1.csv', header=[14],
#                          skiprows=[15, 16, 17])
# proc_stint1 = dr.get_split_laps(raw_stint1, "ONE")
#
# raw_stint2 = pd.read_csv('Test Data/Id Files/230814/spa_nissan_wec_20hz_stint3.csv',
#                          header=[12], skiprows=[15])
# proc_stint2 = dr.get_split_laps(raw_stint2, "TWO")
#
# lap2 = proc_stint2.laps[2]
# lap1 = proc_stint1.laps[6]
# lap3 = proc_stint1.laps[7]
#
# # print("Done procesing")
# laps = [lap1, lap2, lap3]
# columns = ['Ground Speed', 'Steering Angle', 'Brake Pos', 'Throttle Pos', 'Delta']
#
# # column_new = [
# #     Column('Velocity', 'Ground Speed', 'm/s', 0, 120)
# #     , Column('Steering Angle', 'Steering Angle', 'deg', -100, 100)
# #     , Column('Brake Position', 'Brake Pos', '%', 0, 100)
# #     , Column('Throttle Position', 'Throttle Pos', '%', 0, 100)
# # ]
# # #
# generate_plot(lap2, laps, columns, options=Options(add_deltas=True))
