import math
from collections import OrderedDict
from .util import _style_colorbar, _dyn_y_label_size
import plotly
import pandas as pd
import numpy as np

from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.express import IdentityMap
from plotly.express._core import apply_default_cascade, infer_config, \
    get_label, make_trace_kwargs, get_decorated_label, init_figure, make_trendline_spec, configure_axes, \
    configure_animation_controls, process_dataframe_timeline, one_group, \
    get_groups_and_orders

#from plotly.subplots import _subplot_type_for_trace_type, _set_trace_grid_reference
from plotly.validators.choropleth import ColorscaleValidator
from pyadlml.constants import DEVICE, TIME, ACTIVITY, START_TIME, END_TIME, VALUE, NUM, BOOL, \
    CAT, STRFTIME_DATE
import plotly.express as px

from pyadlml.dataset._core.devices import device_events_to_states
from pyadlml.dataset.matplotlib.util import format_device_labels
from pyadlml.dataset.plotly.activities import _set_compact_title
from pyadlml.dataset.stats.acts_and_devs import contingency_table_states, contingency_table_events
from pyadlml.dataset.util import select_timespan, df_difference, activity_order_by, device_order_by, infer_dtypes


__all__ = ['activities_and_devices', 'contingency_states', 'contingency_events']


def _plot_device_states_into_fig(fig: go.Figure, df_devs: pd.DataFrame,  df_devs_usel: pd.DataFrame,
                                 df_devs_outside: pd.DataFrame, dev_order: list, st=None, et=None) -> go.Figure:
    """
    Parameters
    ----------
    df_devs_outside : list of dicts
        Each dictionary contains the key 'df' and a 'color' and a 'opacity'


    """
    EVENT_COLOR = 'Black'
    #marker = dict(size=5, symbol=42, line=dict(color=EVENT_COLOR, width=1))

    df_devs = df_devs.copy()\
                        .sort_values(by=TIME)\
                        .reset_index(drop=True)
    devs = df_devs[DEVICE].unique()
    dtypes = infer_dtypes(df_devs)
    df_devs = device_events_to_states(df_devs, extrapolate_states=True,
                                      st=st, et=et).reset_index(drop=True)

    if df_devs_usel is not None:
        mark_selected = {}
        df_devs_usel = df_devs_usel.rename(columns={TIME: START_TIME})
        if END_TIME not in df_devs_usel.columns:
            tmp = df_devs.copy()
            comp_df = tmp[[START_TIME, DEVICE, VALUE]]\
                      .merge(df_devs_usel, indicator=True, how='left')
            mask = (comp_df['_merge'] == 'both')
            tmp2 = tmp[mask]
            df_devs_usel = tmp2
        df_devs_usel = _endtime_to_offset(df_devs_usel, replace=False)
        df_devs_usel[VALUE] = df_devs_usel[VALUE].map({True: 'on', False: 'off'})


    df_devs = _endtime_to_offset(df_devs, replace=False)

    # A mapping from device to data index
    data_dict = {}
    j = 0
    first_bool = True
    for i, dev in enumerate(devs):
        df = df_devs[df_devs[DEVICE] == dev].copy()

        if dev in dtypes[BOOL]:
            df[VALUE] = df[VALUE].map({True: 'on', False: 'off'})
            df_on = df[df[VALUE] == 'on']
            df_off = df[df[VALUE] == 'off']

            if df_devs_usel is not None:
                mark_selected[dev] = {}
                comp_df = df_on.copy().merge(df_devs_usel, indicator=True, how='left')
                tmp = np.where((comp_df['_merge'] == 'both').values)[0]
                comp_df2 = df_off.copy().merge(df_devs_usel, indicator=True, how='left')
                tmp2 = np.where((comp_df2['_merge'] == 'both').values)[0]
                mark_selected[dev]['on'] = tmp
                mark_selected[dev]['off'] = tmp2

            COL_TRUE = 'teal'
            COL_FALSE = 'lightgray'
            hover_template = '%{y}<br>' + \
                             'Start_time: %{base|' + STRFTIME_DATE + '}<br>' + \
                             'End_time: %{customdata[1]|' + STRFTIME_DATE + '}<br>' + \
                             'Duration: %{customdata[0]}<br>' + \
                             'State: %{customdata[2]}<extra></extra>'

            def create_trace(df, state):
                df['diff'] = (df[END_TIME] - df[START_TIME]).astype(str)
                cd = df[['diff', END_TIME]].values
                # Add state information to custom_data
                vals = np.expand_dims(np.full(cd.shape[0], (state == 'on')), axis=1)
                cd = np.hstack([cd, vals])
                marker_color = COL_TRUE if state == 'on' else COL_FALSE
                return go.Bar(name=state,
                              base=df[START_TIME],
                              meta=dev,
                              x=df['offset'],
                              y=df[DEVICE],
                              marker_color=marker_color,
                              customdata=cd,
                              legendgroup=state,
                              orientation='h',
                              width=0.3,
                              textposition='auto',
                              showlegend=first_bool,
                              hovertemplate=hover_template,
                )

            trace_off = create_trace(df_off, 'off')
            trace_on = create_trace(df_on, 'on')
            data_dict[dev] = [len(fig.data), len(fig.data)+1]
            fig.add_traces([trace_on, trace_off])

            first_bool = False
        elif dev in dtypes[CAT]:
            categories = df.loc[df[DEVICE] == dev, VALUE].unique()
            for cat in categories:
                #values = df.loc[(df[VAL] == cat), [col_bar_start, col_bar_len]].values.tolist()
                #ax.broken_barh(values, (i-0.25, 0.5), facecolors=tab(j), label=dev + ' - ' + cat)
                j += 1
            raise NotImplementedError

        elif dev in dtypes[NUM]:
            values = pd.to_numeric(df[VALUE])
            values = (values-values.min())/(values.max() - values.min())*0.5
            values = values + i - 0.25
            #ax.plot(df['num_st'], values, color=color_num, linestyle='--', marker='o')
            raise NotImplementedError

        # Create user_selection for each trace
        if df_devs_usel is not None:
            if dev in dtypes[BOOL]:
                fig.update_traces(selector=dict(meta=dev, name='off'),
                           selectedpoints=mark_selected[dev]['off'],
                           selected={'marker': {'opacity': 1.0, 'color': COL_FALSE}},
                           unselected={'marker': {'opacity': 0.3, 'color': COL_FALSE}})
                fig.update_traces(selector=dict(meta=dev, name='on'),
                           selectedpoints=mark_selected[dev]['on'],
                           selected={'marker': {'opacity': 1.0, 'color': COL_TRUE}},
                           unselected={'marker': {'opacity': 0.3, 'color': COL_TRUE}})
            else:
                raise NotImplementedError


    fig.update_layout(yaxis_type='category')
    fig.update_yaxes(categoryorder='array', categoryarray=np.flip(dev_order))

    return fig


