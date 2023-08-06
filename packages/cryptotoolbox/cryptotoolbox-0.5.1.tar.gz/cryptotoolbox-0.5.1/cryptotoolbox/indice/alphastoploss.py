#!/usr/bin/env python
# coding: utf-8

import requests
from datetime import datetime
import pandas as pd
from cryptotoolbox.indice import alpha
import numpy as np
from cryptotoolbox.connector import crypto_connector
from cryptotoolbox.realtime import realtime_plotting_utility
import quandl

import talib
from cryptotoolbox.risk_metrics import riskmetrics


def strat_weekly(y, btc='BTC', tone=14,ttwo=23,p1=1.01, p2=1.05, long_expo=1., short_expo=0., rebalancing_day=5):  # On rentre le dataframe
    weekday = y.weekday.values
    cours = y[btc].values
    T = np.size(weekday)
    S = np.zeros(T)
    for t in range(ttwo, T):
        if weekday[t] == rebalancing_day and cours[t - ttwo] > 0:
            if cours[t] > cours[t - tone] * p1 and cours[t] > cours[t - ttwo] * p2:
                S[t] = long_expo
            else:
                S[t] = short_expo
        else:
            S[t] = S[t - 1]
    return S

def strat_daily_ETH(y, eth='ETH', long_expo = 1., short_expo = 0., rebalancing_day=5):  # On rentre le dataframe
    weekday = y.weekday.values
    cours = y[eth].values
    T = np.size(weekday)
    S = np.zeros(T)
    for t in range(30, T):
        if weekday[t] == rebalancing_day and cours[t - 22] > 0:
            if cours[t] > cours[t - 14] * 1.05 or cours[t] > cours[t - 21] * 1.1:
                S[t] = long_expo
            else:
                S[t] = short_expo
        else:
            S[t] = S[t - 1]
    return S


#def strat_daily_BTC(y, btc='BTC', p1=1.1, p2=1.2, long_expo = 1., short_expo = 0.):  # On rentre le dataframe
def strat_daily_BTC(y, btc='BTC', p1=1.05, p2=1.1, long_expo=1., short_expo=0., rebalancing_day=5):  # On rentre le dataframe
    weekday = y.weekday.values
    cours = y[btc].values
    T = np.size(weekday)
    S = np.zeros(T)
    for t in range(22, T):
        if weekday[t] == rebalancing_day and cours[t - 22] > 0:
            if cours[t] > cours[t - 14] * p1 and cours[t] > cours[t - 21] * p2:
                S[t] = long_expo
            else:
                S[t] = short_expo
        else:
            S[t] = S[t - 1]
    return S

#def strat_daily_BTC(y, btc='BTC', p1=1.1, p2=1.2, long_expo = 1., short_expo = 0.):  # On rentre le dataframe
def strat_daily(y, btc='BTC',tone=15,ttwo=26, p1=1., p2=1.05, long_expo=1., short_expo=0., ):  # On rentre le dataframe
    cours = y[btc].values
    T = np.size(cours)
    S = np.zeros(T)
    for t in range(22, T):
        if cours[t] > cours[t - tone] * p1 and cours[t] > cours[t - ttwo] * p2:
            S[t] = long_expo
        else:
            S[t] = short_expo
    return S

def combine_lo_sigs(lo_df = None, rsilo_df = None, core_tokens=None, extra_tokens=None):
    daily_rsi_lo_df = riskmetrics.filter_daily(rsilo_df.copy())
    lo_close_colums = [f'close_{tok}' for tok in core_tokens + extra_tokens]
    rsilo_close_colums = [f'close_{tok}' for tok in core_tokens]
    lo_raw_sigs_colums = [f'SRAWLO{tok}' for tok in core_tokens + extra_tokens]
    rsilo_raw_sigs_columns = [f'SRSILO{tok}' for tok in core_tokens]
#    merged_sig_df = pd.merge(lo_df[lo_close_colums+lo_raw_sigs_colums].copy(), daily_rsi_lo_df[rsilo_close_colums+rsilo_raw_sigs_columns].copy(), right_index=True, left_index=True)
    merged_sig_df = pd.merge(lo_df[lo_close_colums + lo_raw_sigs_colums].copy(),daily_rsi_lo_df[rsilo_raw_sigs_columns].copy(), right_index=True,left_index=True)
    return merged_sig_df

def compute_alpha_signal_rsilo_weekly_multicoin_continuous(df=None, core_tokens=['BTC', 'ETH'], extra_tokens =[], rsi_lookback = 8 ,threshold = 60 , rebalancing_day=6,lo_sig_suffix='RSILO', compute_lo_strat=True, plot_html=False, local_root_directory='None'):
    all_tokens = core_tokens + extra_tokens

    for current_token in all_tokens:
        df['hour'] = df.index.hour
        all_dfs = None
        for me_hour in range(0,24):
            daily_df = df[df['hour'] == me_hour].copy()
            daily_df[f'DAILY_RSI_{current_token}_{me_hour}'] = talib.RSI(daily_df[f'close_{current_token}'], rsi_lookback)
            if all_dfs is None:
                all_dfs = daily_df.copy()
            else:
                all_dfs = pd.concat([all_dfs.copy(), daily_df.copy()])

        all_dfs = all_dfs.sort_index()
        column_list_asset = []

        for me_hour in range(0,24):
            all_dfs[f'DAILY_RSI_{current_token}_{me_hour}'] = all_dfs[f'DAILY_RSI_{current_token}_{me_hour}'].fillna(0.)
            column_list_asset.append(f'DAILY_RSI_{current_token}_{me_hour}')

        all_dfs[f'DAILY_RSI_{current_token}'] = all_dfs[column_list_asset].sum(axis=1)
        df = pd.merge(df.copy(),  all_dfs[[f'DAILY_RSI_{current_token}']].copy() , how='left', left_index=True, right_index=True)

    def compute_dual_RSI_muticoin_continuous(row_df, threshold=60, all_tokens=[],lo_sig_suffix='RSILO'):
        RSI_VALUES = [row_df[f'DAILY_RSI_{cur_tok}'] for cur_tok in all_tokens]
        RSI_nd = np.array(RSI_VALUES)
        RSI_weights = RSI_nd/RSI_nd.sum()
        RSI_th = RSI_nd > threshold
        all_above = RSI_th.sum()

        if all_above >0:
            signals={}
            counter = 0
            for me_tok in all_tokens:
                signals[f'S{lo_sig_suffix}{me_tok}'] = RSI_weights[counter]
                counter=counter+1
            return signals
        else:
            signals={}
            counter = 0
            for me_tok in all_tokens:
                signals[f'S{lo_sig_suffix}{me_tok}'] = 0
                counter=counter+1
            return signals


    # def compute_dual_RSI(row_df, threshold=60, first_token='BTC', second_token='ETH',lo_sig_suffix='RSILO'):
    #     RSI_BTC = row_df[f'DAILY_RSI_{first_token}']
    #     RSI_ETH = row_df[f'DAILY_RSI_{second_token}']
    #     if RSI_BTC > threshold or RSI_ETH > threshold:
    #         if RSI_BTC > RSI_ETH:
    #             return {
    #                 f'S{lo_sig_suffix}{first_token}': 1,
    #                 f'S{lo_sig_suffix}{second_token}': 0
    #             }
    #         else:
    #             return {
    #                 f'S{lo_sig_suffix}{first_token}': 0,
    #                 f'S{lo_sig_suffix}{second_token}': 1
    #             }
    #     else:
    #         return {
    #             f'S{lo_sig_suffix}{first_token}': 0,
    #             f'S{lo_sig_suffix}{second_token}': 0
    #         }

    go_rsi = lambda x: compute_dual_RSI_muticoin_continuous(x, threshold=threshold, all_tokens=all_tokens, lo_sig_suffix=lo_sig_suffix)
    sig_df= df.apply(go_rsi, axis=1)
    sig_df = sig_df.to_frame()
    sig_df.columns = ['signal_gen']
    sig_df['signal'] = sig_df['signal_gen'].shift()
    sig_df.index = all_dfs.index
    sig_df = sig_df.iloc[1:]
    old_index = sig_df.index
    sig_df = pd.DataFrame().from_records(sig_df['signal'].values)
    sig_df.index = old_index

    for current_token in all_tokens:
        df[f'return_{current_token}'] = df[f'close_{current_token}'].pct_change()

    data_df = pd.merge(df.copy(), sig_df.copy(), how='left', left_index=True, right_index=True)

    ### we rebalance monday morning
    def get_filter_date(row,rebalancing_day=6):
        ##### to get the proper daily close
        #### we only keep the signal that has been emitted the day after
        next_day = (rebalancing_day+1)%7
        if row['weekday'] == next_day and row['hour'] == 0:
            return True
        else:
            return False

    data_df['weekday'] = data_df.index.weekday
    data_df['hour'] = data_df.index.hour
    go_reb = lambda x : get_filter_date(x, rebalancing_day=rebalancing_day)
    data_df['rebalancing'] = data_df.apply(go_reb, axis=1)
    ##### we rebalance with the close of rebalancing_day :
    def rebalancing_signal_cut(row, token='BTC', lo_sig_suffix='RSILO'):
        if row['rebalancing']:
            return row[f'S{lo_sig_suffix}{token}']
        else:
            return np.nan
    for current_token in all_tokens:
        gotok = lambda x: rebalancing_signal_cut(x, token=current_token,lo_sig_suffix=lo_sig_suffix)
        data_df[f'S{lo_sig_suffix}{current_token}'] = data_df.apply(gotok, axis=1)
        data_df[f'S{lo_sig_suffix}{current_token}'] = data_df[f'S{lo_sig_suffix}{current_token}'].ffill()

    moderation = 1.
    mod_data_df = data_df.copy()

    def compute_dual_return(row, moderation=1.,all_tokens=[], lo_sig_suffix='RSILO'):
        global_ret = 0.
        for current_token in all_tokens:
            global_ret = global_ret + row[f'S{lo_sig_suffix}{current_token}'] * row[f'return_{current_token}'] * moderation
        return global_ret

    go_compute = lambda x: compute_dual_return(x, moderation=moderation, all_tokens=all_tokens,lo_sig_suffix=lo_sig_suffix)
    mod_data_df['strat_return'] = mod_data_df.apply(go_compute, axis=1)

    mod_data_df['strat_return'] = mod_data_df['strat_return'].fillna(0.)
    me_strat = 'strat'
    mod_data_df[me_strat] = np.cumprod(1 + mod_data_df['strat_return'].values)

    if plot_html:
        fig = realtime_plotting_utility.plot_multiple_time_series(
            data_df=mod_data_df[[me_strat]],
            logy=True, split=False,
            put_on_same_scale=False,
            title=f'Perf{str(all_tokens)}')
        fig.show()
        fig = realtime_plotting_utility.plot_multiple_time_series(
            data_df=mod_data_df[[me_strat]],
            logy=False, split=False,
            put_on_same_scale=False,
            title=f'Perf{str(all_tokens)}')
        fig.show()

    title = f'WEEKLY_MULTICOIN_RSI_{moderation}'
    backtest_df = mod_data_df[[me_strat]].copy()
    backtest_df.columns = ['strat']
    strat_data_df = backtest_df[['strat']].copy()

    daily_df = riskmetrics.filter_daily(strat_data_df)
    daily_df = daily_df.dropna()

    if compute_lo_strat:
        title = 'multicoin_weekly_continuous_rsilo'
        backtest_df = daily_df[['strat']].copy()
        whole_kpis = True
        if whole_kpis:
            strat_data_df = backtest_df[['strat']].copy()
            from cryptotoolbox.analyzer import market

            # strat_data_df = strat_data_df[strat_data_df.index >= '2021-02-01'].copy()
            ma = market.MarketAnalyzer(strat_data_df, hourlyze=True)

            print('computing kpis')
            kpi_df = ma.get_kpi().T
            kpi_df = kpi_df.dropna()
            kpi_df = kpi_df[~np.isnan(kpi_df.sharpe)]
            print(kpi_df.head())

        backtest_df.columns = ['strat']
        riskmetrics.compute_plot_excel_kpis_meterics_metrics(backtest_df, title,
                                                             local_root_directory,
                                                             plot_html=True,
                                                             write_file=True)
    return mod_data_df.copy()


