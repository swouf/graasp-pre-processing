from datetime import datetime
import pandera as pa

from graasp_pre_processing.utils import timestamp_parser

app_data_schema = pa.DataFrameSchema({
    "type": pa.Column(str),
    "visibility": pa.Column(str, pa.Check.isin(["member", "item"])),
    "data": pa.Column(dict),
    "createdAt": pa.Column(datetime, parsers=timestamp_parser, coerce=True),
    "updatedAt": pa.Column(datetime, parsers=timestamp_parser, coerce=True),
    "accountId": pa.Column(str),
    "creatorId": pa.Column(str),
    "itemId": pa.Column(str),
}, index=pa.Index(str))

app_settings_schema = pa.DataFrameSchema({
    "name": pa.Column(str),
    "data": pa.Column(dict),
    "createdAt": pa.Column(datetime, parsers=timestamp_parser, coerce=True),
    "updatedAt": pa.Column(datetime, parsers=timestamp_parser, coerce=True),
    "creatorId": pa.Column(str),
    "itemId": pa.Column(str),
}, index=pa.Index(str))