from portfoliotools.screener.utility.util import memoize, getStockSectorMap, getHistoricStockPrices, getHistoricalIndexData
import datetime as datetime
import nsepython
import pandas as pd
from copy import deepcopy
import numpy as np
from scipy.optimize import minimize
from portfoliotools.analytics.constant import *

@memoize
def getPriceHistory(ticker, tickerType = 'EQ', start_date = None, end_date = None, period = None):
    '''
        Method to get price history for a given ticker. 
        ticker: ticker symbol
        tickerType = 'EQ' for Stock, 'IN' for indexes,
        start_date = start date of type datetime.datetime
        end_date = end date of type datetime.datetime
        period = In case start date not given, period is used for calculating no. of days
    '''
    if period is None: period = 365
    if end_date is None: end_date = datetime.datetime.today()
    if start_date is None: start_date = end_date + datetime.timedelta( days = -1* period )
    
    if tickerType == 'EQ':
        period = (end_date - start_date).days
        data = getHistoricStockPrices(ticker, end_date=end_date, days = period)
    elif tickerType == 'IN':
        data = getHistoricalIndexData(ticker, start_date=start_date, end_date=end_date)
        data.index = [datetime.datetime.strptime(date.strftime('%Y-%m-%d'),'%Y-%m-%d') for date in data.index]
        
    else:
        return 'Please select tickerType as EQ or IN'
    return data