def compute_alpha_signal_rsilo_daily_multicoin_continuous(df=None, core_tokens=['BTC', 'ETH'], extra_tokens =[], rsi_lookback = 8 ,threshold = 60 , rebalancing_day=6,lo_sig_suffix='RSILO', compute_lo_strat=True, plot_html=False, local_root_directory='None'):
    all_tokens = core_tokens + extra_tokens

    for current_token in all_tokens:
        df['hour'] = df.index.hour
        all_dfs = None
        for me_hour in range(0,24):
            daily_df = df[df['hour'] == me_hour].copy()
            daily_df[f'DAILY_RSI_{current_token}_{me_hour}'] = talib.RSI(daily_df[f'close_{current_token}'], rsi_lookback)
            if all_dfs is None:
                all_dfs = daily_df.copy()
            else:
                all_dfs = pd.concat([all_dfs.copy(), daily_df.copy()])

        all_dfs = all_dfs.sort_index()
        column_list_asset = []

        for me_hour in range(0,24):
            all_dfs[f'DAILY_RSI_{current_token}_{me_hour}'] = all_dfs[f'DAILY_RSI_{current_token}_{me_hour}'].fillna(0.)
            column_list_asset.append(f'DAILY_RSI_{current_token}_{me_hour}')

        all_dfs[f'DAILY_RSI_{current_token}'] = all_dfs[column_list_asset].sum(axis=1)
        df = pd.merge(df.copy(),  all_dfs[[f'DAILY_RSI_{current_token}']].copy() , how='left', left_index=True, right_index=True)

    def compute_dual_RSI_muticoin_continuous(row_df, threshold=60, all_tokens=[],lo_sig_suffix='RSILO'):
        RSI_VALUES = [row_df[f'DAILY_RSI_{cur_tok}'] for cur_tok in all_tokens]
        RSI_nd = np.array(RSI_VALUES)
        RSI_weights = RSI_nd/RSI_nd.sum()
        RSI_th = RSI_nd > threshold
        all_above = RSI_th.sum()

        if all_above >0:
            signals={}
            counter = 0
            for me_tok in all_tokens:
                signals[f'S{lo_sig_suffix}{me_tok}'] = RSI_weights[counter]
                counter=counter+1
            return signals
        else:
            signals={}
            counter = 0
            for me_tok in all_tokens:
                signals[f'S{lo_sig_suffix}{me_tok}'] = 0
                counter=counter+1
            return signals


    # def compute_dual_RSI(row_df, threshold=60, first_token='BTC', second_token='ETH',lo_sig_suffix='RSILO'):
    #     RSI_BTC = row_df[f'DAILY_RSI_{first_token}']
    #     RSI_ETH = row_df[f'DAILY_RSI_{second_token}']
    #     if RSI_BTC > threshold or RSI_ETH > threshold:
    #         if RSI_BTC > RSI_ETH:
    #             return {
    #                 f'S{lo_sig_suffix}{first_token}': 1,
    #                 f'S{lo_sig_suffix}{second_token}': 0
    #             }
    #         else:
    #             return {
    #                 f'S{lo_sig_suffix}{first_token}': 0,
    #                 f'S{lo_sig_suffix}{second_token}': 1
    #             }
    #     else:
    #         return {
    #             f'S{lo_sig_suffix}{first_token}': 0,
    #             f'S{lo_sig_suffix}{second_token}': 0
    #         }

    go_rsi = lambda x: compute_dual_RSI_muticoin_continuous(x, threshold=threshold, all_tokens=all_tokens, lo_sig_suffix=lo_sig_suffix)
    sig_df= df.apply(go_rsi, axis=1)
    sig_df = sig_df.to_frame()
    sig_df.columns = ['signal_gen']
    sig_df['signal'] = sig_df['signal_gen'].shift()
    sig_df.index = all_dfs.index
    sig_df = sig_df.iloc[1:]
    old_index = sig_df.index
    sig_df = pd.DataFrame().from_records(sig_df['signal'].values)
    sig_df.index = old_index

    for current_token in all_tokens:
        df[f'return_{current_token}'] = df[f'close_{current_token}'].pct_change()

    data_df = pd.merge(df.copy(), sig_df.copy(), how='left', left_index=True, right_index=True)

    ### we rebalance monday morning
    def get_day_filter_date(row,rebalancing_day=6):
        if row['hour'] == 0:
            return True
        else:
            return False

    data_df['weekday'] = data_df.index.weekday
    data_df['hour'] = data_df.index.hour
    go_reb = lambda x : get_day_filter_date(x, rebalancing_day=rebalancing_day)
    data_df['rebalancing'] = data_df.apply(go_reb, axis=1)
    ##### we rebalance with the close of rebalancing_day :
    def rebalancing_signal_cut(row, token='BTC', lo_sig_suffix='RSILO'):
        if row['rebalancing']:
            return row[f'S{lo_sig_suffix}{token}']
        else:
            return np.nan
    for current_token in all_tokens:
        gotok = lambda x: rebalancing_signal_cut(x, token=current_token,lo_sig_suffix=lo_sig_suffix)
        data_df[f'S{lo_sig_suffix}{current_token}'] = data_df.apply(gotok, axis=1)
        data_df[f'S{lo_sig_suffix}{current_token}'] = data_df[f'S{lo_sig_suffix}{current_token}'].ffill()

    moderation = 1.
    mod_data_df = data_df.copy()

    def compute_dual_return(row, moderation=1.,all_tokens=[], lo_sig_suffix='RSILO'):
        global_ret = 0.
        for current_token in all_tokens:
            global_ret = global_ret + row[f'S{lo_sig_suffix}{current_token}'] * row[f'return_{current_token}'] * moderation
        return global_ret

    go_compute = lambda x: compute_dual_return(x, moderation=moderation, all_tokens=all_tokens,lo_sig_suffix=lo_sig_suffix)
    mod_data_df['strat_return'] = mod_data_df.apply(go_compute, axis=1)

    mod_data_df['strat_return'] = mod_data_df['strat_return'].fillna(0.)
    me_strat = 'strat'
    mod_data_df[me_strat] = np.cumprod(1 + mod_data_df['strat_return'].values)

    if plot_html:
        fig = realtime_plotting_utility.plot_multiple_time_series(
            data_df=mod_data_df[[me_strat]],
            logy=True, split=False,
            put_on_same_scale=False,
            title=f'Perf{str(all_tokens)}')
        fig.show()
        fig = realtime_plotting_utility.plot_multiple_time_series(
            data_df=mod_data_df[[me_strat]],
            logy=False, split=False,
            put_on_same_scale=False,
            title=f'Perf{str(all_tokens)}')
        fig.show()
    title = f'WEEKLY_MULTICOIN_RSI_{moderation}'
    backtest_df = mod_data_df[[me_strat]].copy()
    backtest_df.columns = ['strat']
    strat_data_df = backtest_df[['strat']].copy()

    daily_df = riskmetrics.filter_daily(strat_data_df)
    daily_df = daily_df.dropna()

    if compute_lo_strat:
        title = 'multicoin_daily_continuous_rsilo'
        backtest_df = daily_df[['strat']].copy()
        whole_kpis = True
        if whole_kpis:
            strat_data_df = backtest_df[['strat']].copy()
            from cryptotoolbox.analyzer import market

            # strat_data_df = strat_data_df[strat_data_df.index >= '2021-02-01'].copy()
            ma = market.MarketAnalyzer(strat_data_df, hourlyze=True)

            print('computing kpis')
            kpi_df = ma.get_kpi().T
            kpi_df = kpi_df.dropna()
            kpi_df = kpi_df[~np.isnan(kpi_df.sharpe)]
            print(kpi_df.head())

        backtest_df.columns = ['strat']
        riskmetrics.compute_plot_excel_kpis_meterics_metrics(backtest_df, title,
                                                             local_root_directory,
                                                             plot_html=True,
                                                             write_file=True)
    return mod_data_df.copy()

