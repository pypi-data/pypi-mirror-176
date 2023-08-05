from pyadlml.constants import ACTIVITY, START_TIME, END_TIME

def _style_colorbar(fig, label):
    fig.update_traces(colorbar=dict(
        title=dict(text=label, font=dict(size=10)),
        titleside='right',
        thickness=10,
    ))

def _dyn_y_label_size(plot_height, nr_labels):

    if nr_labels < 15:
        return 12
    elif nr_labels < 20:
        return 11
    elif nr_labels < 30:
        return 10
    else:
        return 9
import pandas as pd

class ActivityDict(dict):
    """ Dictionary with activity pd.DataFrames as values and subject names as keys.
    """
    def nr_acts(self):
        """"""
        return max([len(df_acts[ACTIVITY].unique()) for df_acts in self.values()])

    def get_activity_union(self): 
        return list(set([item for v in self.values() \
                              for item in v[ACTIVITY].unique()]))

    def get_min_start_time(self):
        return min([df_acts[START_TIME].iloc[0] for df_acts in self.values()])

    def get_max_end_time(self):
        return min([df_acts[END_TIME].iloc[-1] for df_acts in self.values()])

    def concat(self):
        return pd.concat(self.values())