def _plot_device_events_into_fig(fig: go.Figure, df_devs: pd.DataFrame,  df_devs_usel: pd.DataFrame,
                                 df_devs_outside: pd.DataFrame, dev_order: list,
                                 marker_height=5,
                                 ) -> go.Figure:
    """
    Parameters
    ----------
    df_devs_outside : list of dicts
        Each dictionary contains the key 'df' and a 'color' and a 'opacity'


    """
    # Enable webgl rendering
    scatter = go.Scattergl if len(df_devs) > 15000 else go.Scatter
    EVENT_COLOR = 'Black'
    hover_template = '%{y}<br>%{x|' + STRFTIME_DATE + '}<br>Event: %{customdata} <extra></extra>'


    marker = dict(size=marker_height, symbol=42, line=dict(color=EVENT_COLOR, width=1))
    fig.update_layout(yaxis_type='category')
    fig.update_yaxes(categoryorder='array', categoryarray=np.flip(dev_order))
    fig.add_trace(scatter(
        mode='markers', y=df_devs[DEVICE], x=df_devs[TIME],
        customdata=df_devs[VALUE],
        hovertemplate=hover_template,
        showlegend=False, marker=marker))

    if not df_devs_outside.empty:
        marker['opacity'] = 0.1
        marker['line']['color'] = 'Grey'
        fig.add_trace(scatter(mode='markers', y=df_devs_outside[DEVICE],
                                 x=df_devs_outside[TIME], showlegend=False,
                                 marker=marker, hoverinfo='skip')
                      )

    # Create user_selection for each trace
    if df_devs_usel is not None:
        df_devs_usel = df_devs_usel[[TIME, DEVICE, VALUE]]
        # Get the indices in the trace where
        comp_df = df_devs.copy().merge(df_devs_usel, indicator=True, how='left')
        mark_selected = np.where((comp_df['_merge'] == 'both').values)[0]
        unselected = {'marker': {'opacity': 0.2, 'color': EVENT_COLOR}}
        selected = {'marker': {'opacity': 1.0, 'color': 'Red'}}
        fig.update_traces(selector=dict(type="scatter"),
                          selectedpoints=mark_selected,
                          selected=selected, unselected=unselected)

    return fig