def compute_alpha_signal_rsilo_weekly_multicoin_discrete(df=None, core_tokens=['BTC', 'ETH'], extra_tokens =[], rsi_lookback = 8 ,threshold = 60 , rebalancing_day=6,lo_sig_suffix='RSILO', compute_lo_strat=True, plot_html=False, local_root_directory='None'):
    all_tokens = core_tokens + extra_tokens
    for current_token in all_tokens:
        df['hour'] = df.index.hour
        all_dfs = None
        for me_hour in range(0,24):
            daily_df = df[df['hour'] == me_hour].copy()
            daily_df[f'DAILY_RSI_{current_token}_{me_hour}'] = talib.RSI(daily_df[f'close_{current_token}'], rsi_lookback)
            if all_dfs is None:
                all_dfs = daily_df.copy()
            else:
                all_dfs = pd.concat([all_dfs.copy(), daily_df.copy()])

        all_dfs = all_dfs.sort_index()
        column_list_asset = []

        for me_hour in range(0,24):
            all_dfs[f'DAILY_RSI_{current_token}_{me_hour}'] = all_dfs[f'DAILY_RSI_{current_token}_{me_hour}'].fillna(0.)
            column_list_asset.append(f'DAILY_RSI_{current_token}_{me_hour}')

        all_dfs[f'DAILY_RSI_{current_token}'] = all_dfs[column_list_asset].sum(axis=1)
        df = pd.merge(df.copy(),  all_dfs[[f'DAILY_RSI_{current_token}']].copy() , how='left', left_index=True, right_index=True)

    def compute_dual_RSI_muticoin_discrete(row_df, threshold=60, all_tokens=[],lo_sig_suffix='RSILO'):
        signals={}
        for me_tok in all_tokens:
            if row_df[f'DAILY_RSI_{me_tok}']>threshold:
                signals[f'S{lo_sig_suffix}{me_tok}'] = 1.
            else:
                signals[f'S{lo_sig_suffix}{me_tok}'] = 0.
        return signals

    go_rsi = lambda x: compute_dual_RSI_muticoin_discrete(x, threshold=threshold, all_tokens=all_tokens, lo_sig_suffix=lo_sig_suffix)
    sig_df= df.apply(go_rsi, axis=1)
    sig_df = sig_df.to_frame()
    sig_df.columns = ['signal_gen']
    sig_df['signal'] = sig_df['signal_gen'].shift()
    sig_df.index = all_dfs.index
    sig_df = sig_df.iloc[1:]
    old_index = sig_df.index
    sig_df = pd.DataFrame().from_records(sig_df['signal'].values)
    sig_df.index = old_index

    sig_df['Counter'] = 0
    for itok in all_tokens:
        sig_df['Counter'] += sig_df[f'S{lo_sig_suffix}{itok}']

    def expo(y, n_max=3):
        S = np.zeros(np.size(y))
        for i in range(np.size(y)):
            if y[i] > n_max:
                S[i] = 1 / y[i]
            elif y[i] > 0:
                S[i] = 1. / n_max
            else:
                S[i] = 0
        return S

    n_max = int(len(all_tokens) / 2.) + 1
    sig_df['expo'] = expo(sig_df['Counter'].values, n_max=n_max)

    for me_tok in all_tokens:
        sig_df[f'S{lo_sig_suffix}{me_tok}'] = sig_df[f'S{lo_sig_suffix}{me_tok}'] * sig_df['expo']

    for current_token in all_tokens:
        df[f'return_{current_token}'] = df[f'close_{current_token}'].pct_change()

    data_df = pd.merge(df.copy(), sig_df.copy(), how='left', left_index=True, right_index=True)

    ### we rebalance monday morning
    def get_filter_date(row,rebalancing_day=6):
        ##### to get the proper daily close
        #### we only keep the signal that has been emitted the day after
        next_day = (rebalancing_day+1)%7
        if row['weekday'] == next_day and row['hour'] == 0:
            return True
        else:
            return False

    data_df['weekday'] = data_df.index.weekday
    data_df['hour'] = data_df.index.hour
    go_reb = lambda x : get_filter_date(x, rebalancing_day=rebalancing_day)
    data_df['rebalancing'] = data_df.apply(go_reb, axis=1)
    ##### we rebalance with the close of rebalancing_day :
    def rebalancing_signal_cut(row, token='BTC', lo_sig_suffix='RSILO'):
        if row['rebalancing']:
            return row[f'S{lo_sig_suffix}{token}']
        else:
            return np.nan
    for current_token in all_tokens:
        gotok = lambda x: rebalancing_signal_cut(x, token=current_token,lo_sig_suffix=lo_sig_suffix)
        data_df[f'S{lo_sig_suffix}{current_token}'] = data_df.apply(gotok, axis=1)
        data_df[f'S{lo_sig_suffix}{current_token}'] = data_df[f'S{lo_sig_suffix}{current_token}'].ffill()

    moderation = 1.
    mod_data_df = data_df.copy()

    def compute_dual_return(row, moderation=1.,all_tokens=[], lo_sig_suffix='RSILO'):
        global_ret = 0.
        for current_token in all_tokens:
            global_ret = global_ret + row[f'S{lo_sig_suffix}{current_token}'] * row[f'return_{current_token}'] * moderation
        return global_ret

    go_compute = lambda x: compute_dual_return(x, moderation=moderation, all_tokens=all_tokens,lo_sig_suffix=lo_sig_suffix)
    mod_data_df['strat_return'] = mod_data_df.apply(go_compute, axis=1)

    mod_data_df['strat_return'] = mod_data_df['strat_return'].fillna(0.)
    me_strat = 'strat'
    mod_data_df[me_strat] = np.cumprod(1 + mod_data_df['strat_return'].values)

    if plot_html:
        fig = realtime_plotting_utility.plot_multiple_time_series(
            data_df=mod_data_df[[me_strat]],
            logy=True, split=False,
            put_on_same_scale=False,
            title=f'Perf{str(all_tokens)}')
        fig.show()
        fig = realtime_plotting_utility.plot_multiple_time_series(
            data_df=mod_data_df[[me_strat]],
            logy=False, split=False,
            put_on_same_scale=False,
            title=f'Perf{str(all_tokens)}')
        fig.show()
    title = f'WEEKLY_MULTICOIN_RSI_{moderation}'
    backtest_df = mod_data_df[[me_strat]].copy()
    backtest_df.columns = ['strat']
    strat_data_df = backtest_df[['strat']].copy()

    daily_df = riskmetrics.filter_daily(strat_data_df)
    daily_df = daily_df.dropna()

    if compute_lo_strat:
        title = 'multicoin_weekly_discrete_rsilo'
        backtest_df = daily_df[['strat']].copy()
        whole_kpis = True
        if whole_kpis:
            strat_data_df = backtest_df[['strat']].copy()
            from cryptotoolbox.analyzer import market

            # strat_data_df = strat_data_df[strat_data_df.index >= '2021-02-01'].copy()
            ma = market.MarketAnalyzer(strat_data_df, hourlyze=True)

            print('computing kpis')
            kpi_df = ma.get_kpi().T
            kpi_df = kpi_df.dropna()
            kpi_df = kpi_df[~np.isnan(kpi_df.sharpe)]
            print(kpi_df.head())

        backtest_df.columns = ['strat']
        riskmetrics.compute_plot_excel_kpis_meterics_metrics(backtest_df, title,
                                                             local_root_directory,
                                                             plot_html=True,
                                                             write_file=True)
    return mod_data_df.copy()


