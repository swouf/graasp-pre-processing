import logging
import pandas as pd
from pandera import check_input, check_io

from .schemas import responses_schema

log = logging.getLogger(__name__)

def compute_childrens(id: str, responses: pd.DataFrame) -> int:
    log.debug(f"Computing number of childrens for {id}")
    childrens = responses[responses['parentId'] == id]['id'].dropna()
    grand_childrens = childrens.apply(lambda x: compute_childrens(x, responses)).sum()
    return childrens.count() + grand_childrens

# @check_input(responses_schema)
def compute_nbr_of_childrens(responses: pd.DataFrame) -> pd.DataFrame:
    """Compute the number of childrens (direct childrens + grand childrens) for each response.

    Args:
        responses (pd.DataFrame): responses dataframe

    Returns:
        pd.DataFrame: the input dataframe with the column 'nbrOfChildrens'
    """
    r = responses.reset_index()
    responses_w_children = responses.join(r.join(r['id']\
                                                .apply(lambda x: compute_childrens(x, r))\
                                                .rename('nbrOfChildrens'))\
                                            .set_index('id')\
                                            .get(['nbrOfChildrens']))
    return responses_w_children