def _determine_start_and_end(df_acts: dict, df_devs: pd.DataFrame, st: pd.Timestamp, et: pd.Timestamp):
    """ Determine the start and endpoint with regard to optional given parameters
    """
    if isinstance(df_acts, pd.DataFrame):
        act_st = df_acts[START_TIME].iloc[0]
        act_et = df_acts[END_TIME].iloc[-1]
    elif isinstance(df_acts, dict):
        act_st = df_acts.get_min_start_time()
        act_et = df_acts.get_max_end_time()

    data_st = min(df_devs[TIME].iloc[0], act_st) - pd.Timedelta('1ms')
    data_et = max(df_devs[TIME].iloc[-1], act_et) + pd.Timedelta('1ms')
    if st is None:
        draw_start_line = False
        st = data_st
    else:
        # Draw the line only if the given start is the right-most
        draw_start_line = (max(st, data_st) == st)
        st = max(st, data_st)
    if et is None:
        draw_end_line = False
        et = data_et
    else:
        # Draw the line only if the given end is the left-most
        draw_end_line = (min(et, data_et) == et)
        et = min(et, data_et)
    return st, et, draw_start_line, draw_end_line



def ActDictLoop(func):
    def func_wrapper(*args, **kwargs):
    if isinstance(df_acts_sel, pd.DataFrame):
            df_acts_sel = ActivityDict(dict(tmp=df_acts_sel))
        if isinstance(df_acts, pd.DataFrame):
            df_acts = ActivityDict(dict(tmp=df_acts))
        
        func()
    return 

@ActDictLoop("df_acts_sle, df_acts")
def act_difference(df_acts_sel, df_acts, st, et):
    """ Get outside activities with enveloping activities correctly clipped

    Parameters
    ----------
    df_acts_sel : pd.DataFrame or ActivityDict or List
        asdf
    df_acts : pd.DataFrame or ActivityDict or List
    st : str
    et : str

    Returns
    -------

    """
    df_acts_outside = df_difference(df_acts_sel, df_acts)\
                      .sort_values(by=START_TIME)\
                      .reset_index(drop=True)

    # ao contains both the cut up and the non-cut activities, adjust the start activity
    if not df_acts_outside.empty:
        df_acts_outside[ACTIVITY] = 'not selected'

        # Both the old time and the new start_time are in df_acts_outside
        # Get entry of outside corresponding to start_time
        act_st_split_et = df_acts_outside[df_acts_outside[START_TIME] == st]
        if not act_st_split_et.empty:
            idxs_acts_st_split = df_acts_outside[(df_acts_outside[END_TIME] == act_st_split_et.iat[0, 1])].index
            df_acts_outside.iat[idxs_acts_st_split[0], 1] = st - pd.Timedelta('1ms')
            df_acts_outside = df_acts_outside.drop(index=idxs_acts_st_split[1])

            df_acts_outside = df_acts_outside.reset_index(drop=True)


        act_st_split_st = df_acts_outside[df_acts_outside[END_TIME] == et]
        if not act_st_split_st.empty:
            idxs_acts_et_split = df_acts_outside[(df_acts_outside[START_TIME] == act_st_split_st.iat[0, 0])].index
            df_acts_outside.iat[idxs_acts_et_split[1], 0] = et - pd.Timedelta('1ms')
            df_acts_outside = df_acts_outside.drop(index=idxs_acts_et_split[0])

            df_acts_outside = df_acts_outside.reset_index(drop=True)



    return df_acts_outside


