import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .private_func import _get_report


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

    report = get_report(indicator, ret)
    report_all = report.loc['All', :]

    fig = plt.figure(figsize=(20, 12))

    ax1 = plt.subplot2grid((3, 1), (0, 0), rowspan=2)
    ax2 = plt.subplot2grid((3, 1), (2, 0))

    pnl = delta*ret
    day_ret = (ret*100).groupby(by=ret.index.to_series().apply(lambda x: x.date())).sum()
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


