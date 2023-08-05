import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .private_func import _get_report, _get_report_composite
import seaborn as sns


def get_report(delta, ret):
    """
    delta: pd.Series with DatatimeIndex
    ret: pd.Series with DatatimeIndex
    report: pd.DataFrame
    """
    if not (isinstance(delta, pd.Series)) or not (isinstance(ret, pd.Series)):
        print('indicator and pnl must be pd.Series')
        return

    if not (isinstance(delta.index, pd.core.indexes.datetimes.DatetimeIndex)) \
            or not (isinstance(ret.index, pd.core.indexes.datetimes.DatetimeIndex)):
        print('index of indicator and pnl must be pd.core.indexes.datetimes.DatetimeIndex')
        return

    if len(delta) < len(ret):
        ret = ret.copy().reindex(delta.index)
        indicator = delta.copy()
    else:
        indicator = delta.copy().reindex(ret.index)
        ret = ret.copy()

    valid_ind = np.isfinite(indicator)
    indicator = indicator[valid_ind]
    ret = ret[valid_ind]

    report_all = _get_report(indicator, ret).rename('All').to_frame().T
    report_sub = indicator.groupby(by=indicator.index.to_series().apply(lambda x: x.year)) \
        .apply(lambda x: _get_report(x, ret.reindex(x.index))).unstack()

    return pd.concat([report_all, report_sub])


def get_composite_report(delta, ret):
    """
    delta: pd.DataFrame with DatatimeIndex
    ret: pd.DataFrame with DatatimeIndex
    report: pd.DataFrame
    """
    if not (isinstance(delta, pd.DataFrame)) or not (isinstance(ret, pd.DataFrame)):
        print('indicator and pnl must be pd.Series')
        return

    if not (isinstance(delta.index, pd.core.indexes.datetimes.DatetimeIndex)) \
            or not (isinstance(ret.index, pd.core.indexes.datetimes.DatetimeIndex)):
        print('index of indicator and pnl must be pd.core.indexes.datetimes.DatetimeIndex')
        return

    if len(delta) < len(ret):
        ret = ret.copy().reindex(delta.index)
        indicator = delta.copy()
    else:
        indicator = delta.copy().reindex(ret.index)
        ret = ret.copy()

    inf_ind = np.isinf(indicator)
    indicator[inf_ind] = np.nan
    indicator.dropna(inplace=True)
    ret = ret.reindex(indicator.index)

    report_all = _get_report_composite(indicator, ret).rename('All').to_frame().T
    report_sub = indicator.groupby(by=indicator.index.to_series().apply(lambda x: x.year)) \
        .apply(lambda x: _get_report_composite(x, ret.reindex(x.index))).unstack()

    return pd.concat([report_all, report_sub])


def get_pnl_plot(delta, ret, return_plot=False):
    """
    delta: pd.Series with DatatimeIndex
    ret: pd.Series with DatatimeIndex
    """
    if not (isinstance(delta, pd.Series)) or not (isinstance(ret, pd.Series)):
        print('indicator and pnl must be pd.Series')
        return

    if not (isinstance(delta.index, pd.core.indexes.datetimes.DatetimeIndex)) \
            or not (isinstance(ret.index, pd.core.indexes.datetimes.DatetimeIndex)):
        print('index of indicator and pnl must be pd.core.indexes.datetimes.DatetimeIndex')
        return

    if len(delta) < len(ret):
        ret = ret.copy().reindex(delta.index)
        indicator = delta.copy()
    else:
        indicator = delta.copy().reindex(ret.index)
        ret = ret.copy()

    valid_ind = np.isfinite(indicator)
    indicator = indicator[valid_ind]
    ret = ret[valid_ind]

    report_all = _get_report(indicator, ret)

    fig = plt.figure(figsize=(20, 12))

    ax1 = plt.subplot2grid((3, 1), (0, 0), rowspan=2)
    ax2 = plt.subplot2grid((3, 1), (2, 0))

    pnl = indicator * ret
    day_ret = (ret * 100).groupby(by=ret.index.to_series().apply(lambda x: x.date())).sum()
    day_pnl = pnl.groupby(by=pnl.index.to_series().apply(lambda x: x.date())).sum()
    DD_ss = day_pnl.cumsum() - day_pnl.cumsum().expanding(0).max()

    day_pnl.cumsum().plot(ax=ax1, label='Strategy')
    (day_pnl.cumsum() - day_ret.cumsum()).plot(ax=ax1, label='Alpha')
    day_ret.cumsum().plot(ax=ax1, ls=':', c='k', alpha=0.5, label='Asset')

    ax1.set_title('PnL={} PoT={} Sharpe={} WR={:.2f} Worst={:.2f}'.format(
        report_all.loc['PnL'], report_all.loc['PoT'], report_all.loc['Sharpe'], report_all.loc['WR'],
        report_all.loc['Worst']
    ))
    ax1.set_ylabel('PnL')
    ax1.legend(loc=2)
    ax1.set_xlabel('')
    ax1.grid()

    DD_ss.plot(ax=ax2, c='r')
    ax2.set_title('MDD={} MDDD={}'.format(
        report_all.loc['MDD'], report_all.loc['MDDD']
    ))
    ax2.set_ylabel('Drawdown')
    ax2.set_xlabel('Data')
    ax2.grid()

    plt.show()
    if return_plot:
        return fig

    return