def _plot_selected_activity_marker(fig, df):
    """ Plot markers at the midpoint of selected activities
    """
    df = df[[START_TIME, END_TIME, ACTIVITY]].copy()
    cd = df.values
    diff = df[END_TIME] - df[START_TIME]
    df['mid_point'] = df[START_TIME] + diff/2
    y_label = 'Selected Activity mark'
    df['y'] = y_label

    marker = dict(size=5, symbol=5, line=dict(color='Red', width=1))
    hover_template = 'Activity: %{customdata[2]}<br>' + \
                     'Start_time: %{customdata[0]|' + STRFTIME_DATE + '}<br>' + \
                     'End_time: %{customdata[1]|' + STRFTIME_DATE + '}<br>' + \
                     '<extra></extra>'

    fig.add_trace(go.Scatter(
        mode='markers', y=df['y'], x=df['mid_point'],
        customdata=cd,
        marker=marker,
        hovertemplate=hover_template,
        showlegend=False))
    y_axis_order = [y_label] + fig.layout.yaxis.categoryarray.tolist()
    fig.update_yaxes(categoryarray=y_axis_order)

    return fig


def _plot_selected_device_marker(fig, df, df_devs, states=False):
    df = df[[TIME, DEVICE, VALUE]].copy()
    df_devs = df_devs[[TIME, DEVICE, VALUE]].copy()\
        .sort_values(by=TIME)\
        .reset_index(drop=True)

    y_label = 'Selected Device mark'
    df['y'] = y_label

    if states:
        # Set the categorical and boolean markers to midpoint of state
        dtypes = infer_dtypes(df)
        df[END_TIME] = df[TIME].copy()
        for dev in dtypes[BOOL] + dtypes[CAT]:
            df_tmp = df_devs[df_devs[DEVICE] == dev].copy()
            df_tmp[END_TIME] = df_tmp[TIME].shift(-1)
            mask = (dev == df[DEVICE])
            times = df.loc[mask, TIME]
            vals = df_tmp[df_tmp[TIME].isin(times)]
            df.at[mask, END_TIME] = vals

        df[START_TIME] = df[TIME]
        df[TIME] = df[TIME] + (df[END_TIME] - df[TIME])/2
        custom_data = df[[DEVICE, START_TIME, END_TIME]].values
        hover_template = 'Device: %{customdata[0]}<br>' + \
                         'Start_time: %{customdata[1]|' + STRFTIME_DATE + '}<br>' + \
                         'End_time: %{customdata[2]|' + STRFTIME_DATE + '}<br>' + \
                         '<extra></extra>'
    else:
        custom_data = df[DEVICE]
        hover_template = 'Device: %{customdata}<br>Time: %{x}<extra></extra>'
    marker = dict(size=5, symbol=5, line=dict(color='Red', width=1))
    fig.add_trace(go.Scatter(
        mode='markers', y=df['y'], x=df[TIME],
        customdata=custom_data,
        marker=marker,
        hovertemplate=hover_template,
        showlegend=False))
    y_axis_order = [y_label, *list(fig.layout.yaxis.categoryarray)]
    fig.update_yaxes(categoryarray=y_axis_order)
    return fig


