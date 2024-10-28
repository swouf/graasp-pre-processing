from datetime import datetime
import pandera as pa

responses_schema = pa.DataFrameSchema({
    "type": pa.Column(str),
    "visibility": pa.Column(str, pa.Check.isin(["member", "item"])),
    "createdAt": pa.Column(datetime),
    "updatedAt": pa.Column(datetime),
    "accountId": pa.Column(str),
    "creatorId": pa.Column(str),
    "itemId": pa.Column(str),
    "response": pa.Column(str),
    "responsesChain": pa.Column(list[str], nullable=True),
    "round": pa.Column(int, nullable=True),
    "bot": pa.Column(bool),
    "numberOfAssistants": pa.Column(int),
    "visibilityMode": pa.Column(str),
    "assistantId": pa.Column(str, nullable=True),
    "parentId": pa.Column(str, nullable=True),
}, index=pa.Index(str))