def compute_alpha_signal_rsilo_daily_multicoin_discrete(df=None, core_tokens=['BTC', 'ETH'], extra_tokens =[], rsi_lookback = 8 ,threshold = 60 , rebalancing_day=6,lo_sig_suffix='RSILO', compute_lo_strat=True, plot_html=False, local_root_directory='None'):
    all_tokens = core_tokens + extra_tokens
    for current_token in all_tokens:
        df['hour'] = df.index.hour
        all_dfs = None
        for me_hour in range(0,24):
            daily_df = df[df['hour'] == me_hour].copy()
            daily_df[f'DAILY_RSI_{current_token}_{me_hour}'] = talib.RSI(daily_df[f'close_{current_token}'], rsi_lookback)
            if all_dfs is None:
                all_dfs = daily_df.copy()
            else:
                all_dfs = pd.concat([all_dfs.copy(), daily_df.copy()])

        all_dfs = all_dfs.sort_index()
        column_list_asset = []

        for me_hour in range(0,24):
            all_dfs[f'DAILY_RSI_{current_token}_{me_hour}'] = all_dfs[f'DAILY_RSI_{current_token}_{me_hour}'].fillna(0.)
            column_list_asset.append(f'DAILY_RSI_{current_token}_{me_hour}')

        all_dfs[f'DAILY_RSI_{current_token}'] = all_dfs[column_list_asset].sum(axis=1)
        df = pd.merge(df.copy(),  all_dfs[[f'DAILY_RSI_{current_token}']].copy() , how='left', left_index=True, right_index=True)

    def compute_dual_RSI_muticoin_discrete(row_df, threshold=60, all_tokens=[],lo_sig_suffix='RSILO'):
        signals={}
        for me_tok in all_tokens:
            if row_df[f'DAILY_RSI_{me_tok}']>threshold:
                signals[f'S{lo_sig_suffix}{me_tok}'] = 1.
            else:
                signals[f'S{lo_sig_suffix}{me_tok}'] = 0.
        return signals

    go_rsi = lambda x: compute_dual_RSI_muticoin_discrete(x, threshold=threshold, all_tokens=all_tokens, lo_sig_suffix=lo_sig_suffix)
    sig_df= df.apply(go_rsi, axis=1)
    sig_df = sig_df.to_frame()
    sig_df.columns = ['signal_gen']
    sig_df['signal'] = sig_df['signal_gen'].shift()
    sig_df.index = all_dfs.index
    sig_df = sig_df.iloc[1:]
    old_index = sig_df.index
    sig_df = pd.DataFrame().from_records(sig_df['signal'].values)
    sig_df.index = old_index

    sig_df['Counter'] = 0
    for itok in all_tokens:
        sig_df['Counter'] += sig_df[f'S{lo_sig_suffix}{itok}']

    def expo(y, n_max=3):
        S = np.zeros(np.size(y))
        for i in range(np.size(y)):
            if y[i] > n_max:
                S[i] = 1 / y[i]
            elif y[i] > 0:
                S[i] = 1. / n_max
            else:
                S[i] = 0
        return S

    n_max = int(len(all_tokens) / 2.) + 1
    sig_df['expo'] = expo(sig_df['Counter'].values, n_max=n_max)


    for me_tok in all_tokens:
        sig_df[f'S{lo_sig_suffix}{me_tok}'] = sig_df[f'S{lo_sig_suffix}{me_tok}'] * sig_df['expo']

    for current_token in all_tokens:
        df[f'return_{current_token}'] = df[f'close_{current_token}'].pct_change()

    data_df = pd.merge(df.copy(), sig_df.copy(), how='left', left_index=True, right_index=True)

    ### we rebalance monday morning
    def get_day_filter_date(row,rebalancing_day=6):
        ##### to get the proper daily close
        #### we only keep the signal that has been emitted the day after
        if row['hour'] == 0:
            return True
        else:
            return False

    data_df['weekday'] = data_df.index.weekday
    data_df['hour'] = data_df.index.hour
    go_reb = lambda x : get_day_filter_date(x, rebalancing_day=rebalancing_day)
    data_df['rebalancing'] = data_df.apply(go_reb, axis=1)
    ##### we rebalance with the close of rebalancing_day :
    def rebalancing_signal_cut(row, token='BTC', lo_sig_suffix='RSILO'):
        if row['rebalancing']:
            return row[f'S{lo_sig_suffix}{token}']
        else:
            return np.nan
    for current_token in all_tokens:
        gotok = lambda x: rebalancing_signal_cut(x, token=current_token,lo_sig_suffix=lo_sig_suffix)
        data_df[f'S{lo_sig_suffix}{current_token}'] = data_df.apply(gotok, axis=1)
        data_df[f'S{lo_sig_suffix}{current_token}'] = data_df[f'S{lo_sig_suffix}{current_token}'].ffill()

    moderation = 1.
    mod_data_df = data_df.copy()

    def compute_dual_return(row, moderation=1.,all_tokens=[], lo_sig_suffix='RSILO'):
        global_ret = 0.
        for current_token in all_tokens:
            global_ret = global_ret + row[f'S{lo_sig_suffix}{current_token}'] * row[f'return_{current_token}'] * moderation
        return global_ret

    go_compute = lambda x: compute_dual_return(x, moderation=moderation, all_tokens=all_tokens,lo_sig_suffix=lo_sig_suffix)
    mod_data_df['strat_return'] = mod_data_df.apply(go_compute, axis=1)

    mod_data_df['strat_return'] = mod_data_df['strat_return'].fillna(0.)
    me_strat = 'strat'
    mod_data_df[me_strat] = np.cumprod(1 + mod_data_df['strat_return'].values)

    if plot_html:
        fig = realtime_plotting_utility.plot_multiple_time_series(
            data_df=mod_data_df[[me_strat]],
            logy=True, split=False,
            put_on_same_scale=False,
            title=f'Perf{str(all_tokens)}')
        fig.show()
        fig = realtime_plotting_utility.plot_multiple_time_series(
            data_df=mod_data_df[[me_strat]],
            logy=False, split=False,
            put_on_same_scale=False,
            title=f'Perf{str(all_tokens)}')
        fig.show()
    title = f'WEEKLY_MULTICOIN_RSI_{moderation}'
    backtest_df = mod_data_df[[me_strat]].copy()
    backtest_df.columns = ['strat']
    strat_data_df = backtest_df[['strat']].copy()

    daily_df = riskmetrics.filter_daily(strat_data_df)
    daily_df = daily_df.dropna()

    if compute_lo_strat:
        title = 'multicoin_daily_discrete_rsilo'
        backtest_df = daily_df[['strat']].copy()
        whole_kpis = True
        if whole_kpis:
            strat_data_df = backtest_df[['strat']].copy()
            from cryptotoolbox.analyzer import market

            # strat_data_df = strat_data_df[strat_data_df.index >= '2021-02-01'].copy()
            ma = market.MarketAnalyzer(strat_data_df, hourlyze=True)

            print('computing kpis')
            kpi_df = ma.get_kpi().T
            kpi_df = kpi_df.dropna()
            kpi_df = kpi_df[~np.isnan(kpi_df.sharpe)]
            print(kpi_df.head())

        backtest_df.columns = ['strat']
        riskmetrics.compute_plot_excel_kpis_meterics_metrics(backtest_df, title,
                                                             local_root_directory,
                                                             plot_html=True,
                                                             write_file=True)
    return mod_data_df.copy()


def compute_alpha_signal_rsilo_multi_freq_multicoin_discrete_dailystoploss(df=None, core_tokens=['BTC', 'ETH'], extra_tokens =[], rsi_lookback = 8 ,threshold = 60 , rebalancing_day=6,lo_sig_suffix='RSILO', compute_lo_strat=True, plot_html=False, local_root_directory='None'):
    all_tokens = core_tokens + extra_tokens
    for current_token in all_tokens:
        df['hour'] = df.index.hour
        all_dfs = None
        for me_hour in range(0,24):
            daily_df = df[df['hour'] == me_hour].copy()
            daily_df[f'DAILY_RSI_{current_token}_{me_hour}'] = talib.RSI(daily_df[f'close_{current_token}'], rsi_lookback)
            if all_dfs is None:
                all_dfs = daily_df.copy()
            else:
                all_dfs = pd.concat([all_dfs.copy(), daily_df.copy()])

        all_dfs = all_dfs.sort_index()
        column_list_asset = []

        for me_hour in range(0,24):
            all_dfs[f'DAILY_RSI_{current_token}_{me_hour}'] = all_dfs[f'DAILY_RSI_{current_token}_{me_hour}'].fillna(0.)
            column_list_asset.append(f'DAILY_RSI_{current_token}_{me_hour}')

        all_dfs[f'DAILY_RSI_{current_token}'] = all_dfs[column_list_asset].sum(axis=1)
        df = pd.merge(df.copy(),  all_dfs[[f'DAILY_RSI_{current_token}']].copy() , how='left', left_index=True, right_index=True)

    def compute_dual_RSI_muticoin_discrete(row_df, threshold=60, all_tokens=[],lo_sig_suffix='RSILO'):
        signals={}
        for me_tok in all_tokens:
            if row_df[f'DAILY_RSI_{me_tok}']>threshold:
                signals[f'S{lo_sig_suffix}{me_tok}'] = 1.
            else:
                signals[f'S{lo_sig_suffix}{me_tok}'] = 0.
        return signals

    go_rsi = lambda x: compute_dual_RSI_muticoin_discrete(x, threshold=threshold, all_tokens=all_tokens, lo_sig_suffix=lo_sig_suffix)
    sig_df= df.apply(go_rsi, axis=1)
    sig_df = sig_df.to_frame()
    sig_df.columns = ['signal_gen']
    sig_df['signal'] = sig_df['signal_gen'].shift()
    sig_df.index = all_dfs.index
    sig_df = sig_df.iloc[1:]
    old_index = sig_df.index
    sig_df = pd.DataFrame().from_records(sig_df['signal'].values)
    sig_df.index = old_index

    sig_df['Counter'] = 0
    for itok in all_tokens:
        sig_df['Counter'] += sig_df[f'S{lo_sig_suffix}{itok}']

    def expo(y, n_max=3):
        S = np.zeros(np.size(y))
        for i in range(np.size(y)):
            if y[i] > n_max:
                S[i] = 1 / y[i]
            elif y[i] > 0:
                S[i] = 1. / n_max
            else:
                S[i] = 0
        return S

    n_max = int(len(all_tokens) / 2.) + 1
    sig_df['expo'] = expo(sig_df['Counter'].values, n_max=n_max)


    for me_tok in all_tokens:
        sig_df[f'S{lo_sig_suffix}{me_tok}'] = sig_df[f'S{lo_sig_suffix}{me_tok}'] * sig_df['expo']

    for current_token in all_tokens:
        df[f'return_{current_token}'] = df[f'close_{current_token}'].pct_change()

    data_df = pd.merge(df.copy(), sig_df.copy(), how='left', left_index=True, right_index=True)

    ### we rebalance monday morning
    ######### weekly signal
    def get_filter_date(row,rebalancing_day=6):
        ##### to get the proper daily close
        #### we only keep the signal that has been emitted the day after
        next_day = (rebalancing_day+1)%7
        if row['weekday'] == next_day and row['hour'] == 0:
            return True
        else:
            return False

    data_df['weekday'] = data_df.index.weekday
    data_df['hour'] = data_df.index.hour
    go_reb = lambda x : get_filter_date(x, rebalancing_day=rebalancing_day)
    data_df['rebalancing'] = data_df.apply(go_reb, axis=1)

    def get_day_filter_date(row):
        if row['hour'] == 0:
            return True
        else:
            return False
    data_df['day_rebalancing'] = data_df.apply(get_day_filter_date, axis=1)

    ##### we rebalance with the close of rebalancing_day :
    def rebalancing_signal_cut(row, token='BTC', lo_sig_suffix='RSILO'):
        if row['rebalancing']:
            return row[f'SH{lo_sig_suffix}{token}']
        else:
            return np.nan

    def day_rebalancing_signal_cut(row, token='BTC', lo_sig_suffix='RSILO'):
        if row['day_rebalancing']:
            return row[f'SH{lo_sig_suffix}{token}']
        else:
            return np.nan

    multi_freq_sigs = []
    investigative_list = []

    for current_token in all_tokens:

        godaytok = lambda x: day_rebalancing_signal_cut(x, token=current_token,lo_sig_suffix=lo_sig_suffix)
        gotok = lambda x: rebalancing_signal_cut(x, token=current_token,lo_sig_suffix=lo_sig_suffix)
        data_df[f'SH{lo_sig_suffix}{current_token}'] = data_df[f'S{lo_sig_suffix}{current_token}']

        data_df[f'SD{lo_sig_suffix}{current_token}'] = data_df.apply(godaytok, axis=1)
        data_df[f'SD{lo_sig_suffix}{current_token}'] = data_df[f'SD{lo_sig_suffix}{current_token}'].ffill()

        data_df[f'S{lo_sig_suffix}{current_token}'] = data_df.apply(gotok, axis=1)
        data_df[f'S{lo_sig_suffix}{current_token}'] = data_df[f'S{lo_sig_suffix}{current_token}'].ffill()
        multi_freq_sigs.append(f'SH{lo_sig_suffix}{current_token}')
        multi_freq_sigs.append(f'SD{lo_sig_suffix}{current_token}')
        multi_freq_sigs.append(f'S{lo_sig_suffix}{current_token}')
        investigative_list.append(f'SH{lo_sig_suffix}{current_token}')
        investigative_list.append(f'SD{lo_sig_suffix}{current_token}')
        investigative_list.append(f'S{lo_sig_suffix}{current_token}')