def activities_and_devices(df_acts, df_devs, states=False, st=None, et=None,
                           act_order='alphabetical', dev_order='alphabetical',
                           df_acts_usel=None, df_devs_usel=None, devs_usel_state=None,
                           height=350
                           ):

    # Determines if device markers indicate the event or a states midpoint
    if states:
        devs_usel_state = states if devs_usel_state is None else devs_usel_state
    else:
        devs_usel_state = False
    assert isinstance(devs_usel_state, bool), 'devs_usel_state has to be set with either a boolean or None'

    # Copy data
    if isinstance(df_acts, pd.DataFrame): 
        df_acts = df_acts.copy().reset_index(drop=True)  # TODO
        df_acts = ActivityDict({'subject':df_acts})
    
    df_devs = df_devs.copy()

    # Determine the start and endpoint with regard to optional given parameters
    st, et, draw_start_line, draw_end_line = _determine_start_and_end(df_acts, df_devs, st, et)

    # Select the active displayed parts
    df_devs_sel, df_acts_sel = select_timespan(df_devs, df_acts, st, et, clip_activities=True)

    # Get the y-axis and label order
    act_order = activity_order_by(df_acts_sel.concat(), rule=act_order)
    dev_order = device_order_by(df_devs_sel, rule=dev_order)


    # determinte visual properties
    nr_devs = len(dev_order)
    marker_height = 3 if nr_devs > 15 else 5
    y_label_size = _dyn_y_label_size(height, nr_devs)

    # Reconstruct outside parts
    df_devs_outside = df_difference(df_devs_sel, df_devs)
    df_acts_outside = act_difference(df_acts_sel, df_acts, st, et)

    title = 'Activities and device events'
    fig = go.Figure()
    if states:
        fig = _plot_device_states_into_fig(fig, df_devs_sel, df_devs_usel,
                                           df_devs_outside, dev_order, st, et)
    else:
        fig = _plot_device_events_into_fig(fig, df_devs_sel, df_devs_usel, df_devs_outside, dev_order, marker_height)

    fig = _plot_activities_into_fig(fig, df_acts_sel, df_acts_usel, df_acts_outside, act_order)

    # Plot markers into trace
    if df_acts_usel is not None:
        fig = _plot_selected_activity_marker(fig, df_acts_usel)

    if df_devs_usel is not None:
        fig = _plot_selected_device_marker(fig, df_devs_usel, df_devs, devs_usel_state)



    if draw_start_line:
        fig.add_vline(x=st, line_width=1, line_color="Grey")
    if draw_end_line:
        fig.add_vline(x=et, line_width=1, line_color="Grey")

    _set_compact_title(fig, title)
    fig.update_yaxes(title=None, fixedrange=True, tickfont=dict(size=y_label_size),
                     ticklabeloverflow='allow'
                     )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=30, pad=0), height=height)

    return fig


def _endtime_to_offset(df_act, replace=True):
    """Compute the end_time as numerical offset in ms"""
    x_start = pd.to_datetime(df_act[START_TIME])
    x_end = pd.to_datetime(df_act[END_TIME])
    col_label = END_TIME if replace else 'offset'
    df_act[col_label] = (x_end - x_start).astype("timedelta64[ms]")
    return df_act


