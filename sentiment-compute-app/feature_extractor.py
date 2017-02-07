import sys
from functools import partial
from collections import OrderedDict

import pandas
import sklearn.base


if sys.version_info.major == 3:
    imap = map
else:
    from itertools import imap


# FUNCTIONS


def is_field_nonnull(obj, field):
    """Check whether obj[field] is null (None or numpy.nan)"""
    if field not in obj:
        return False
    else:
        return not pandas.isnull(obj[field])


def subfield_getter(obj, field_seq):
    """Recursively get items from obj based on field_seq"""
    if len(field_seq) == 0:
        return obj
    elif field_seq[0] not in obj:
        return None
    else:
        return subfield_getter(obj[field_seq[0]], field_seq[1:])


def subfield_func_apply(obj, field_seq, func=len):
    """Return result of func(sub_obj) where sub_obj is the
    value found by recursively retrieving nested items from obj based
    on field_seq."""
    return func(subfield_getter(obj, field_seq))


feat_only_per_rec_funcs = OrderedDict(
    (
        ('text_len', partial(subfield_func_apply, field_seq=('text',), func=len)),
        ('user_protected', partial(subfield_getter, field_seq=('user', 'protected'))),
        ('user_verified', partial(subfield_getter, field_seq=('user', 'verified'))),
        ('is_quote', partial(is_field_nonnull, field='quoted_status')),
        ('is_retweet', partial(is_field_nonnull, field='retweeted_status')),
        ('user_mentions_n', partial(subfield_func_apply, field_seq=('entities', 'user_mentions'), func=len)),
        ('urls_n', partial(subfield_func_apply, field_seq=('entities', 'urls'), func=len)),
        ('hashtags_n', partial(subfield_func_apply, field_seq=('entities', 'hashtags'), func=len)),
        ('symbols_n', partial(subfield_func_apply, field_seq=('entities', 'symbols'), func=len)),
    )
)


# CLASSES

class FeatureExtractor(sklearn.base.TransformerMixin):
    def __init__(self, funcs):
        self.funcs = funcs

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        """return array of shape [n_samples, n_features]"""
        if isinstance(X, pandas.DataFrame):
            iter_ = imap(lambda a: a[1], X.iterrows())
        else:
            iter_ = X
        return tuple(tuple(func(i) for key, func in self.funcs.items()) for i in iter_)

    def __getstate__(self):
        return self.funcs

    def __setstate__(self, state):
        self.funcs = state
