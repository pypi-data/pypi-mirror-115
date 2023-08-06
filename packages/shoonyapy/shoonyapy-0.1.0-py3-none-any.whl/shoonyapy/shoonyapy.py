# -*- coding:utf-8 -*-

import json
from base64 import b64encode
from datetime import datetime as dt
from datetime import timedelta as td
from hashlib import sha512
from time import sleep

import getmac
import pandas as pd
import numpy as np
import requests
import logging
import pytz

import dateutil

from collections import namedtuple

pd.set_option('display.width', 1500)
pd.set_option('display.max_columns', 75)
# pd.set_option('display.max_rows', 1500)


logger = logging.getLogger(__name__)


class DataApi(object):

    _candletype = {1: 1, 2: 1, 3: 1, 5: 1, 10: 1, 15: 1,
                   30: 1, 45: 1, '1H': 2, '2H': 2, '3H': 2, '4H': 2, '1D': 3, 'D': 3, 'W': 3, 'M': 3}

    _data_duration = {1: 1, 2: 2, 3: 3, 5: 5, 10: 10, 15: 15,
                      30: 30, 45: 45, '1H': None, '2H': 2, '3H': 2, '4H': 2, '1D': None, 'D': None, 'W': None, 'M': None}

    def __init__(self):
        self._headers = {
            'Content-Type': 'application/json',
            'Connection': 'Keep-Alive',
            'Accept': 'application/json'
        }

    def ltp(self, instrument):
        url = 'https://shoonyabrd.finvasia.com/DataPub/api/SData/LiveFeed'
        exch = {
            'NSE': 1, 'BSE': 2, 'MCX': 3
        }

        if instrument.exchange == 'NSE':
            if instrument.segment == 'E':
                seg = 1
            elif instrument.segment == 'D':
                seg = 2
            elif instrument.segment == 'C':
                seg = 3
        if instrument.exchange == 'BSE':
            if instrument.segment == 'E':
                seg = 4
            elif instrument.segment == 'D':
                seg = 6
            elif instrument.segment == 'C':
                seg = 7
        if instrument.exchange == 'MCX':
            if instrument.segment == 'M':
                seg = 5

        d = {"Seg": seg, "ScripIdLst": [
            f"{instrument.token}"], "Exch": exch[instrument.exchange], "SecIdxCode": "-1"}
        payload = {
            "Count": "50",
            "Data": str(d),
            "DoCompress": False,
            "RequestCode": 131,
            "Reserved": "",
            "Source": "W",
            "UserId": "",
            "UserType": "C"
        }
        # [{"Exch":"MCX","Seg":"M","SId":229420,"Vol":14821,"ltp":4810.0,"Chg":20.0,"PChg":0.42}]

        r = requests.post(url, json=payload, headers=self._headers)
        data = r.json()[0]

        Instrument = namedtuple('Instrument', [
                                'exchange', 'segment', 'symbol', 'token', 'volume', 'change', 'per_change', 'ltp'])
        instrument = Instrument(data['Exch'], data['Seg'], instrument.symbol,
                                data['SId'], data['Vol'], data['Chg'], data['PChg'], data['ltp'])
        print(instrument)
        return instrument

    def get_instrument_by_token_or_security_id(self, token_or_security_id):
        Instrument = namedtuple('Instrument', ['exchange', 'segment', 'token', 'symbol',
                                               'name', 'expiry', 'lot_size', 'upper_ckt', 'lower_ckt', 'search_str'])
        instrument = None
        url = 'https://data.rupeetracker.in/solr/scrip/select'
        query = {
            'wt': 'json',
            'indent': 'true',
            'q': f'((Sid_s:{token_or_security_id}))',
            'rows': 10,
            'sort': 'ExpDate_s asc,volume_i desc,Sid_s asc'
        }
        r = requests.get(url, params=query, headers=self._headers)
        stock = r.json()['response']['docs'][0]
        # print(stock)
        lot_size = stock['NSE_Regular_lot_i'] * stock['Mcx_Multiplier_i']
        instrument = Instrument(stock['_Exch_s'], stock['Seg_s'], stock['Sid_s'], stock['ExchTradingSymbol_s'],
                                stock['CompName_t'], stock['ExpDate_s'], lot_size, stock['Upper_ckt_d'], stock['LoweCkt_d'], stock['SearcTerm_s'])
        print(instrument)
        return instrument

    def get_instrument_by_exchange_symbol(self, exchange, symbol):
        Instrument = namedtuple('Instrument', ['exchange', 'segment', 'token', 'symbol',
                                               'name', 'expiry', 'lot_size', 'upper_ckt', 'lower_ckt', 'search_str'])
        instrument = None
        url = 'https://data.rupeetracker.in/solr/scrip/select'
        query = {
            'wt': 'json',
            'indent': 'true',
            'q': f'((_Exch_s:{exchange} AND Sym_t:{symbol}) OR (ExchTradingSymbol_s:{symbol}))',
            'rows': 10,
            'sort': 'ExpDate_s asc,volume_i desc,Sid_s asc'
        }
        r = requests.get(url, params=query, headers=self._headers)
        stock = r.json()['response']['docs'][0]
        # print(stock)
        lot_size = stock['NSE_Regular_lot_i'] * stock['Mcx_Multiplier_i']
        instrument = Instrument(stock['_Exch_s'], stock['Seg_s'], stock['Sid_s'], stock['ExchTradingSymbol_s'],
                                stock['CompName_t'], stock['ExpDate_s'], lot_size, stock['Upper_ckt_d'], stock['LoweCkt_d'], stock['SearcTerm_s'])
        print(instrument)
        return instrument

    def get_1minute_bars(self, instrument, bars=100):
        url = 'https://shoonyabrd.finvasia.com/TickPub/api/Tick/LiveFeed'
        d = {"Exch": instrument.exchange, "Seg": instrument.segment, "ScripId": instrument.token,
             "FromDate": 1, "ToDate": 30, "Time": 1}
        payload = {
            "Count": 10, "Data": str(d),
            "DoCompress": False, "RequestCode": 800, "Reserved": "FVSA147", "Source": "W", "UserId": "", "UserType": "C"
        }

        r = requests.post(url, json=payload, headers=self._headers)
        data = r.json()
        # print(json.dumps(data, indent=1))
        df = pd.DataFrame(data, index=None)
        df['datetime'] = pd.to_datetime(df['Start_Time'])
        df['open'] = df['Open']
        df['high'] = df['High']
        df['low'] = df['Low']
        df['close'] = df['Close']
        df['volume'] = df['Volume']
        # df['oi'] = df['OI']
        # df = df[['datetime', 'open', 'high', 'low', 'close', 'volume', 'oi']]
        df = df[['datetime', 'open', 'high', 'low', 'close', 'volume']]
        df = df.replace(0, np.nan)
        df = df.dropna()
        df.set_index('datetime', inplace=True)
        print(df.tail(bars))
        return df.tail(bars)

    def _format_candles(self, data, interval):
        records = data['data']['candles']
        df = pd.DataFrame(records, columns=[
            'datetime', 'open', 'high', 'low', 'close', 'volume'])  # , index=0)
        df['datetime'] = df['datetime'].apply(
            pd.Timestamp, unit='s', tzinfo=pytz.timezone('Asia/Kolkata'))

        df[['open', 'high', 'low', 'close']] = df[[
            'open', 'high', 'low', 'close']].astype(float)
        df['volume'] = df['volume'].astype(int)
        df.set_index('datetime', inplace=True)
        if interval in ['2H', '3H', '4H', 'W', 'M']:
            if interval == 'W':
                interval = 'W-Mon'
            df = df.resample(interval, origin='start').agg({'open': 'first', 'high': 'max',
                                                            'low': 'min', 'close': 'last', 'volume': 'sum'}).dropna()
        df.index = df.index.astype(str).str[:-6]
        return df

    def history(self, instrument, start_time=dt.today() - td(days=2), end_time=dt.now(), interval=1, is_index=False):
        exchange = instrument.exchange
        start_time = int(start_time.timestamp())
        end_time = int(end_time.timestamp())
        if is_index:
            exchange = 'NSE_INDICES'

        candle_type = self._candletype[interval]

        data_duration = self._data_duration[interval]

        PARAMS = {
            'exchange': exchange,
            'token': instrument.token,
            'name': instrument.symbol,
            'candletype': candle_type,
            'starttime': start_time,
            'endtime': end_time,
            'type': 'all'
        }
        if data_duration is not None:
            PARAMS['data_duration'] = data_duration

        r = requests.get(
            'https://ant.aliceblueonline.com/api/v1/charts/tdv', params=PARAMS, headers=self._headers)
        data = r.json()
        return self._format_candles(data, interval)