##### end of weekly
    data_df['week_epoch'] = data_df['rebalancing'].cumsum()
    data_df['day_epoch'] = data_df['day_rebalancing'].cumsum()
    investigative_list.append('week_epoch')
    investigative_list.append('day_epoch')
    data_df = data_df.fillna(0.)
    def get_daily_stoploss(data_df,investigative_list=None):
        data_stop_loss_df = data_df.copy()
        week_btc_on = data_df[f'SRSILOBTC'].iloc[0] > 0
        week_eth_on = data_df[f'SRSILOETH'].iloc[0] > 0
        if week_btc_on :
            changing_day_states = len(data_df[f'SDRSILOBTC'].unique())
            if changing_day_states>1:
                data_df[f'SDRSILOBTC_OFF'] = data_df[f'SDRSILOBTC']==0
                first_day_off = np.argmax(data_df[f'SDRSILOBTC_OFF'].values)
                data_stop_loss_df[f'SRSILOBTC'].iloc[first_day_off:]=0

        if week_eth_on:
            changing_day_states = len(data_df[f'SDRSILOETH'].unique())
            if changing_day_states>1:
                data_df[f'SDRSILOETH_OFF'] = data_df[f'SDRSILOETH']==0
                first_day_off = np.argmax(data_df[f'SDRSILOETH_OFF'].values)
                data_stop_loss_df[f'SRSILOETH'].iloc[first_day_off:]=0
        return data_stop_loss_df
    go_stop = lambda x : get_daily_stoploss(x,investigative_list=investigative_list)
    stop_loss_df = data_df.groupby('week_epoch').apply(go_stop)

    moderation = 1.
    mod_data_df = stop_loss_df.copy()

    def compute_dual_return(row, moderation=1.,all_tokens=[], lo_sig_suffix='RSILO'):
        global_ret = 0.
        for current_token in all_tokens:
            global_ret = global_ret + row[f'S{lo_sig_suffix}{current_token}'] * row[f'return_{current_token}'] * moderation
        return global_ret

    go_compute = lambda x: compute_dual_return(x, moderation=moderation, all_tokens=all_tokens,lo_sig_suffix=lo_sig_suffix)
    mod_data_df['strat_return'] = mod_data_df.apply(go_compute, axis=1)

    mod_data_df['strat_return'] = mod_data_df['strat_return'].fillna(0.)
    me_strat = 'strat'
    mod_data_df[me_strat] = np.cumprod(1 + mod_data_df['strat_return'].values)


    if plot_html:
        fig = realtime_plotting_utility.plot_multiple_time_series(
            data_df=mod_data_df[multi_freq_sigs],
            logy=True, split=False,
            put_on_same_scale=False,
            title=f'Multi freq signals{str(all_tokens)}')
        fig.show()

        fig = realtime_plotting_utility.plot_multiple_time_series(
            data_df=mod_data_df[[me_strat]],
            logy=True, split=False,
            put_on_same_scale=False,
            title=f'Perf{str(all_tokens)}')
        fig.show()
        fig = realtime_plotting_utility.plot_multiple_time_series(
            data_df=mod_data_df[[me_strat]],
            logy=False, split=False,
            put_on_same_scale=False,
            title=f'Perf{str(all_tokens)}')
        fig.show()
    title = f'WEEKLY_MULTICOIN_RSI_{moderation}'
    backtest_df = mod_data_df[[me_strat]].copy()
    backtest_df.columns = ['strat']
    strat_data_df = backtest_df[['strat']].copy()

    daily_df = riskmetrics.filter_daily(strat_data_df)
    daily_df = daily_df.dropna()

    if compute_lo_strat:
        title = 'multicoin_daily_discrete_rsilo'
        backtest_df = daily_df[['strat']].copy()
        whole_kpis = True
        if whole_kpis:
            strat_data_df = backtest_df[['strat']].copy()
            from cryptotoolbox.analyzer import market

            # strat_data_df = strat_data_df[strat_data_df.index >= '2021-02-01'].copy()
            ma = market.MarketAnalyzer(strat_data_df, hourlyze=True)

            print('computing kpis')
            kpi_df = ma.get_kpi().T
            kpi_df = kpi_df.dropna()
            kpi_df = kpi_df[~np.isnan(kpi_df.sharpe)]
            print(kpi_df.head())

        backtest_df.columns = ['strat']
        riskmetrics.compute_plot_excel_kpis_meterics_metrics(backtest_df, title,
                                                             local_root_directory,
                                                             plot_html=True,
                                                             write_file=True)
    return mod_data_df.copy()

def compute_alpha_signal_rsilo_multi_freq_multicoin_discrete_hourlystoploss(df=None, core_tokens=['BTC', 'ETH'], extra_tokens =[], rsi_lookback = 8 ,threshold = 60 , rebalancing_day=6,lo_sig_suffix='RSILO', compute_lo_strat=True, plot_html=False, local_root_directory='None'):
    all_tokens = core_tokens + extra_tokens
    for current_token in all_tokens:
        df['hour'] = df.index.hour
        all_dfs = None
        for me_hour in range(0,24):
            daily_df = df[df['hour'] == me_hour].copy()
            daily_df[f'DAILY_RSI_{current_token}_{me_hour}'] = talib.RSI(daily_df[f'close_{current_token}'], rsi_lookback)
            if all_dfs is None:
                all_dfs = daily_df.copy()
            else:
                all_dfs = pd.concat([all_dfs.copy(), daily_df.copy()])

        all_dfs = all_dfs.sort_index()
        column_list_asset = []

        for me_hour in range(0,24):
            all_dfs[f'DAILY_RSI_{current_token}_{me_hour}'] = all_dfs[f'DAILY_RSI_{current_token}_{me_hour}'].fillna(0.)
            column_list_asset.append(f'DAILY_RSI_{current_token}_{me_hour}')

        all_dfs[f'DAILY_RSI_{current_token}'] = all_dfs[column_list_asset].sum(axis=1)
        df = pd.merge(df.copy(),  all_dfs[[f'DAILY_RSI_{current_token}']].copy() , how='left', left_index=True, right_index=True)

    def compute_dual_RSI_muticoin_discrete(row_df, threshold=60, all_tokens=[],lo_sig_suffix='RSILO'):
        signals={}
        for me_tok in all_tokens:
            if row_df[f'DAILY_RSI_{me_tok}']>threshold:
                signals[f'S{lo_sig_suffix}{me_tok}'] = 1.
            else:
                signals[f'S{lo_sig_suffix}{me_tok}'] = 0.
        return signals

    go_rsi = lambda x: compute_dual_RSI_muticoin_discrete(x, threshold=threshold, all_tokens=all_tokens, lo_sig_suffix=lo_sig_suffix)
    sig_df= df.apply(go_rsi, axis=1)
    sig_df = sig_df.to_frame()
    sig_df.columns = ['signal_gen']
    sig_df['signal'] = sig_df['signal_gen'].shift()
    sig_df.index = all_dfs.index
    sig_df = sig_df.iloc[1:]
    old_index = sig_df.index
    sig_df = pd.DataFrame().from_records(sig_df['signal'].values)
    sig_df.index = old_index

    sig_df['Counter'] = 0
    for itok in all_tokens:
        sig_df['Counter'] += sig_df[f'S{lo_sig_suffix}{itok}']

    def expo(y, n_max=3):
        S = np.zeros(np.size(y))
        for i in range(np.size(y)):
            if y[i] > n_max:
                S[i] = 1 / y[i]
            elif y[i] > 0:
                S[i] = 1. / n_max
            else:
                S[i] = 0
        return S

    n_max = int(len(all_tokens) / 2.) + 1
    sig_df['expo'] = expo(sig_df['Counter'].values, n_max=n_max)


    for me_tok in all_tokens:
        sig_df[f'S{lo_sig_suffix}{me_tok}'] = sig_df[f'S{lo_sig_suffix}{me_tok}'] * sig_df['expo']

    for current_token in all_tokens:
        df[f'return_{current_token}'] = df[f'close_{current_token}'].pct_change()

    data_df = pd.merge(df.copy(), sig_df.copy(), how='left', left_index=True, right_index=True)

    ### we rebalance monday morning
    ######### weekly signal
    def get_filter_date(row,rebalancing_day=6):
        ##### to get the proper daily close
        #### we only keep the signal that has been emitted the day after
        next_day = (rebalancing_day+1)%7
        if row['weekday'] == next_day and row['hour'] == 0:
            return True
        else:
            return False

    data_df['weekday'] = data_df.index.weekday
    data_df['hour'] = data_df.index.hour
    go_reb = lambda x : get_filter_date(x, rebalancing_day=rebalancing_day)
    data_df['rebalancing'] = data_df.apply(go_reb, axis=1)

    def get_day_filter_date(row):
        if row['hour'] == 0:
            return True
        else:
            return False
    data_df['day_rebalancing'] = data_df.apply(get_day_filter_date, axis=1)

    ##### we rebalance with the close of rebalancing_day :
    def rebalancing_signal_cut(row, token='BTC', lo_sig_suffix='RSILO'):
        if row['rebalancing']:
            return row[f'SH{lo_sig_suffix}{token}']
        else:
            return np.nan

    def day_rebalancing_signal_cut(row, token='BTC', lo_sig_suffix='RSILO'):
        if row['day_rebalancing']:
            return row[f'SH{lo_sig_suffix}{token}']
        else:
            return np.nan

    multi_freq_sigs = []
    investigative_list = []

    for current_token in all_tokens:

        godaytok = lambda x: day_rebalancing_signal_cut(x, token=current_token,lo_sig_suffix=lo_sig_suffix)
        gotok = lambda x: rebalancing_signal_cut(x, token=current_token,lo_sig_suffix=lo_sig_suffix)
        data_df[f'SH{lo_sig_suffix}{current_token}'] = data_df[f'S{lo_sig_suffix}{current_token}']

        data_df[f'SD{lo_sig_suffix}{current_token}'] = data_df.apply(godaytok, axis=1)
        data_df[f'SD{lo_sig_suffix}{current_token}'] = data_df[f'SD{lo_sig_suffix}{current_token}'].ffill()

        data_df[f'S{lo_sig_suffix}{current_token}'] = data_df.apply(gotok, axis=1)
        data_df[f'S{lo_sig_suffix}{current_token}'] = data_df[f'S{lo_sig_suffix}{current_token}'].ffill()
        multi_freq_sigs.append(f'SH{lo_sig_suffix}{current_token}')
        multi_freq_sigs.append(f'SD{lo_sig_suffix}{current_token}')
        multi_freq_sigs.append(f'S{lo_sig_suffix}{current_token}')
        investigative_list.append(f'SH{lo_sig_suffix}{current_token}')
        investigative_list.append(f'SD{lo_sig_suffix}{current_token}')
        investigative_list.append(f'S{lo_sig_suffix}{current_token}')

