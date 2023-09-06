import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# stint1 = pd.read_csv('Test Data/Id Files/230814/Stint1.csv', header=[0])

DEFAULT_LAP_COLUMN_NAME = 'Last Lap Time'

class Stint:
    def __init__(self, raw_stint_data: pd.DataFrame, laps: list, name: str):
        self.raw_stint_data = raw_stint_data
        self.laps = laps
        self.name = name

    def show_laps(self):
        print("-----------------------------")
        print("- Lap # -      Laptime      ")
        print("-----------------------------")
        for i in range(len(self.laps)):
            print(f"Lap {i} - {self.laps[i]}")

    def display_laps(self):
        trace = go.Table(
            header=dict(values=["Lap Number", "Lap Time"]),
            cells=dict(values=[list(range(0, len(self.laps))), [pretty_print_laptime(lap.laptime) for lap in self.laps]]),
            columnwidth=[15, 25]
        )
        # Create a subplot to display the table
        fig = make_subplots(rows=1, cols=1)

        fig.add_trace(trace)

        # Update the layout to remove axes and gridlines
        fig.update_layout(
            title=f"{self.name} Lap Table",
            title_x=0,
            xaxis=dict(showticklabels=False),
            yaxis=dict(showticklabels=False),
        )

        # Show the table
        fig.show()


class Lap:
    def __init__(self, raw_lap_data, laptime, stint_name, lap_number):
        self.raw_lap_data = raw_lap_data
        self.processed_lap_data = self.process_lap_data(raw_lap_data)
        self.laptime = laptime
        self.stint_name = stint_name
        self.lap_number = lap_number

    def process_lap_data(self, raw_lap_data : pd.DataFrame):
        proc_data = raw_lap_data
        proc_data['Distance'] = proc_data['Distance'].astype(float) - proc_data['Distance'].astype(float).iloc[0]
        proc_data['Time'] = proc_data['Time'].astype(float) - proc_data['Time'].astype(float).iloc[0]
        return proc_data

    def __str__(self):
        return f"{pretty_print_laptime(self.laptime)}"

    def print_lap_name(self):
        return f"{self.stint_name} - {pretty_print_laptime(self.laptime)}"


def pretty_print_laptime(laptime: float):
    minutes = int(laptime // 60)
    seconds = int(laptime % 60)
    milliseconds = int((laptime - int(laptime)) * 1000)

    return f'{minutes:01d}:{seconds:02d}.{milliseconds:03d}'


def get_split_laps(stint_data: pd.DataFrame, stint_name: str):
    # Find where the laps split
    previous_value = None
    change_indices = []

    for index, value in enumerate(stint_data[DEFAULT_LAP_COLUMN_NAME]):
        if value != previous_value:
            change_indices.append(index)
        previous_value = value

    change_indices.append(len(stint_data[DEFAULT_LAP_COLUMN_NAME]))

    if (len(change_indices) % 2) != 0:
        raise Exception('Number of Lap change indices is not even, cannot split laps! Lap change indices found: ',
                        change_indices)

    laps = []
    lap_number = 0
    for i in range(0, len(change_indices) - 1):

        try:
            cur_lap_data = stint_data.iloc[change_indices[i]:change_indices[i + 1]]
        except:
            # print(f"Failed to retrieve lap data from lap: {lap_number}, using fall-back")
            cur_lap_data = stint_data.iloc[change_indices[i]:change_indices[i + 1] - 1]
        try:
            cur_lap_time = stint_data[DEFAULT_LAP_COLUMN_NAME].iloc[change_indices[i + 1] + 1]
        except IndexError:
            # print(f"Failed to retrieve laptime from lap: {lap_number}, using fall-back")
            cur_lap_time = stint_data['Lap Time'].iloc[change_indices[i + 1] - 1]

        # print(f"{lap_number} - {pretty_print_laptime(cur_lap_time)}")

        cur_lap = Lap(
            cur_lap_data,
            cur_lap_time,
            stint_name,
            lap_number
        )
        laps.append(cur_lap)
        lap_number += 1

    return Stint(stint_data, laps, stint_name)