class ShoonyaApi(object):

    # Constants

    # Product Type

    PRODUCT_CNC = 'C'
    PRODUCT_MARGIN = 'M'  # USED FOR OPTIONS HEDGING
    PRODUCT_INTRADAY = 'I'
    PRODUCT_NORMAL = 'H'
    PRODUCT_MTF = 'F'
    PRODUCT_BO = 'B'
    PRODUCT_CO = 'V'

    # product
    # C CNC
    # M Margin
    # I Intraday
    # H Normal – Hybrid
    # F MTF
    # B BO – Bracket Order
    # V CO – Cover Order

    EXCHANGE_NSE = 'NSE'
    EXCHANGE_BSE = 'BSE'
    EXCHANGE_MCX = 'MCX'

    TRANSACTION_TYPE_BUY = 'B'
    TRANSACTION_TYPE_SELL = 'S'

    # txn_type
    # B Buy
    # S Sell

    ORDER_TYPE_LIMIT = 'LMT'
    ORDER_TYPE_MARKET = 'MKT'
    ORDER_TYPE_STOPLOSS = 'SL'
    ORDER_TYPE_STOPLOSS_MARKET = 'SLM'

    # order_type
    # LMT Limit
    # MKT Market
    # SL Stoploss
    # SLM Stoploss-Market

    VALIDITY_IMMEDIATE_OR_CANCEL = 'IOC'
    VALIDITY_DAY = 'DAY'
    VALIDITY_GOOD_TILL_CANCEL = 'GTC'
    VALIDITY_GOOD_TILL_DATE = 'GTD'

    # IOC Immediate or cancel
    # DAY Intraday
    # GTC Good till cancel
    # GTD Good till Date

    SEGMENT_EQUITY = 'E'
    SEGMENT_DERIVATIVE = 'D'
    SEGMENT_CURRENCY = 'C'
    SEGMENT_COMMODITY = 'M'

    # E Equity
    # D Derivative
    # C Currency
    # M Commodity

    # source
    # M Mobile Web
    # W Website
    # N Android
    # I IOS
    # O Operator Work Station
    # H Admin

    # mkt_type NL/OL/AU/SP/A1/A2

    MARKET_TYPE_NL = 'NL'
    MARKET_TYPE_OL = 'OL'
    MARKET_TYPE_AU = 'AU'
    MARKET_TYPE_SP = 'SP'
    MARKET_TYPE_A1 = 'A1'
    MARKET_TYPE_A2 = 'A2'
    MARKET_TYPE_ALL = ''

    # mkt_status OPEN/CLOSE/PREOPEN/POSTCLOSE

    MARKET_STATUS_PREOPEN = 'PREOPEN'
    MARKET_STATUS_OPEN = 'OPEN'
    MARKET_STATUS_PRECLOSE = 'PRECLOSE'
    MARKET_STATUS_CLOSE = 'CLOSE'

    _config = {
        'host': 'http://rapishoonya.finvasia.com:8080/RupeeApi',
        'paths': {
            'auth': '/Authenticate',
            'basic_auth': '/PasswordAuth/BasicAuth',
            'holdings': '/HoldingDetails',
            'funds': '/FundLimit',
            'place_order': '/OrderEntry',
            'modify_order': '/OrderModify',
            'cancel_order': '/OrderCancel',
            'place_cover_order': '/CoOrderEntry',
            'modify_cover_order': '/CoOrderCancel',
            'exit_cover_order': '/CoOrderExit',
            'place_bracket_order': '/BoOrderEntry',
            'modify_bracket_order': '/BoOrderCancel',
            'exit_bracket_order': '/BoOrderExit',
            'orders': '/OrderBook',
            'order_history': '/OrderDetails',
            'trades': '/TradeBook',
            'trade_history': '/TradeDetails',
            'market_status': '/MarketStatus',
            'positions': '/NetPosition',
            'convert_to_delivery': '/ConvToDel'
        }
    }

    _segments = {
        'EQUITY': 'E',
        'FUTIDX': 'D',
        'OPTIDX': 'D',
        'FUTSTK': 'D',
        'OPTSTK': 'D',
        'FUTCOM': 'M',
        'OPTCUR': 'C',
        'FUTCUR': 'C',
    }

    def __init__(self, username, password, pan_or_dob, debug=False):

        self._client_id = username
        self._password = password
        self._pan_no = pan_or_dob  # dob =? dd-MM-yyyy format and pan => AXXXX1234Z
        self._token_id = ''
        self._session = requests.session()
        self.debug = debug

        config = self._config
        url = f"{config['host']}"
        try:
            requests.get(url, timeout=1)
        except requests.exceptions.ConnectionError:
            print(f"URL {url} not reachable. Please use during trading days only. Monday to Friday.")
            return

        self._payload = {
            'entity_id': self._client_id,
            'source': 'I',
            'token_id': self._token_id,
            'iv': '',
            'data': {}
        }

        self._headers = {
            'Content-Type': 'application/json',
            'Connection': 'Keep-Alive',
            'Accept': 'application/json',
            'User-Agent': 'python3-requests'
        }
        self._device_id = getmac.get_mac_address()
        self._authenticate()

    def get_hash(self, password, salt):
        import hashlib
        from base64 import b64encode
        bytes_password = password.encode('utf-8')
        bytes_salt = salt.encode('utf-8')
        for _ in range(1000):
            # if i < 10:
            #     print(b64encode(bytes_password).decode())

            b64pw = b64encode(bytes_password).decode()
            b64sa = b64encode(bytes_salt).decode()
            bytes_iteration = (b64pw + b64sa).encode('utf-8')
            bytes_password = hashlib.sha512(bytes_iteration).digest()

        # print(b64encode(bytes_password).decode())
        return b64encode(bytes_password).decode()

    def _authenticate(self):
        """ Authenticate to generate token id and salt """
        data = self._post_helper('auth')
        self._token_id = data['token_id']
        self._salt = data['salt']
        self._payload['token_id'] = self._token_id
        self._password_hash = self.get_hash(self._password, self._salt)
        d = {
            'device_id': self._device_id,
            'pan_no': self._pan_no,
            'pass': self._password_hash
        }
        self._update_payload(d)
        data = self._post_helper('basic_auth')
        if self.debug:
            logger.debug(f"Data: {data}")

    def _update_payload(self, data):
        self._payload['data'] = data
        if self.debug:
            logger.debug(f"Payload: {self._payload}")

    def _format_response(self, data):
        """Parse and format responses."""

        _list = None

        if type(data) == list:
            _list = data
        elif type(data) == dict:
            _list = [data]

        for item in _list:
            # Convert date time string to datetime object
            for field in ["order_date_time", "exch_order_time", "timestamp", "last_updated_time"]:
                if item.get(field) and len(item[field]) == 19:
                    item[field] = dateutil.parser.parse(item[field])

        return _list[0] if type(data) == dict else _list

    def positions(self):
        data = {
            'client_id': self._client_id
        }
        self._update_payload(data)
        data = self._post_helper('positions')
        # Index(['client_id', 'security_id', 'instrument', 'symbol', 'exchange', 'expiry_date', 'strike_price', 'opt_type',
        # 'tot_buy_qty', 'tot_buy_val', 'buy_avg', 'tot_sell_qty', 'tot_sell_val', 'sell_avg', 'net_qty', 'net_val', 'net_avg',
        # 'gross_qty', 'gross_val', 'segment', 'mkt_type', 'product', 'lot_size', 'last_traded_price', 'realised_profit', 'mtm',
        # 'rbi_reference_rate', 'cross_cur_flag', 'comm_multiplier', 'tot_buy_qty_cf', 'tot_sell_qty_cf', 'tot_buy_val_cf', 'tot_sell_val_cf',
        # 'tot_buy_qty_day', 'tot_buy_val_day', 'tot_sell_qty_day', 'tot_sell_val_day', 'isin', 'series', 'display_name', 'exchange_inst_name'], dtype='object')
        position_columns = ['exchange', 'symbol', 'security_id', 'net_qty', 'segment', 'product', 'realised_profit', 'mtm',
                            'tot_buy_qty', 'tot_sell_qty', 'instrument', 'lot_size', 'expiry_date', 'mkt_type', 'last_traded_price']
        df = pd.DataFrame(data, columns=position_columns)
        print(df)
        if self.debug:
            logger.debug(f"Data :: {df}")
        return df

    def holdings(self):
        data = {
            'client_id': self._client_id
        }
        self._update_payload(data)
        data = self._post_helper('holdings')
        holding_columns = ['nse_symbol', 'nse_security_id', 'bse_symbol',
                           'bse_security_id', 'exchange', 'quantity', 'utilized_quantity', 'total_quantity']
        df = pd.DataFrame(data, columns=holding_columns)
        print(df)
        if self.debug:
            logger.debug(f"Data :: {df}")
        return df

    def funds(self):
        data = {
            'client_id': self._client_id
        }
        self._update_payload(data)
        data = self._post_helper('funds')
        fund_columns = ['segment', 'limit_type', 'limit_sod', 'adhoc_limit', 'total_balance', 'available_balance', 'withdrawal_balance',
                        'amount_utilized', 'realized_profits', 'pay_out_amt', 'bank_clear_balance', 'bank_unclear_balance']
        df = pd.DataFrame(data, columns=fund_columns)
        print(df)
        if self.debug:
            logger.debug(f"Data :: {df}")
        return df

    def orders(self):
        data = {
            'client_id': self._client_id
        }
        self._update_payload(data)
        data = self._post_helper('orders')
        order_columns = ['order_no', 'status', 'exchange', 'symbol', 'security_id', 'order_type',
                         'product', 'txn_type', 'segment', 'price', 'quantity', 'instrument', 'order_date_time', 'exch_order_time']
        df = pd.DataFrame(data, columns=order_columns)
        print(df)
        if self.debug:
            logger.debug(f"Data :: {df}")
        return df
        #     Index(['client_id', 'order_date_time', 'last_updated_time', 'order_no', 'exchange', 'txn_type', 'segment', 'instrument', 'symbol', 'product',
        #    'product_name', 'status', 'quantity', 'remaining_quantity', 'price', 'trigger_price', 'order_type', 'disc_quantity', 'serial_no', 'security_id',
        #    'validity', 'lot_size', 'rem_qty_tot_qty', 'traded_qty', 'dq_qty_rem', 'exch_order_no', 'exch_order_time', 'reason_description', 'leg_no',
        #    'row_no', 'traded_price', 'avg_traded_price', 'pan_no', 'participant_type', 'mkt_pro_flag', 'mkt_pro_value', 'settlor', 'encash_flag',
        #    'mkt_type', 'algo_ord_no', 'trailing_sl_value', 'sl_abstick_value', 'pr_abstick_value', 'off_mkt_flag', 'child_leg_unq_id',
        #    'strike_price', 'expiry_date', 'opt_type', 'series', 'good_till_days_date', 'group_id', 'isin', 'display_name', 'exchange_inst_name',
        #    'error_code', 'source', 'placed_by', 'source_name', 'ref_ltp'], dtype='object')

    def trades(self):
        data = {
            'client_id': self._client_id
        }
        self._update_payload(data)
        data = self._post_helper('trades')

        trade_columns = ['trade_no', 'order_no', 'traded_price', 'trade_value', 'exchange', 'symbol',
                         'security_id', 'product', 'txn_type', 'order_type', 'segment', 'price', 'quantity', 'instrument', 'order_date_time', 'exch_order_time', 'exch_trade_time']

        df = pd.DataFrame(data, columns=trade_columns)
        print(df)
        if self.debug:
            logger.debug(f"Data :: {df}")
        return df
        #     Index(['client_id', 'order_date_time', 'exch_order_time', 'exch_trade_time', 'last_updated_time', 'order_no', 'exch_order_no',
        #    'exchange', 'txn_type', 'segment', 'order_type', 'symbol', 'product', 'product_name', 'quantity', 'traded_price', 'trade_value',
        #    'trade_no', 'security_id', 'row_no', 'pan_no', 'participant_type', 'mkt_pro_flag', 'mkt_pro_value', 'settlor', 'encash_flag', 'mkt_type',
        #    'strike_price', 'expiry_date', 'opt_type', 'instrument', 'lot_size', 'series', 'isin', 'display_name', 'exchange_inst_name', 'placed_by'], dtype='object')

    def _post_helper(self, name):
        config = self._config
        url = f"{config['host']}{config['paths'][name]}"
        try:
            response = self._session.post(
                url, json=self._payload, headers=self._headers)
        except Exception as ex:
            raise f'Exception Raised :: {ex}'

        if self.debug:
            logger.debug(
                f"Response: {response.status_code} {response.content}")

        if response.status_code == 200:
            json_data = response.json()
            # print(json_data)
            if json_data['status'] == 'success':
                return json_data['data']
            else:
                return [json.loads(response.text)]
        else:
            return json.loads(response.text)

    def place_bracket_order(self,
                            instrument,
                            txn_type,
                            order_type,
                            quantity,
                            price,
                            profit,
                            stoploss,
                            trigger=0.0,
                            trailing_stoploss=0.0):
        d = {
            'client_id': self._client_id,
            'txn_type': txn_type,
            'exchange': instrument.exchange,
            'segment': instrument.segment,
            'product': self.PRODUCT_BO,
            'security_id': instrument.token,
            'quantity': quantity,
            'validity': self.VALIDITY_DAY,
            'price': price,
            'order_type': order_type,
            'trigger_price': trigger,
            'off_mkt_flag': False,  # AMO After Market Order is always False for Bracket Order
            'profit_value': profit,
            'stoploss_value': stoploss,
            'trailing_gap': trailing_stoploss
        }
        self._update_payload(d)
        data = self._post_helper('place_bracket_order')
        # print(data)
        # df = pd.DataFrame(data)
        # print(df)
        order_info = data[0]
        print(order_info)
        return order_info['order_no']

    def exit_bracket_order(self, order_no, segment=SEGMENT_EQUITY):
        order_details = self.order_history(order_no, segment)[0]
        print(order_details)
        segment = self._segments[order_details['instrument']]
        d = {
            'client_id': order_details['client_id'],
            # 'user_id': userid,
            'txn_type': order_details['txn_type'],
            'exchange': order_details['exchange'],
            'segment': segment,
            'product': order_details['product'],
            'security_id': order_details['security_id'],
            'quantity': order_details['quantity'],
            'price': order_details['price'],
            'validity': order_details['validity'],
            'order_type': order_details['order_type'],
            'disc_quantity': order_details['disc_quantity'],
            'trigger_price': order_details['trigger_price'],
            'off_mkt_flag': False,
            # 'remarks': '',
            'mkt_type': order_details['mkt_type'],
            'good_till_days_date': order_details['good_till_days_date'],
            'mkt_pro_flag': order_details['mkt_pro_flag'],
            'mkt_pro_value': order_details['mkt_pro_value'],
            'algo_order_no': '0',
            'order_no': str(order_details['order_no']),
            'serial_no':  order_details['serial_no'],
            'leg_no': '1',
            'group_id': '1'
        }

        self._update_payload(d)
        data = self._post_helper('exit_bracket_order')
        if self.debug:
            logger.debug(f"Data :: {data}")
        return json.dumps(data)

    def exit_cover_order(self, order_no, segment=SEGMENT_EQUITY):
        order_details = self.order_history(order_no, segment)[0]
        print(order_details)
        segment = self._segments[order_details['instrument']]
        d = {
            'client_id': order_details['client_id'],
            # 'user_id': userid,
            'txn_type': order_details['txn_type'],
            'exchange': order_details['exchange'],
            'segment': segment,
            'product': order_details['product'],
            'security_id': order_details['security_id'],
            'quantity': order_details['quantity'],
            'price': order_details['price'],
            'validity': order_details['validity'],
            'order_type': order_details['order_type'],
            'disc_quantity': order_details['disc_quantity'],
            'trigger_price': order_details['trigger_price'],
            'off_mkt_flag': False,
            # 'remarks': '',
            'mkt_type': order_details['mkt_type'],
            'good_till_days_date': order_details['good_till_days_date'],
            'mkt_pro_flag': order_details['mkt_pro_flag'],
            'mkt_pro_value': order_details['mkt_pro_value'],
            'algo_order_no': '0',
            'order_no': str(order_details['order_no']),
            'serial_no':  order_details['serial_no'],
            'leg_no': '1',
            'group_id': '1'
        }

        self._update_payload(d)
        data = self._post_helper('exit_cover_order')
        if self.debug:
            logger.debug(f"Data :: {data}")
        return json.dumps(data)

    def market_status(self, exchange=EXCHANGE_NSE, segment=SEGMENT_EQUITY, mkt_type=MARKET_TYPE_NL):
        segment = segment if exchange is not self.EXCHANGE_MCX else self.SEGMENT_COMMODITY
        d = {
            'exchange': exchange,
            'segment': segment,
            'mkt_type': mkt_type
        }
        self._update_payload(d)
        data = self._post_helper('market_status')
        df = pd.DataFrame(data)
        print(df)
        if self.debug:
            logger.debug(f"Data :: {df}")
        return df

    def order_history(self, order_no, segment=SEGMENT_EQUITY):
        """ get order details based on order number and segment """
        d = {
            'client_id': self._client_id,
            'order_no': str(order_no),
            'segment': segment
        }
        self._update_payload(d)
        data = self._post_helper('order_history')
        print(data)
        if self.debug:
            logger.debug(f"[DEBUG] : order history data :: \n{data}")
        return data

        # order_columns = ["exchange", "txn_type", "symbol", "security_id", "quantity", "traded_quantity",
        #                  "product", "order_date_time", "exch_order_time", "disc_quantity", "remaining_quantity", "validity", "serial_no", "source", "order_no", "exch_order_no",
        #                  "mkt_pro_flag", "mkt_pro_value", "settlor", "mkt_type", "good_till_days_date", "instrument", "strike_price",
        #                  "expiry_date", "opt_type", "lot_size", "error_code", "last_updated_time"]
        # df = pd.DataFrame(data, columns=order_columns)
        # if format_type == 'csv':
        #     return df.to_csv(index=False)
        # if format_type == 'json':
        #     return json.dumps(data, indent=1)
        # print(df)
        # return df

        # ["client_id","entity_id","exch_order_no","exchange","txn_type","symbol","security_id","quantity","remaining_quantity",
        # "traded_quantity","product","product_name","order_date_time","exch_order_time","last_updated_time","status","price",
        # "trigger_price","order_type","reason_description","disc_quantity","validity","serial_no","source","order_no","pan_no",
        # "participant_type","mkt_pro_flag","mkt_pro_value","settlor","encash_flag","mkt_type","good_till_days_date","instrument",
        # "strike_price","expiry_date","opt_type","lot_size","series","isin","display_name","exchange_inst_name","error_code","placed_by","source_name"]

    def trade_history(self, order_no, segment=SEGMENT_EQUITY, leg_no=1):
        """ get trade history or details based on order number and segment, leg number is optional """
        d = {
            'client_id': self._client_id,
            'order_no': str(order_no),
            'segment': segment,
            'leg_no': leg_no
        }
        self._update_payload(d)
        data = self._post_helper('trade_history')
        if self.debug:
            logger.debug(f"[DEBUG] :: Trade History Data ::")
            logger.debug(json.dumps(data))
        return data

    def exit_pending_orders(self, include_amo=False):
        df = self.orders()

        if include_amo:
            df = df.loc[df['status'].str.contains('O-Pending|O-Modified'), [
                'order_no', 'status', 'segment', 'product']]
            for order in df.itertuples():
                print(f'cancelling order {order.order_no} with status :: {order.status} '
                      + 'segment :: {order.segment} product :: {order.product}')
                self.cancel_order(order.order_no, order.segment, is_amo=True)
            
            df = self.orders()

        df = df.loc[df['status'].str in ['Pending', 'Modified'], [
            'order_no', 'status', 'segment', 'product']]


        for order in df.itertuples():
            if order.status in ['O-Pending', 'O-Modified']:
                print(f'skipping order {order.order_no} with status :: {order.status}')
                continue
            if self.debug is not None:
                logger.debug(f'[DEBUG] : order :: {order}')
            if order.product == 'B':
                self.exit_bracket_order(order.order_no, order.segment)
            elif order.product == 'V':
                self.exit_cover_order(order.order_no, order.segment)
            elif order.product in ['I', 'C', 'H', 'F', 'M']:
                print(f'cancelling order {order.order_no} with status :: {order.status} '
                      + 'segment :: {order.segment} product :: {order.product}')
                self.cancel_order(order.order_no, order.segment)

    def sell_bo_limit(self, exchange, symbol, quantity, price, target, stoploss):
        """Places Sell Bracket Order with Order Type as Limit

        Args:
            symbol (str): Symbol of NSE instrument
            quantity (int): Quantity as positive integer
            price (float): Limit Price for selling
            target (float): Target or Profit value
            stoploss (float): Stoploss value

        Returns:
            int: order number
        """
        data = DataApi()
        inst = data.get_instrument_by_exchange_symbol(exchange, symbol)
        return self.place_bracket_order(inst, self.TRANSACTION_TYPE_SELL, self.ORDER_TYPE_LIMIT, quantity, price, target, stoploss)

    def sell_amo_limit(self, exchange, symbol, quantity, price):
        data = DataApi()
        inst = data.get_instrument_by_exchange_symbol(exchange, symbol)
        print(inst)
        return self.place_order(inst, quantity, price, is_amo=True)

    def square_off_all(self):
        df = self.positions()
        data = DataApi()
        for position in df.itertuples():
            if position.net_qty != 0:
                quantity = abs(position.net_qty)
                inst = data.get_instrument_by_token_or_security_id(
                    position.security_id)
                txn_type = self.TRANSACTION_TYPE_BUY if position.net_qty < 0 else self.TRANSACTION_TYPE_SELL
                self.place_order(inst, quantity, price=0.0, txn_type=txn_type,
                                 order_type=self.ORDER_TYPE_MARKET, product=position.product)
            else:
                print(f'no position for {position.symbol}')

    def square_off_symbol(self, symbol):
        df = self.positions()
        data = DataApi()
        for position in df.itertuples():
            if position.net_qty != 0 and position.symbol == symbol:
                quantity = abs(position.net_qty)
                inst = data.get_instrument_by_token_or_security_id(
                    position.security_id)
                txn_type = self.TRANSACTION_TYPE_BUY if position.net_qty < 0 else self.TRANSACTION_TYPE_SELL
                self.place_order(inst, quantity, price=0.0, txn_type=txn_type,
                                 order_type=self.ORDER_TYPE_MARKET, product=position.product)
            else:
                print(f'no position for {position.symbol}')

    def place_order(self,
                    instrument,
                    quantity,
                    price,
                    txn_type=TRANSACTION_TYPE_SELL,
                    order_type=ORDER_TYPE_LIMIT,
                    product=PRODUCT_INTRADAY,
                    trigger=0.0,
                    validity=VALIDITY_DAY,
                    is_amo=False):
        """ Place order for Intraday, Margin

        Args:
            instrument (Instrument): Instrument to trade it is namedtuple
            quantity (int): Positive number (quantity) of lots or shares to buy or sell
            price (float): Price value in float which cannot be zero when order_type is ORDER_TYPE_LIMIT or ORDER_TYPE_STOPLOSS
            txn_type (str, optional): 'B' for Buy and 'S' for Sell or choose from shoonya.TRANSACTION_TYPE_BUY. \
                Defaults to shoonya.TRANSACTION_TYPE_SELL
            order_type (str, optional): Type of order like 'LMT', 'MKT', 'SL' or 'SLM'. Choose from shoonya.ORDER_TYPE_[...]. Defaults to ORDER_TYPE_LIMIT.
            product (str, optional): Type of product CNC (C), Margin (M) for options, Intraday (I), Normal - Hybrid (H) and MTF (F). Defaults to PRODUCT_INTRADAY.
            trigger (float, optional): Trigger at which order must be placed useful for SL or SLM orders. Defaults to 0.0.
            validity (str, optional): Validity of order. Defaults to VALIDITY_DAY.
            is_amo (bool): After Market Order. Defaults to False

        Returns:
            int: order number
        """

        d = {
            'client_id': self._client_id,
            'user_id': self._client_id,
            'exchange': instrument.exchange,
            'segment': instrument.segment,
            'order_type': order_type,
            'price': price,
            'product': product,
            'quantity': quantity,
            'security_id': instrument.token,
            'txn_type': txn_type,
            'trigger_price': str(trigger),
            'validity': validity,
            'off_mkt_flag': is_amo
        }
        self._update_payload(d)
        data = self._post_helper('place_order')
        print(data)
        df = pd.DataFrame(data)
        print(df)
        order_info = data[0]
        print(order_info)
        return order_info['order_no']

    def cancel_order(self, order_no, segment=SEGMENT_EQUITY, is_amo=False):
        """ Cancel an order with order number and segment

        Args:
            order_no (int): Order number as int or string
            segment (str, optional): Segment as 'E' / 'D' / 'C' / 'M'. Choose from shoonya.SEGMENT_DERIVATIVE, etc. Defaults to SEGMENT_EQUITY.

        Returns:
            order_no: Returns order number when status is success
        """

        order_details = self.order_history(order_no, segment)[0]
        # print(order)
        d = {
            'client_id': order_details['client_id'],
            'user_id': order_details['client_id'],
            'txn_type': order_details['txn_type'],
            'exchange': order_details['exchange'],
            'segment': segment,
            'product': order_details['product'],
            'security_id': order_details['security_id'],
            'quantity': order_details['quantity'],
            'price': order_details['price'],
            'validity': order_details['validity'],
            'order_type': order_details['order_type'],
            'disc_quantity': order_details['disc_quantity'],
            'trigger_price': order_details['trigger_price'],
            'off_mkt_flag': is_amo,
            # 'remarks': '',
            'mkt_type': order_details['mkt_type'],
            'good_till_days_date': order_details['good_till_days_date'],
            'mkt_pro_flag': order_details['mkt_pro_flag'],
            'mkt_pro_value': order_details['mkt_pro_value'],
            'algo_order_no': '0',
            'order_no': str(order_details['order_no']),
            'serial_no':  order_details['serial_no'],
            'leg_no': '1',
            'group_id': '1'
        }
        self._update_payload(d)
        data = self._post_helper('cancel_order')
        # if data['status'] == 'error':
        #     d['off_mkt_flag'] = True
        #     self._update_payload(d)
        #     data = self._post_helper('cancel_order')
        # print(data)
        df = pd.DataFrame(data)
        print(df.iloc[0])
        order_info = data[0]
        print(order_info)
        return order_info['order_no']

    def modify_order(self, segment, order_no, price, quantity,):
        """ Modify an order with order number and segment

        Args:
            segment (str, optional): Segment as 'E' / 'D' / 'C' / 'M'. Choose from shoonya.SEGMENT_DERIVATIVE, etc. Defaults to SEGMENT_EQUITY.
            order_no (int): Order number as int or string
            price (float): Positive number


        Returns:
            order_no: Returns order number when status is success
        """

        order_details = self.order_history(order_no, segment)[0]
        # print(order)
        d = {
            'client_id': order_details['client_id'],
            'user_id': order_details['client_id'],
            'txn_type': order_details['txn_type'],
            'exchange': order_details['exchange'],
            'segment': segment,
            'product': order_details['product'],
            'security_id': order_details['security_id'],
            'quantity': order_details['quantity'],
            'price': order_details['price'],
            'validity': order_details['validity'],
            'order_type': order_details['order_type'],
            'disc_quantity': order_details['disc_quantity'],
            'trigger_price': order_details['trigger_price'],
            'off_mkt_flag': False,
            # 'remarks': '',
            'mkt_type': order_details['mkt_type'],
            'good_till_days_date': order_details['good_till_days_date'],
            'mkt_pro_flag': order_details['mkt_pro_flag'],
            'mkt_pro_value': order_details['mkt_pro_value'],
            'algo_order_no': '0',
            'order_no': str(order_details['order_no']),
            'serial_no':  order_details['serial_no'],
            'leg_no': '1',
            'group_id': '1'
        }
        self._update_payload(d)
        data = self._post_helper('cancel_order')
        # print(data)
        df = pd.DataFrame(data)
        print(df.iloc[0])
        order_info = data[0]
        print(order_info)
        return order_info['order_no']

    def modify_bracket_order(self, segment, order_no,
                             quantity=None,
                             price=None,
                             target=None):
        """ Modify order for Intraday, Margin

        Args:
            instrument (Instrument): Instrument to trade it is namedtuple
            quantity (int): Positive number (quantity) of lots or shares to buy or sell
            price (float): Price value in float which cannot be zero when order_type is ORDER_TYPE_LIMIT or ORDER_TYPE_STOPLOSS
            txn_type (str, optional): 'B' for Buy and 'S' for Sell or choose from shoonya.TRANSACTION_TYPE_BUY. \
                Defaults to shoonya.TRANSACTION_TYPE_SELL
            order_type (str, optional): Type of order like 'LMT', 'MKT', 'SL' or 'SLM'. Choose from shoonya.ORDER_TYPE_[...]. Defaults to ORDER_TYPE_LIMIT.
            product (str, optional): Type of product CNC (C), Margin (M) for options, Intraday (I), Normal - Hybrid (H) and MTF (F). Defaults to PRODUCT_INTRADAY.
            trigger (float, optional): Trigger at which order must be placed useful for SL or SLM orders. Defaults to 0.0.
            validity (str, optional): Validity of order. Defaults to VALIDITY_DAY.
            is_amo (bool): After Market Order. Defaults to False

        Returns:
            int: order number
        """

        order_details = self.order_history(order_no, segment)[0]
        print(order_details)
        segment = self._segments[order_details['instrument']]

        d = {
            'client_id': order_details['client_id'],
            # 'user_id': userid,
            'txn_type': order_details['txn_type'],
            'exchange': order_details['exchange'],
            'segment': segment,
            'product': order_details['product'],
            'security_id': order_details['security_id'],
            'quantity': order_details['quantity'] if quantity is None else quantity,
            'price': order_details['price'],
            'validity': order_details['validity'],
            'order_type': order_details['order_type'],
            'disc_quantity': order_details['disc_quantity'],
            'trigger_price': order_details['trigger_price'],
            'off_mkt_flag': False,
            # 'remarks': '',
            'mkt_type': order_details['mkt_type'],
            'good_till_days_date': order_details['good_till_days_date'],
            'mkt_pro_flag': order_details['mkt_pro_flag'],
            'mkt_pro_value': order_details['mkt_pro_value'],
            'algo_order_no': '0',
            'order_no': str(order_details['order_no']),
            'serial_no':  order_details['serial_no'],
            'leg_no': '1',
            'group_id': '1'
        }

        self._update_payload(d)
        data = self._post_helper('modify_bracket_order')
        if self.debug:
            logger.debug(f"Data :: {data}")
        return data