##### end of weekly
    data_df['week_epoch'] = data_df['rebalancing'].cumsum()
    data_df['day_epoch'] = data_df['day_rebalancing'].cumsum()
    investigative_list.append('week_epoch')
    investigative_list.append('day_epoch')
    data_df = data_df.fillna(0.)
    def get_hourly_stoploss(data_df,investigative_list=None):
        data_stop_loss_df = data_df.copy()
        week_btc_on = data_df[f'SRSILOBTC'].iloc[0] > 0
        week_eth_on = data_df[f'SRSILOETH'].iloc[0] > 0
        if week_btc_on :
            changing_day_states = len(data_df[f'SHRSILOBTC'].unique())
            if changing_day_states>1:
                data_df[f'SHRSILOBTC_OFF'] = data_df[f'SHRSILOBTC']==0
                first_day_off = np.argmax(data_df[f'SHRSILOBTC_OFF'].values)
                data_stop_loss_df[f'SRSILOBTC'].iloc[first_day_off:]=0

        if week_eth_on:
            changing_day_states = len(data_df[f'SHRSILOETH'].unique())
            if changing_day_states>1:
                data_df[f'SHRSILOETH_OFF'] = data_df[f'SHRSILOETH']==0
                first_day_off = np.argmax(data_df[f'SHRSILOETH_OFF'].values)
                data_stop_loss_df[f'SRSILOETH'].iloc[first_day_off:]=0
        return data_stop_loss_df
    go_stop = lambda x : get_hourly_stoploss(x,investigative_list=investigative_list)
    stop_loss_df = data_df.groupby('week_epoch').apply(go_stop)

    moderation = 1.
    mod_data_df = stop_loss_df.copy()

    def compute_dual_return(row, moderation=1.,all_tokens=[], lo_sig_suffix='RSILO'):
        global_ret = 0.
        for current_token in all_tokens:
            global_ret = global_ret + row[f'S{lo_sig_suffix}{current_token}'] * row[f'return_{current_token}'] * moderation
        return global_ret

    go_compute = lambda x: compute_dual_return(x, moderation=moderation, all_tokens=all_tokens,lo_sig_suffix=lo_sig_suffix)
    mod_data_df['strat_return'] = mod_data_df.apply(go_compute, axis=1)

    mod_data_df['strat_return'] = mod_data_df['strat_return'].fillna(0.)
    me_strat = 'strat'
    mod_data_df[me_strat] = np.cumprod(1 + mod_data_df['strat_return'].values)


    if plot_html:
        fig = realtime_plotting_utility.plot_multiple_time_series(
            data_df=mod_data_df[multi_freq_sigs],
            logy=True, split=False,
            put_on_same_scale=False,
            title=f'Multi freq signals{str(all_tokens)}')
        fig.show()

        fig = realtime_plotting_utility.plot_multiple_time_series(
            data_df=mod_data_df[[me_strat]],
            logy=True, split=False,
            put_on_same_scale=False,
            title=f'Perf{str(all_tokens)}')
        fig.show()
        fig = realtime_plotting_utility.plot_multiple_time_series(
            data_df=mod_data_df[[me_strat]],
            logy=False, split=False,
            put_on_same_scale=False,
            title=f'Perf{str(all_tokens)}')
        fig.show()
    title = f'WEEKLY_MULTICOIN_RSI_{moderation}'
    backtest_df = mod_data_df[[me_strat]].copy()
    backtest_df.columns = ['strat']
    strat_data_df = backtest_df[['strat']].copy()

    daily_df = riskmetrics.filter_daily(strat_data_df)
    daily_df = daily_df.dropna()

    if compute_lo_strat:
        title = 'multicoin_daily_discrete_rsilo'
        backtest_df = daily_df[['strat']].copy()
        whole_kpis = True
        if whole_kpis:
            strat_data_df = backtest_df[['strat']].copy()
            from cryptotoolbox.analyzer import market

            # strat_data_df = strat_data_df[strat_data_df.index >= '2021-02-01'].copy()
            ma = market.MarketAnalyzer(strat_data_df, hourlyze=True)

            print('computing kpis')
            kpi_df = ma.get_kpi().T
            kpi_df = kpi_df.dropna()
            kpi_df = kpi_df[~np.isnan(kpi_df.sharpe)]
            print(kpi_df.head())

        backtest_df.columns = ['strat']
        riskmetrics.compute_plot_excel_kpis_meterics_metrics(backtest_df, title,
                                                             local_root_directory,
                                                             plot_html=True,
                                                             write_file=True)
    return mod_data_df.copy()

def compute_alpha_signal_rsilo_hourly_multicoin_discrete(df=None, core_tokens=['BTC', 'ETH'], extra_tokens =[], rsi_lookback = 8 ,threshold = 60 , rebalancing_day=6,lo_sig_suffix='RSILO', compute_lo_strat=True, plot_html=False, local_root_directory='None'):
    all_tokens = core_tokens + extra_tokens
    for current_token in all_tokens:
        df['hour'] = df.index.hour
        all_dfs = None
        for me_hour in range(0,24):
            daily_df = df[df['hour'] == me_hour].copy()
            daily_df[f'DAILY_RSI_{current_token}_{me_hour}'] = talib.RSI(daily_df[f'close_{current_token}'], rsi_lookback)
            if all_dfs is None:
                all_dfs = daily_df.copy()
            else:
                all_dfs = pd.concat([all_dfs.copy(), daily_df.copy()])

        all_dfs = all_dfs.sort_index()
        column_list_asset = []

        for me_hour in range(0,24):
            all_dfs[f'DAILY_RSI_{current_token}_{me_hour}'] = all_dfs[f'DAILY_RSI_{current_token}_{me_hour}'].fillna(0.)
            column_list_asset.append(f'DAILY_RSI_{current_token}_{me_hour}')

        all_dfs[f'DAILY_RSI_{current_token}'] = all_dfs[column_list_asset].sum(axis=1)
        df = pd.merge(df.copy(),  all_dfs[[f'DAILY_RSI_{current_token}']].copy() , how='left', left_index=True, right_index=True)

    def compute_dual_RSI_muticoin_discrete(row_df, threshold=60, all_tokens=[],lo_sig_suffix='RSILO'):
        signals={}
        for me_tok in all_tokens:
            if row_df[f'DAILY_RSI_{me_tok}']>threshold:
                signals[f'S{lo_sig_suffix}{me_tok}'] = 1.
            else:
                signals[f'S{lo_sig_suffix}{me_tok}'] = 0.
        return signals

    go_rsi = lambda x: compute_dual_RSI_muticoin_discrete(x, threshold=threshold, all_tokens=all_tokens, lo_sig_suffix=lo_sig_suffix)
    sig_df= df.apply(go_rsi, axis=1)
    sig_df = sig_df.to_frame()
    sig_df.columns = ['signal_gen']
    sig_df['signal'] = sig_df['signal_gen'].shift()
    sig_df.index = all_dfs.index
    sig_df = sig_df.iloc[1:]
    old_index = sig_df.index
    sig_df = pd.DataFrame().from_records(sig_df['signal'].values)
    sig_df.index = old_index

    sig_df['Counter'] = 0
    for itok in all_tokens:
        sig_df['Counter'] += sig_df[f'S{lo_sig_suffix}{itok}']

    def expo(y, n_max=3):
        S = np.zeros(np.size(y))
        for i in range(np.size(y)):
            if y[i] > n_max:
                S[i] = 1 / y[i]
            elif y[i] > 0:
                S[i] = 1. / n_max
            else:
                S[i] = 0
        return S

    n_max = int(len(all_tokens) / 2.) + 1
    sig_df['expo'] = expo(sig_df['Counter'].values, n_max=n_max)


    for me_tok in all_tokens:
        sig_df[f'S{lo_sig_suffix}{me_tok}'] = sig_df[f'S{lo_sig_suffix}{me_tok}'] * sig_df['expo']

    for current_token in all_tokens:
        df[f'return_{current_token}'] = df[f'close_{current_token}'].pct_change()

    data_df = pd.merge(df.copy(), sig_df.copy(), how='left', left_index=True, right_index=True)

    moderation = 1.
    mod_data_df = data_df.copy()

    def compute_dual_return(row, moderation=1.,all_tokens=[], lo_sig_suffix='RSILO'):
        global_ret = 0.
        for current_token in all_tokens:
            global_ret = global_ret + row[f'S{lo_sig_suffix}{current_token}'] * row[f'return_{current_token}'] * moderation
        return global_ret

    go_compute = lambda x: compute_dual_return(x, moderation=moderation, all_tokens=all_tokens,lo_sig_suffix=lo_sig_suffix)
    mod_data_df['strat_return'] = mod_data_df.apply(go_compute, axis=1)

    mod_data_df['strat_return'] = mod_data_df['strat_return'].fillna(0.)
    me_strat = 'strat'
    mod_data_df[me_strat] = np.cumprod(1 + mod_data_df['strat_return'].values)

    if plot_html:
        fig = realtime_plotting_utility.plot_multiple_time_series(
            data_df=mod_data_df[[me_strat]],
            logy=True, split=False,
            put_on_same_scale=False,
            title=f'Perf{str(all_tokens)}')
        fig.show()
        fig = realtime_plotting_utility.plot_multiple_time_series(
            data_df=mod_data_df[[me_strat]],
            logy=False, split=False,
            put_on_same_scale=False,
            title=f'Perf{str(all_tokens)}')
        fig.show()
    title = f'WEEKLY_MULTICOIN_RSI_{moderation}'
    backtest_df = mod_data_df[[me_strat]].copy()
    backtest_df.columns = ['strat']
    strat_data_df = backtest_df[['strat']].copy()

    daily_df = riskmetrics.filter_daily(strat_data_df)
    daily_df = daily_df.dropna()

    if compute_lo_strat:
        title = 'multicoin_daily_discrete_rsilo'
        backtest_df = daily_df[['strat']].copy()
        whole_kpis = True
        if whole_kpis:
            strat_data_df = backtest_df[['strat']].copy()
            from cryptotoolbox.analyzer import market

            # strat_data_df = strat_data_df[strat_data_df.index >= '2021-02-01'].copy()
            ma = market.MarketAnalyzer(strat_data_df, hourlyze=True)

            print('computing kpis')
            kpi_df = ma.get_kpi().T
            kpi_df = kpi_df.dropna()
            kpi_df = kpi_df[~np.isnan(kpi_df.sharpe)]
            print(kpi_df.head())

        backtest_df.columns = ['strat']
        riskmetrics.compute_plot_excel_kpis_meterics_metrics(backtest_df, title,
                                                             local_root_directory,
                                                             plot_html=True,
                                                             write_file=True)
    return mod_data_df.copy()