class PortfolioAnalysis:
    
    _instrument_details = {}
    
    def __init__(self, portfolio_constituents, start_date = None, end_date = None, period = None, saa_min_allocation = 0, saa_max_allocation = .08):
        self.constituents = portfolio_constituents
        self.start_date = start_date
        self.end_date = end_date
        self.period = period
        self.saa_min_allocation = saa_min_allocation
        self.saa_max_allocation = saa_max_allocation
        self.stock_sector_map = self.__getStockSectorMap()
        
        self.__fetch_instrument_details()
        
    @memoize
    def __getStockSectorMap(self, to_dict = True):
        
        df = getStockSectorMap()
        df = df[['Symbol', 'Company Name', 'Industry', 'ISIN Code']]
        if to_dict:
            info = dict()
            for stock in df.to_dict(orient = 'records'):
                stock['Benchmark'] = SECTOR_BM_DEFAULT[stock['Industry']]
                info[stock['Symbol']] = stock
            return info
        return df
    
    def __fetch_instrument_details(self):
        tickers = self.constituents.keys()
        benchmarks = list(set([info['Benchmark'] for ticker, info in self.stock_sector_map.items() if ticker in self.constituents.keys()]))
        benchmarks = list(SECTOR_BM_DEFAULT.values()) + ['NIFTY']

        def getOtherDetails(historical_prices):
            other_details = {}
            other_details['return'] = self.__calc_instrument_return(historical_prices)
            other_details['risk'] = self.__calc_instrument_risk(historical_prices)
            other_details['sharpe_ratio'] = self.__calc_instrument_sharp_ratio(historical_prices)
            return other_details
            
        
        for instrument in tickers:
            
            historical_prices = self.__get_ticker_price_history(instrument)['Adj Close']
            temp = getOtherDetails(historical_prices)
            temp['historical_price'] = historical_prices
            
            self._instrument_details[instrument] = temp
            
        for instrument in benchmarks:
            temp = {}
            historical_prices = self.__get_index_price_history(instrument)['Adj Close']
            temp = getOtherDetails(historical_prices)
            temp['historical_price'] = historical_prices
            
            self._instrument_details[instrument] = temp
            
    @memoize
    def __get_ticker_price_history(self, ticker, start_date = None, end_date = None, period = None):
        
        if start_date is None: start_date = self.start_date
        if end_date is None: end_date = self.end_date
        if period is None: period = self.period
        
        stockPrices = getPriceHistory(ticker, tickerType = 'EQ', start_date = start_date, end_date = end_date, period = period)
        return stockPrices
    
    @memoize
    def __get_index_price_history(self, index, start_date = None, end_date = None, period = None):
        
        if start_date is None: start_date = self.start_date
        if end_date is None: end_date = self.end_date
        if period is None: period = self.period
        
        stockPrices = getPriceHistory(index, tickerType = 'IN', start_date = start_date, end_date = end_date, period = period)
        return stockPrices
    
    @memoize
    def __calc_return_series(self, historical_price):
        return np.log(historical_price/historical_price.shift(1)).dropna()
    
    @memoize
    def __calc_instrument_return(self, historical_price):
        return np.round(self.__calc_return_series(historical_price).mean()*252*100,2)
    
    @memoize
    def __calc_portfolio_returns(self, historical_prices, weights):
        ret = self.__calc_return_series(historical_prices)
        return np.round(np.sum(ret.values.mean()*weights)*252*100, 2)
    
    @memoize
    def __calc_instrument_risk(self, historical_price):
        return np.round(np.log(historical_price/historical_price.shift(1)).std()*np.sqrt(252)*100,2)
    
    @memoize
    def __calc_portfolio_risk(self, historical_prices, weights):
        
        cov_matrix = self.__calc_covariance_matrix(historical_prices)
        return np.round(np.sqrt(np.dot(weights.T, np.dot(cov_matrix*252, weights)))*100, 2)
    
    @memoize
    def __calc_instrument_sharp_ratio(self, historical_price):
        return np.round(self.__calc_instrument_return(historical_price)/self.__calc_instrument_risk(historical_price), 2)

    @memoize
    def __calc_portfolio_sharp_ratio(self, historical_prices, weights):
        return np.round(self.__calc_portfolio_returns(historical_prices, weights)/self.__calc_portfolio_risk(historical_prices, weights), 2)

    @memoize
    def __calc_covariance_matrix(self, historical_prices):
        ret = self.__calc_return_series(historical_prices)
        return ret.cov()
    
    @memoize
    def __get_portfolio_constituents(self):
        data = self.getDetails()[['Symbol', 'Benchmark', 'Allocation']]
        data['Allocation'] = data['Allocation']*100
        return data
    
    
    def _get_efficient_frontier(self, historic_prices, saa_min_allocation = None, saa_max_allocation = None):
        
        def _get_ret_vol_sr(weights):
            weights = np.array(weights)
            ret = np.sum(log_ret.mean() * weights) * 252*100
            vol = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov()*252, weights)))*100
            sr = ret/vol
            return np.array([ret, vol, sr])

        def _neg_sharpe(weights):
        # the number 2 is the sharpe ratio index from the get_ret_vol_sr
            return _get_ret_vol_sr(weights)[2] * -1

        def _check_sum(weights):
            #return 0 if sum of the weights is 1
            return np.sum(weights)-1

        def _minimize_volatility(weights):
            return _get_ret_vol_sr(weights)[1]
        
        if saa_min_allocation is None:
            saa_min_allocation = self.saa_min_allocation
        
        if saa_max_allocation is None:
            saa_max_allocation = self.saa_max_allocation

        historic_prices.dropna(inplace = True)
        tickers     = historic_prices.columns.tolist()
        log_ret    = np.log(historic_prices/historic_prices.shift(1))

        cons       = {'type' : 'eq', 'fun' : _check_sum}
        bounds     = tuple([(saa_min_allocation,saa_max_allocation)]*len(tickers))
        init_guess = [1/len(tickers)]*len(tickers)

        opt_results = minimize(_neg_sharpe, init_guess, method='SLSQP', bounds = bounds, constraints=cons)
        market_port = {}
        market_port['Allocation'] = {k:round(v*100,2) for k,v in zip(tickers, np.round(opt_results.x, 4))}
        performance = {}
        performance['Return'], performance['Risk'], performance['Sharpe Ratio'] = np.round(_get_ret_vol_sr(opt_results.x),2)
        market_port['Performance'] = performance
        return market_port
    
    @memoize
    def _get_saa_portfolio(self):
        security_price_matrix = pd.DataFrame()
        for ticker in self.constituents.keys():
            security_price_matrix[ticker] = self._instrument_details[ticker]['historical_price']
        
        market_portfolio = self._get_efficient_frontier(security_price_matrix)
        return market_portfolio
    
    @memoize
    def _get_saa_benchmark(self):
        benchmark_price_matrix = pd.DataFrame()
        for ticker in list(SECTOR_BM_DEFAULT.values()) + ['NIFTY']:
            #benchmark = self.stock_sector_map[ticker]['Benchmark']
            benchmark_price_matrix[ticker] = self._instrument_details[ticker]['historical_price']
            
        market_portfolio = self._get_efficient_frontier(benchmark_price_matrix, 0, .16)
        return market_portfolio
            
    def getPortfolioAllocations(self):
        portfolio = self._get_saa_portfolio()
        portfolio_alloc = pd.DataFrame([portfolio['Allocation']]).T
        portfolio_alloc.columns = [SAA_ASSET_ALLOCATION]
        portfolio_alloc.reset_index(inplace = True)
        portfolio_alloc.rename(columns = {'index' : 'Symbol'}, inplace = True)

        benchmark = self._get_saa_benchmark()
        benchmark_alloc = pd.DataFrame([benchmark['Allocation']]).T
        benchmark_alloc.columns = [SAA_BENCHMARK_ALLOCATION]
        benchmark_alloc.reset_index(inplace = True)
        benchmark_alloc.rename(columns = {'index' : 'Benchmark'}, inplace = True)

        result = self.getDetails()[['Symbol', 'Benchmark', 'Allocation']]
        result['Allocation'] = result['Allocation']*100
        result.rename(columns = {'Allocation': ASSET_ALLOCATION}, inplace = True)
        result[BENCHMARK_ALLOCATION] = result[ASSET_ALLOCATION]

        result = result.merge(portfolio_alloc, left_on = 'Symbol', right_on = 'Symbol', how='inner', right_index=False)
        result = result.merge(benchmark_alloc, left_on = 'Benchmark', right_on = 'Benchmark', how='outer', left_index=False)
        result = result[['Benchmark', 'Symbol', ASSET_ALLOCATION, BENCHMARK_ALLOCATION, SAA_ASSET_ALLOCATION, SAA_BENCHMARK_ALLOCATION]].fillna('')
        group = result.groupby('Benchmark').agg({
            BENCHMARK_ALLOCATION: sum,
            SAA_BENCHMARK_ALLOCATION: max
        })
        group.reset_index(inplace = True)
        group['Symbol'] = group['Benchmark']
        result = pd.concat([group, result[['Benchmark', 'Symbol', ASSET_ALLOCATION, SAA_ASSET_ALLOCATION]]]).fillna('')
        result = result.groupby(['Benchmark', 'Symbol']).sum()
        result.reset_index(inplace = True)
        result.replace('', np.NaN, inplace=True)
        result.dropna(how='all', subset=['Symbol'], inplace=True)
        result.fillna(0, inplace = True)

        return result
    
    def getDetails(self):
        details = []
        for ticker, allocation in self.constituents.items():
            temp = self.stock_sector_map.get(ticker, 'NIFTY')
            temp['Allocation'] = allocation
            temp['Return'] = self._instrument_details[ticker]['return']
            temp['Risk'] = self._instrument_details[ticker]['risk']
            temp['Sharpe Ratio'] = self._instrument_details[ticker]['sharpe_ratio']
            temp['Benchmark Return'] = self._instrument_details[temp['Benchmark']]['return']
            temp['Benchmark Risk'] = self._instrument_details[temp['Benchmark']]['risk']
            temp['Benchmark Sharpe Ratio'] = self._instrument_details[temp['Benchmark']]['sharpe_ratio']
            details.append(temp)
        
        return pd.DataFrame(details)
    
    
    def getPortfolioPerformance(self):
        
        result = {}
        
        security_price_matrix = pd.DataFrame()
        for ticker in self.constituents.keys():
            security_price_matrix[ticker] = self._instrument_details[ticker]['historical_price']
            
        benchmark_price_matrix = pd.DataFrame()
        for ticker in self.constituents.keys():
            benchmark = self.stock_sector_map[ticker]['Benchmark']
            benchmark_price_matrix[ticker] = self._instrument_details[benchmark]['historical_price']
        
        weights = np.array(list(self.constituents.values()))
        
        asset_return = self.__calc_portfolio_returns(security_price_matrix, weights)
        asset_risk = self.__calc_portfolio_risk(security_price_matrix, weights)
        asset_sharpe_ratio = self.__calc_portfolio_sharp_ratio(security_price_matrix, weights)
        
        benchmark_return = self.__calc_portfolio_returns(benchmark_price_matrix, weights)
        benchmark_risk = self.__calc_portfolio_risk(benchmark_price_matrix, weights)
        benchmark_sharpe_ratio = self.__calc_portfolio_sharp_ratio(benchmark_price_matrix, weights)
        
        result['Asset'] = {
            'Return': asset_return,
            'Risk': asset_risk,
            'Sharpe Ratio': asset_sharpe_ratio
        }
        result['Benchmark'] = {
            'Return': benchmark_return,
            'Risk': benchmark_risk,
            'Sharpe Ratio': benchmark_sharpe_ratio
        }
        result['SAA Asset'] = self._get_saa_portfolio()['Performance']
        result['SAA Benchmark'] = self._get_saa_benchmark()['Performance']
        
        result = pd.DataFrame(result)
        return result
    