def _plot_activities_into_fig(fig, df_acts: pd.DataFrame, df_acts_usel: pd.DataFrame,
                              df_acts_outside: pd.DataFrame, act_order: list, y_label='Activity',
                              color_discrete_map=None) -> go.Figure:
    """ Manually plot timeline from plotly.express.make_figure
        fig = px.timeline(df_acts, x_start=START_TIME, x_end=END_TIME, y='y_label',
                              color=ACTIVITY)

    Parameters
    ----------
    fig : obj.Figure

    df_acts : pd.DataFrame

    mask_unselected : pd.Series
        A mask that indicates the datapoints whichs opacity should be lowered.
    """

    df_acts['y_label'] = y_label
    df_acts = df_acts[['y_label', START_TIME, END_TIME, ACTIVITY]]
    df_acts['dur'] = (df_acts[END_TIME] - df_acts[START_TIME]).astype(str)

    df_acts_outside['y_label'] = y_label
    df_acts_outside = df_acts_outside[['y_label', START_TIME, END_TIME, ACTIVITY]]
    df_acts_outside['dur'] = (df_acts_outside[END_TIME] - df_acts_outside[START_TIME]).astype(str)

    if df_acts_usel is not None:
        df_acts_usel['y_label'] = y_label
        df_acts_usel = df_acts_usel[['y_label', START_TIME, END_TIME, ACTIVITY]]
        df_acts_usel['dur'] = (df_acts_usel[END_TIME] - df_acts_usel[START_TIME]).astype(str)
        df_acts_usel = _endtime_to_offset(df_acts_usel)

    args = dict(data_frame=df_acts,
                x_start=START_TIME,
                x_end=END_TIME,
                y='y_label',
                color=ACTIVITY,
                color_discrete_map=color_discrete_map,
                category_orders={'activity': []},
                #categoryarray=category_orders,

                # Necessary to work
                template=None,
                color_discrete_sequence=None,
                hover_data=None,
    )

    trace_patch = dict(textposition="auto", orientation="h")
    layout_patch = dict(barmode="overlay")

    # Process args
    apply_default_cascade(args)
    args = process_dataframe_timeline(args)

    trace_specs, grouped_mappings, sizeref, _ = infer_config(
        args, go.Bar, trace_patch, layout_patch
    )

    grouper = [x.grouper or one_group for x in grouped_mappings] or [one_group]
    grouped = args["data_frame"].groupby(grouper, sort=False)

    # Grouped is already ordered TODO debug
    _, orders = get_groups_and_orders(args, grouper)
    #orders, sorted_group_names = get_orderings(args, grouper, grouped)

    # Assign colors to the groups
    for val in act_order:
        m = grouped_mappings[0]
        if val not in m.val_map:
            m.val_map[val] = m.sequence[len(m.val_map) % len(m.sequence)]


    trace_lst = []
    for group_name in act_order:
        df_sel_act = grouped.get_group(group_name)
        act_name = group_name

        # Create the trace
        trace = go.Bar(name=act_name)
        trace.update(legendgroup=act_name, showlegend=True,
                     alignmentgroup=True, offsetgroup=act_name)

        # Init subplot row/col
        trace._subplot_row = 1
        trace._subplot_col = 1

        m = grouped_mappings[0]
        trace_color = m.val_map[group_name]
        m.updater(trace, trace_color)
        hover_template = '<b>' + act_name + '</b><br>'\
                         + 'Start_time: %{base|' + STRFTIME_DATE + '}<br>' \
                         + 'End_time: %{x| ' + STRFTIME_DATE + '}' \
                         + '<br>Duration: %{customdata}<extra></extra>'
        trace.update(dict(textposition='auto', orientation='h',
                          base=df_sel_act[START_TIME],
                          x=df_sel_act[END_TIME],
                          y=df_sel_act['y_label'],
                          customdata=df_sel_act['dur'],
                          hovertemplate=hover_template
        ))

        trace_lst.append(trace)

        # Create user_selection for each trace
        if df_acts_usel is not None:
            # Get the indices in the trace where
            comp_df = df_sel_act.copy().merge(df_acts_usel, indicator=True, how='left')
            mark_selected = np.where((comp_df['_merge'] == 'both').values)[0]
            unselected = {'marker': {'opacity': 0.3, 'color': trace_color}}
            selected = {'marker': {'opacity': 1.0, 'color': trace_color}}
            trace.update(selectedpoints=mark_selected, selected=selected, unselected=unselected)

    if not df_acts_outside.empty:
        # Convert to bar
        act_name = 'not selected'
        df_sel_act = _endtime_to_offset(df_acts_outside)

        # Create the trace
        trace = go.Bar(name=act_name,
                       base=df_sel_act[START_TIME],
                       hoverinfo='skip',
                       marker=dict(color='rgba(58, 71, 80, 0.6)', opacity=0.2),
                       x=df_sel_act[END_TIME],
                       y=df_sel_act['y_label'],
                       customdata=df_sel_act['dur'],
                       textposition='auto',
                       orientation='h',
                       legendgroup=act_name,
                       showlegend=False,
                       alignmentgroup=True,
                       offsetgroup=act_name,
        )
        trace._subplot_row = 1
        trace._subplot_col = 1
        trace_lst.append(trace)

    fig = make_subplots(
        rows=1,
        cols=1,
        shared_xaxes='all',
        shared_yaxes='all',
        start_cell="bottom-left",
        horizontal_spacing=0.02,
        vertical_spacing=0.03,
        subplot_titles=[],
        column_widths=[1.0],
        row_heights=[1.0],
        specs=[[{'type': 'xy'}]],
        figure=fig)


    # Position traces in subplots
    for trace in trace_lst:
        trace.update({'xaxis': 'x', 'yaxis': 'y'})

    # Add traces, layout and frames to figure
    fig.add_traces(trace_lst)
    fig.update_layout({'barmode': 'overlay',
                       'legend': {'tracegroupgap': 0,
                                  'title_text': ACTIVITY}
                       })
    configure_axes(args, go.Bar, fig, orders)

    return fig


