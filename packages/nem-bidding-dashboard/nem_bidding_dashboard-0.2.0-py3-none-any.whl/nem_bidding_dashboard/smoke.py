from nemosis import defaults, dynamic_data_compiler

defaults.table_columns['BIDPEROFFER_D'] += ['PASAAVAILABILITY', 'ROCUP']

start_time = '2017/01/01 00:00:00'
end_time = '2017/01/01 00:05:00'
table = 'BIDPEROFFER_D'
raw_data_cache = "D:/nemosis_cache"

volume_bid_data = dynamic_data_compiler(start_time, end_time, table, raw_data_cache, rebuild=True)