def compute_alpha_signal_lo_daily(df=None, core_tokens=['BTC', 'ETH'], extra_tokens=['AVAX'], rebalancing_day=6,lo_sig_suffix='LO',compute_lo_strat=True, plot_html=False):
    all_tokens = core_tokens + extra_tokens
    df['weekday'] = df.index.weekday
    df['rebalance'] = df.index.weekday == rebalancing_day
    for me_token in all_tokens:
        df[f'return_{me_token}'] = df[f'close_{me_token}'].pct_change().fillna(0)
    df.replace([np.inf], 0, inplace=True)
    weekly = pd.DataFrame(index=df.index,
                          data={'SBTC': strat_daily_BTC(df, 'close_BTC', 1, 1, rebalancing_day=rebalancing_day)})
    addw = pd.DataFrame(index=df.index,
                        data={'S{}'.format('ETH'): strat_daily_ETH(df, 'close_ETH', rebalancing_day=rebalancing_day)})
    weekly = weekly.join(addw, how='left')
    for i in extra_tokens:
        addw = pd.DataFrame(index=df.index, data={'S{}'.format(i): strat_daily_BTC(df, f'close_{i}', rebalancing_day=rebalancing_day)})
        weekly = weekly.join(addw, how='left')
    dfsig = weekly.copy()
    dfsig2 = dfsig.copy()
    ######
    df = pd.merge(df.copy(), dfsig2.copy(), how='left', right_index=True, left_index=True)
    def curate_signals(row,under='BTC'):
        if abs(row[f'close_{under}']) <= 1e-3:
            return np.nan
        else:
            return row[f'S{ssj}']

    for ssj in core_tokens + extra_tokens:
        go_curate = lambda x: curate_signals(x, under=ssj)
        df[f'S{ssj}'] = df.apply(go_curate, axis=1)

    signal_df = df.copy()
    signal_df = signal_df.fillna(0.)
    signal_df['Counter'] = 0
    for i in all_tokens:
        if 'S{}'.format(i) in signal_df.columns:
            signal_df['Counter'] += signal_df['S{}'.format(i)]

    def expo(y, n_max=3):
        S = np.zeros(np.size(y))
        for i in range(np.size(y)):
            if y[i] > n_max:
                S[i] = 1 / y[i]
            elif y[i] > 0:
                S[i] = 1. / n_max
            else:
                S[i] = 0
        return S

    n_max = int(len(all_tokens) / 2.) + 1
    signal_df['expo'] = expo(signal_df['Counter'].values, n_max=n_max)

    for me_tok in all_tokens:
        if not 'S{}'.format(me_tok) in signal_df.columns:
            signal_df[f'S{me_tok}'] = 0.

    for me_tok in all_tokens:
        signal_df[f'SE{me_tok}'] = signal_df[f'S{me_tok}'] * signal_df['expo']

    for i in all_tokens:
        signal_df[f'S{lo_sig_suffix}{i}'] = signal_df[f'SE{i}'].shift(1)
        signal_df[f'SRAW{lo_sig_suffix}{i}'] = signal_df[f'S{i}'].shift(1)


    signal_df[f'total_expo'] = 0.
    for me_tok in all_tokens:
        signal_df[f'total_expo'] = signal_df[f'total_expo'] + signal_df[f'S{lo_sig_suffix}{me_tok}']

    fin_df = signal_df.copy()
    if compute_lo_strat:
        def compute_return(row, tokens=[]):
            total_return = 0.
            for me_tok in tokens:
                total_return = total_return + row[f'return_{me_tok}'] * row[f'S{lo_sig_suffix}{me_tok}']
            return total_return

        comp_ret = lambda x: compute_return(x, tokens=all_tokens)
        fin_df['TR'] = fin_df.apply(comp_ret, axis=1)
        fin_df['TR'] = fin_df['TR'].fillna(0.)
        me_strat = 'strat'
        fin_df[me_strat] = np.cumprod(1 + fin_df['TR'].values)
        if plot_html:
            dollar_df = fin_df[['strat']].copy()
            new_names = {'strat': 'Absolute Return Weekly LO Strategy'}
            dollar_df = dollar_df.rename(columns=new_names)
            fig = realtime_plotting_utility.plot_dollar_multiple_time_series(data_df=dollar_df,
                                                                             logy=True, split=False,
                                                                             put_on_same_scale=False,
                                                                             title=f'strategy performance')
            fig.show()
            fig = realtime_plotting_utility.plot_dollar_multiple_time_series(data_df=dollar_df,
                                                                             logy=False, split=False,
                                                                             put_on_same_scale=False,
                                                                             title=f'strategy performance')
            fig.show()


    return fin_df.copy()

def compute_alpha_signal_lo_weekly(df=None, core_tokens=['BTC', 'ETH'], extra_tokens=['AVAX'],     p1btc = 1.01, p2btc = 1.05, p1eth = 1.01, p2eth = 1.05, tone = 14,ttwo = 23, rebalancing_day=6,lo_sig_suffix='LO',compute_lo_strat=True, plot_html=False, whole_kpis=False,local_root_directory='None'):
    all_tokens = core_tokens + extra_tokens
    df['weekday'] = df.index.weekday
    df['rebalance'] = df.index.weekday == rebalancing_day
    for me_token in all_tokens:
        df[f'return_{me_token}'] = df[f'close_{me_token}'].pct_change().fillna(0)
    df.replace([np.inf], 0, inplace=True)
    weekly = pd.DataFrame(index=df.index,
                          data={'SBTC': strat_weekly(df, 'close_BTC', tone=tone, ttwo=ttwo, p1=p1btc, p2=p2btc, rebalancing_day=rebalancing_day)})
    addw = pd.DataFrame(index=df.index,
                        data={'S{}'.format('ETH'): strat_weekly(df, 'close_ETH',  p1=p1eth,p2=p2eth,rebalancing_day=rebalancing_day)})
    weekly = weekly.join(addw, how='left')
    for i in extra_tokens:
        addw = pd.DataFrame(index=df.index, data={'S{}'.format(i): strat_weekly(df, f'close_{i}', rebalancing_day=rebalancing_day)})
        weekly = weekly.join(addw, how='left')
    dfsig = weekly.copy()
    dfsig2 = dfsig.copy()
    ######
    df = pd.merge(df.copy(), dfsig2.copy(), how='left', right_index=True, left_index=True)
    def curate_signals(row,under='BTC'):
        if abs(row[f'close_{under}']) <= 1e-3:
            return np.nan
        else:
            return row[f'S{ssj}']

    for ssj in core_tokens + extra_tokens:
        go_curate = lambda x: curate_signals(x, under=ssj)
        df[f'S{ssj}'] = df.apply(go_curate, axis=1)

    signal_df = df.copy()
    signal_df = signal_df.fillna(0.)
    signal_df['Counter'] = 0
    for i in all_tokens:
        if 'S{}'.format(i) in signal_df.columns:
            signal_df['Counter'] += signal_df['S{}'.format(i)]

    def expo(y, n_max=3):
        S = np.zeros(np.size(y))
        for i in range(np.size(y)):
            if y[i] > n_max:
                S[i] = 1 / y[i]
            elif y[i] > 0:
                S[i] = 1. / n_max
            else:
                S[i] = 0
        return S

    n_max = int(len(all_tokens) / 2.) + 1
    signal_df['expo'] = expo(signal_df['Counter'].values, n_max=n_max)

    for me_tok in all_tokens:
        if not 'S{}'.format(me_tok) in signal_df.columns:
            signal_df[f'S{me_tok}'] = 0.

    for me_tok in all_tokens:
        signal_df[f'SE{me_tok}'] = signal_df[f'S{me_tok}'] * signal_df['expo']

    for i in all_tokens:
        signal_df[f'S{lo_sig_suffix}{i}'] = signal_df[f'SE{i}'].shift(1)
        signal_df[f'SRAW{lo_sig_suffix}{i}'] = signal_df[f'S{i}'].shift(1)


    signal_df[f'total_expo'] = 0.
    for me_tok in all_tokens:
        signal_df[f'total_expo'] = signal_df[f'total_expo'] + signal_df[f'S{lo_sig_suffix}{me_tok}']

    fin_df = signal_df.copy()
    kpi_df = None
    if compute_lo_strat:
        def compute_return(row, tokens=[]):
            total_return = 0.
            for me_tok in tokens:
                total_return = total_return + row[f'return_{me_tok}'] * row[f'S{lo_sig_suffix}{me_tok}']
            return total_return

        comp_ret = lambda x: compute_return(x, tokens=all_tokens)
        fin_df['TR'] = fin_df.apply(comp_ret, axis=1)
        fin_df['TR'] = fin_df['TR'].fillna(0.)
        me_strat = 'strat'
        fin_df[me_strat] = np.cumprod(1 + fin_df['TR'].values)
        title = 'BTC_weekly_lo'
        if plot_html:
            fig = realtime_plotting_utility.plot_multiple_time_series(
                data_df=fin_df[[me_strat]],
                logy=True, split=False,
                put_on_same_scale=False,
                title=title)
            fig.show()
            fig = realtime_plotting_utility.plot_multiple_time_series(
                data_df=fin_df[[me_strat]],
                logy=False, split=False,
                put_on_same_scale=False,
                title=title)
            fig.show()

        backtest_df = fin_df[['strat']].copy()

        strat_data_df = backtest_df[['strat']].copy()
        from cryptotoolbox.analyzer import market

        # strat_data_df = strat_data_df[strat_data_df.index >= '2021-02-01'].copy()
        ma = market.MarketAnalyzer(strat_data_df, hourlyze=True)

        print('computing kpis')
        kpi_df = ma.get_kpi().T
        kpi_df = kpi_df.dropna()
        kpi_df = kpi_df[~np.isnan(kpi_df.sharpe)]
        print(kpi_df.head())


        if whole_kpis:
            backtest_df.columns = ['strat']
            riskmetrics.compute_plot_excel_kpis_meterics_metrics(backtest_df, title,
                                                                 local_root_directory,
                                                                 plot_html=True,
                                                                 write_file=True)
    return fin_df.copy(), kpi_df