def contingency_events(df_acts=None, df_devs=None, con_tab=None, scale='linear', height=350,
                       act_order='alphabetical', dev_order='alphabetical', distributed=False
                       ) -> plotly.graph_objects.Figure:
    """
    """
    title = 'Activities vs device events'
    cbarlabel = 'count' if scale == 'linear' else 'log count'

    # get the list of cross tabulations per t_window
    if con_tab is not None:
        df_con = con_tab.copy()    # :pd.DataFrame
    else:
        df_con = contingency_table_events(df_devs, df_acts)

    df_con = df_con.set_index('device')

    act_order = activity_order_by(df_acts, rule=act_order)
    dev_order = device_order_by(df_devs, rule=dev_order)
    df_con = df_con[np.flip(act_order)]     # change order of rows
    df_con = df_con.reindex(dev_order)      # change order of columns

    # Extract values
    devs = df_con.index.values
    acts = df_con.columns.values
    vals = df_con.values
    z = vals if scale == 'linear' else np.log(vals)

    fig = go.Figure(data=go.Heatmap(
        z=z.T,
        x=devs,
        y=acts,
        customdata=vals.T,
        hovertemplate='"%{x}" during "%{y}" %{customdata} times<extra></extra>',
        colorscale='Viridis',
        hoverongaps=False))

    _set_compact_title(fig, title)

    fig.update_xaxes(tickangle=45)
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=30, pad=0), height=height)
    _style_colorbar(fig, cbarlabel)

    return fig


def contingency_states(df_acts=None, df_devs=None, con_tab=None, scale='linear', height=350,
                       act_order='alphabetical', dev_order='alphabetical', distributed=False
                       ) -> plotly.graph_objects.Figure:
    """
    """
    title = 'Activities vs device states'
    cbarlabel = 'seconds' if scale == 'linear' else 'log seconds'

    # get the list of cross tabulations per t_window
    if con_tab is not None:
        df_con = con_tab.copy()    # :pd.DataFrame
    else:
        df_con = contingency_table_states(df_devs, df_acts, distributed=distributed)

    # Determine device and activity labels order
    act_order = activity_order_by(df_acts, rule=act_order)
    df_con = df_con[np.flip(act_order)]     # change order of rows
    devs = df_con.index.values

    # Reorder and format devices
    dtypes = infer_dtypes(df_devs)
    dtypes.pop(NUM, None)
    new_devs, new_order = format_device_labels(devs, dtypes, boolean_state=True, categorical_state=True)
    devs = list(new_devs)
    vals = df_con.copy()\
        .reset_index()\
        .reindex(new_order)\
        .set_index(DEVICE)

    # Extract values
    acts = df_con.columns.values


    # Convert timedelta to nanoseconds
    z = vals.astype('timedelta64[ns]')/np.timedelta64(1, 'ns')
    z = z if scale == 'linear' else np.log(z)
    z = z.T

    # Create hoverdata, the duration as strings in (D,A,0) and full X names in (D,A,1)
    vals = vals.astype(str)
    tmp = np.tile(vals.index, (len(vals.columns), 1))
    cd = np.array([tmp, vals.values.T])
    cd = np.moveaxis(cd, 0, -1)


    # TODO hack, add whitespaces to similar categories to make them unique
    #      strings since otherwise plotly merges them into one category
    j = 0
    for i in range(len(devs)):
        if devs[i] == 'on':
            devs[i] = devs[i] + ' '*j
            j += 1

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=devs,
        y=acts,
        customdata=cd,
        hovertemplate='"%{customdata[0]}" during "%{y}" for %{customdata[1]}<extra></extra>',
        colorscale='Viridis',
        hoverongaps=False))

    _set_compact_title(fig, title)

    fig.update_xaxes(tickangle=45)
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=30, pad=0), height=height)
    _style_colorbar(fig, cbarlabel)

    return fig