def get_composite_pnl_plot(delta, ret, return_plot=False):
    """
    Multi-Assets PnL
    delta: pd.DataFrame with DatatimeIndex
    ret: pd.DataFrame with DatatimeIndex
    """
    if not (isinstance(delta, pd.DataFrame)) or not (isinstance(ret, pd.DataFrame)):
        print('indicator and pnl must be pd.DataFrame')
        return

    if not (isinstance(delta.index, pd.core.indexes.datetimes.DatetimeIndex)) \
            or not (isinstance(ret.index, pd.core.indexes.datetimes.DatetimeIndex)):
        print('index of indicator and pnl must be pd.core.indexes.datetimes.DatetimeIndex')
        return

    if len(delta) < len(ret):
        ret = ret.copy().reindex(delta.index)
        indicator = delta.copy()
    else:
        indicator = delta.copy().reindex(ret.index)
        ret = ret.copy()

    inf_ind = np.isinf(indicator)
    indicator[inf_ind] = np.nan
    indicator.dropna(inplace=True)
    ret = ret.reindex(indicator.index)

    indicator_og = pd.DataFrame(100.0 / len(indicator.columns), index=indicator.index, columns=indicator.columns)

    # plot
    fig = plt.figure(figsize=(20, 12))

    ax1 = plt.subplot2grid((3, 1), (0, 0), rowspan=2)
    ax2 = plt.subplot2grid((3, 1), (2, 0))

    #
    pnl = (indicator * ret).sum(axis=1)
    day_ret = (indicator_og * ret).sum(axis=1).groupby(by=ret.index.to_series().apply(lambda x: x.date())).sum()
    day_pnl = pnl.groupby(by=pnl.index.to_series().apply(lambda x: x.date())).sum()
    DD_ss = day_pnl.cumsum() - day_pnl.cumsum().expanding(0).max()

    day_pnl.cumsum().plot(ax=ax1, label='Strategy')
    (day_pnl.cumsum() - day_ret.cumsum()).plot(ax=ax1, ls='--', label='Alpha')
    day_ret.cumsum().plot(ax=ax1, ls=':', c='k', alpha=0.5, label='Asset')

    report_all = _get_report_composite(indicator, ret)

    ax1.set_title('PnL={} PoT={} Sharpe={} WR={:.2f} Worst={:.2f}'.format(
        report_all.loc['PnL'], report_all.loc['PoT'], report_all.loc['Sharpe'], report_all.loc['WR'],
        report_all.loc['Worst']
    ))
    ax1.set_ylabel('PnL')
    ax1.legend(loc=2)
    ax1.set_xlabel('')
    ax1.grid()

    DD_ss.plot(ax=ax2, c='r')
    ax2.set_title('MDD={} MDDD={}'.format(
        report_all.loc['MDD'], report_all.loc['MDDD']
    ))
    ax2.set_ylabel('Drawdown')
    ax2.set_xlabel('Data')
    ax2.grid()

    plt.show()
    if return_plot:
        return fig

    return