def combine_weekly_lo_sigs(lo_df = None, rsilo_df = None, core_tokens=None, extra_tokens=None, plot_html=True):
    daily_rsi_lo_df = riskmetrics.filter_daily(rsilo_df.copy())
    lo_close_colums = [f'close_{tok}' for tok in core_tokens + extra_tokens]
    rsilo_close_colums = [f'close_{tok}' for tok in core_tokens]
    lo_raw_sigs_colums = [f'SRAWLO{tok}' for tok in core_tokens + extra_tokens]
    rsilo_raw_sigs_columns = [f'SRSILO{tok}' for tok in core_tokens]
#    merged_sig_df = pd.merge(lo_df[lo_close_colums+lo_raw_sigs_colums].copy(), daily_rsi_lo_df[rsilo_close_colums+rsilo_raw_sigs_columns].copy(), right_index=True, left_index=True)
    merged_sig_df = pd.merge(lo_df[lo_close_colums + lo_raw_sigs_colums + ['rebalance']].copy(),daily_rsi_lo_df[rsilo_raw_sigs_columns].copy(), right_index=True,left_index=True)

    def mix_lo_rsilo(row, core_tokens=None, extra_tokens=None):
        new_signals = {}
        total_core_expo = 0
        for token in core_tokens:
            if row[f'SRAWLO{token}'] > 0. and row[f'SRSILO{token}'] > 0.:
                new_signals[f'SMIX{token}'] = (row[f'SRAWLO{token}'] + row[f'SRSILO{token}']) / 2.
                total_core_expo = total_core_expo + (row[f'SRAWLO{token}'] + row[f'SRSILO{token}']) / 2.
            else:
                new_signals[f'SMIX{token}'] = 0.
            # new_signals[f'SMIX{token}'] = row[f'SRAWLO{token}']

        for token in extra_tokens:
            if total_core_expo > 0.:
                new_signals[f'SMIX{token}'] = row[f'SRAWLO{token}']
            else:
                new_signals[f'SMIX{token}'] = 0

        return new_signals

    go_mixer = lambda x: mix_lo_rsilo(x, core_tokens=core_tokens, extra_tokens=extra_tokens)
    final_lo_sig = merged_sig_df.apply(go_mixer, axis=1)
    final_lo_sig_df = pd.DataFrame().from_records(final_lo_sig.values)
    final_lo_sig_df.index = final_lo_sig.index
    merged_sig_df = pd.merge(merged_sig_df.copy(), final_lo_sig_df.copy(), left_index=True, right_index=True)

    all_tokens = core_tokens + extra_tokens
    n_max = int(len(all_tokens) / 2.) + 1

    def get_expo(row, n_max=None, all_tokens=None):
        signals = [f'SMIX{tok}' for tok in core_tokens + extra_tokens]
        total_sig = 0
        for sig in signals:
            total_sig = total_sig + row[sig]
        expo = 0.
        if total_sig > n_max:
            expo = 1. / total_sig
        elif total_sig > 0.:
            expo = 1. / n_max
        else:
            expo = 0.
        return expo

    go_get_expo = lambda x: get_expo(x, n_max=n_max, all_tokens=all_tokens)

    merged_sig_df['expo'] = merged_sig_df.apply(go_get_expo, axis=1)

    for tok in all_tokens:
        merged_sig_df[f'return_{tok}'] = merged_sig_df[f'close_{tok}'].pct_change()
        merged_sig_df[f'return_{tok}'] = merged_sig_df[f'return_{tok}'].fillna(0.)
        merged_sig_df[f'return_{tok}'] = merged_sig_df[f'return_{tok}'].replace([np.inf], 0)

    new_merged_sig_df = merged_sig_df.dropna()

    def compute_strat_perf(row, all_tokens=None):
        global_return = 0.
        expo = row['expo']
        for tok in all_tokens:
            global_return = global_return + row[f'return_{tok}'] * row[f'SMIX{tok}'] * expo
        return global_return

    go_comp = lambda x: compute_strat_perf(x, all_tokens=all_tokens)
    new_merged_sig_df['strat_return'] = new_merged_sig_df.apply(go_comp, axis=1)

    new_merged_sig_df['strat'] = np.cumprod(1. + new_merged_sig_df['strat_return'].values)

    if plot_html:
        title = 'Mix RSI/LO Weekly Strategy'
        dollar_df = new_merged_sig_df[['strat']].copy()
        new_names = {'strat': 'Absolute Return Weekly LO Strategy'}
        dollar_df = dollar_df.rename(columns=new_names)
        fig = realtime_plotting_utility.plot_dollar_multiple_time_series(data_df=dollar_df,
                                                                         logy=True, split=False,
                                                                         put_on_same_scale=False,
                                                                         title=title)
        fig.show()
        fig = realtime_plotting_utility.plot_dollar_multiple_time_series(data_df=dollar_df,
                                                                         logy=False, split=False,
                                                                         put_on_same_scale=False,
                                                                         title=title)
        fig.show()
    return new_merged_sig_df


def combine_daily_lo_sigs(lo_df = None, rsilo_df = None, core_tokens=None, extra_tokens=None, plot_html=True):
    daily_rsi_lo_df = riskmetrics.filter_daily(rsilo_df.copy())
    lo_close_colums = [f'close_{tok}' for tok in core_tokens + extra_tokens]
    rsilo_close_colums = [f'close_{tok}' for tok in core_tokens]
    lo_raw_sigs_colums = [f'SRAWLO{tok}' for tok in core_tokens + extra_tokens]
    rsilo_raw_sigs_columns = [f'SRSILO{tok}' for tok in core_tokens]
#    merged_sig_df = pd.merge(lo_df[lo_close_colums+lo_raw_sigs_colums].copy(), daily_rsi_lo_df[rsilo_close_colums+rsilo_raw_sigs_columns].copy(), right_index=True, left_index=True)
    merged_sig_df = pd.merge(lo_df[lo_close_colums + lo_raw_sigs_colums + ['rebalance']].copy(),daily_rsi_lo_df[rsilo_raw_sigs_columns].copy(), right_index=True,left_index=True)

    def mix_lo_rsilo(row, core_tokens=None, extra_tokens=None):
        new_signals = {}
        total_core_expo = 0
        for token in core_tokens:
            if row[f'SRAWLO{token}'] > 0. and row[f'SRSILO{token}'] > 0.:
                new_signals[f'SMIX{token}'] = (row[f'SRAWLO{token}'] + row[f'SRSILO{token}']) / 2.
                total_core_expo = total_core_expo + (row[f'SRAWLO{token}'] + row[f'SRSILO{token}']) / 2.
            else:
                new_signals[f'SMIX{token}'] = 0.
            # new_signals[f'SMIX{token}'] = row[f'SRAWLO{token}']

        for token in extra_tokens:
            if total_core_expo > 0.:
                new_signals[f'SMIX{token}'] = row[f'SRAWLO{token}']
            else:
                new_signals[f'SMIX{token}'] = 0

        return new_signals

    go_mixer = lambda x: mix_lo_rsilo(x, core_tokens=core_tokens, extra_tokens=extra_tokens)
    final_lo_sig = merged_sig_df.apply(go_mixer, axis=1)
    final_lo_sig_df = pd.DataFrame().from_records(final_lo_sig.values)
    final_lo_sig_df.index = final_lo_sig.index
    merged_sig_df = pd.merge(merged_sig_df.copy(), final_lo_sig_df.copy(), left_index=True, right_index=True)

    all_tokens = core_tokens + extra_tokens
    n_max = int(len(all_tokens) / 2.) + 1

    def get_expo(row, n_max=None, all_tokens=None):
        signals = [f'SMIX{tok}' for tok in core_tokens + extra_tokens]
        total_sig = 0
        for sig in signals:
            total_sig = total_sig + row[sig]
        expo = 0.
        if total_sig > n_max:
            expo = 1. / total_sig
        elif total_sig > 0.:
            expo = 1. / n_max
        else:
            expo = 0.
        return expo

    go_get_expo = lambda x: get_expo(x, n_max=n_max, all_tokens=all_tokens)

    merged_sig_df['expo'] = merged_sig_df.apply(go_get_expo, axis=1)

    for tok in all_tokens:
        merged_sig_df[f'return_{tok}'] = merged_sig_df[f'close_{tok}'].pct_change()
        merged_sig_df[f'return_{tok}'] = merged_sig_df[f'return_{tok}'].fillna(0.)
        merged_sig_df[f'return_{tok}'] = merged_sig_df[f'return_{tok}'].replace([np.inf], 0)

    new_merged_sig_df = merged_sig_df.dropna()

    def compute_strat_perf(row, all_tokens=None):
        global_return = 0.
        expo = row['expo']
        for tok in all_tokens:
            global_return = global_return + row[f'return_{tok}'] * row[f'SMIX{tok}'] * expo
        return global_return

    go_comp = lambda x: compute_strat_perf(x, all_tokens=all_tokens)
    new_merged_sig_df['strat_return'] = new_merged_sig_df.apply(go_comp, axis=1)

    new_merged_sig_df['strat'] = np.cumprod(1. + new_merged_sig_df['strat_return'].values)

    if plot_html:
        title = 'Mix RSI/LO Daily Strategy'
        dollar_df = new_merged_sig_df[['strat']].copy()
        new_names = {'strat': 'Absolute Return Daily LO Strategy'}
        dollar_df = dollar_df.rename(columns=new_names)
        fig = realtime_plotting_utility.plot_dollar_multiple_time_series(data_df=dollar_df,
                                                                         logy=True, split=False,
                                                                         put_on_same_scale=False,
                                                                         title=title)
        fig.show()
        fig = realtime_plotting_utility.plot_dollar_multiple_time_series(data_df=dollar_df,
                                                                         logy=False, split=False,
                                                                         put_on_same_scale=False,
                                                                         title=title)
        fig.show()
    return new_merged_sig_df
