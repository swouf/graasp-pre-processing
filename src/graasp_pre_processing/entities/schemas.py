from datetime import datetime
import pandera as pa

from graasp_pre_processing.utils import timestamp_parser

members_schema = pa.DataFrameSchema({
    "name": pa.Column(str),
    "email": pa.Column(str, nullable=True),
    "extra": pa.Column(dict, nullable=True),
}, index=pa.Index(str, name="id"))


items_schema = pa.DataFrameSchema({
       "name": pa.Column(str),
       "displayName": pa.Column(str),
       "description": pa.Column(str, nullable=True),
       "createdAt": pa.Column(datetime, parsers=timestamp_parser, coerce=True),
       "updatedAt": pa.Column(datetime, parsers=timestamp_parser, coerce=True),
       "deletedAt": pa.Column(datetime, parsers=timestamp_parser, coerce=True, nullable=True),
       "settings": pa.Column(dict),
       "extra": pa.Column(dict),
       "path": pa.Column(str),
       "lang": pa.Column(str),
       "order": pa.Column(int, coerce=True),
       "creatorId": pa.Column(str),
       "parentId": pa.Column(str),
}, index=pa.Index(str))