def round_test(delta, close, adj_close, BPV, mult=1e4, fee_rate=3e-4, vol_limit=1):
    if not isinstance(delta, pd.DataFrame):
        print('delta must be pd.DataFrame')
        return

    if not isinstance(close, pd.DataFrame):
        print('close must be pd.DataFrame')
        return

    if not isinstance(adj_close, pd.DataFrame):
        print('adj_close must be pd.DataFrame')
        return

    if not isinstance(BPV, pd.DataFrame):
        print('BPV must be pd.DataFrame')
        return

    if not isinstance(vol_limit, int):
        print('vol_limit must be int')
        return

    if not all([set(delta.columns) == set(close.columns),
                set(adj_close.columns) == set(close.columns),
                set(BPV.columns) == set(close.columns)]):
        print(F'mismatched columns: delta{delta.columns}, close{close.columns}, \
              adj_close{adj_close.columns}, BPV{BPV.columns}')
        return

    if not all([len(delta) == len(close), len(close) == len(adj_close), len(adj_close) == len(BPV)]):
        print(F'mismatched length: delta{len(delta)}, close{len(close)}, \
              adj_close{len(adj_close)}, BPV{len(BPV)}')
        return

    # vol without round
    og_vol = ((delta*mult)/(BPV*close)).fillna(0)

    # rounded vol
    vol = og_vol.round(0)

    # vol_limit
    new_vol = og_vol.applymap(lambda x: np.sign(x) if x >= vol_limit or x <= -vol_limit else 0)

    #
    ret = adj_close.pct_change().shift(-1).fillna(0)

    #
    og_pnl = delta * mult * ret
    og_day_pnl = og_pnl.groupby(by=og_pnl.index.to_series().apply(lambda x: x.date())).sum().sum(axis=1)
    og_sum_pnl = og_pnl.cumsum().dropna().sum(axis=1)

    pnl = vol * BPV * close * ret
    day_pnl = pnl.groupby(by=og_pnl.index.to_series().apply(lambda x: x.date())).sum().sum(axis=1)
    sum_pnl = pnl.cumsum().dropna().sum(axis=1)

    # after cost
    sum_pnl_ac = (pnl - (vol.diff() * BPV * close).abs() * fee_rate).cumsum().sum(axis=1)
    day_pnl_ac = (pnl - (vol.diff() * BPV * close).abs() * fee_rate) \
        .groupby(by=og_pnl.index.to_series().apply(lambda x: x.date())).sum().sum(axis=1)

    new_pnl = new_vol * BPV * close * ret
    new_sum_pnl = new_pnl.dropna().cumsum().sum(axis=1)
    new_day_pnl = new_pnl.groupby(by=og_pnl.index.to_series().apply(lambda x: x.date())).sum().sum(axis=1)

    #
    og_pot = (og_pnl.sum().sum() / (og_vol.diff() * BPV * close).abs().sum().sum()) * 1e4
    pot = (pnl.sum().sum() / (vol.diff() * BPV * close).abs().sum().sum()) * 1e4
    new_pot = (new_pnl.sum().sum() / (new_vol.diff() * BPV * close).abs().sum().sum()) * 1e4

    def _sharpe(m):
        return m.mean()/m.std() * 16.0

    data_pnl = pd.concat([
        og_sum_pnl.rename('Orginal Delta: sharpe={:.2f} PoT={:.2f}'. \
                          format(_sharpe(og_day_pnl), og_pot)),
        sum_pnl.rename('Round Volume: sharpe={:.2f} PoT={:.2f}'. \
                       format(_sharpe(day_pnl), pot)),
        new_sum_pnl.rename('1 Volume Limit: sharpe={:.2f} PoT={:.2f}'. \
                           format(_sharpe(new_day_pnl), new_pot)),
        sum_pnl_ac.rename('Round Volume after-cost: sharpe={:.2f}'. \
                          format(_sharpe(day_pnl_ac)))], axis=1)/mult

    # plot
    plt.figure(figsize=(20, 16))

    ax1 = plt.subplot2grid((4, 1), (0, 0), rowspan=2)
    ax2 = plt.subplot2grid((4, 1), (2, 0))
    ax3 = plt.subplot2grid((4, 1), (3, 0))

    sns.lineplot(data=data_pnl, ax=ax1)
    ax1.set_title('Round-Test: mult={}k vol_limit={}'.format(int(mult / 1e3), int(vol_limit)))
    ax1.set_xlabel('')
    ax1.set_ylabel('PnL')

    sns.lineplot(data=vol, ax=ax2)
    ax2.set_xlabel('')
    ax2.set_ylabel('Volume')

    sns.lineplot(data=new_vol.dropna().astype(int), ax=ax3)
    ax3.set_xlabel('Date')
    ax3.set_ylabel('Long or Short')
    ax3.set_yticks([-1, 0, 1])

    plt.show()

    return






