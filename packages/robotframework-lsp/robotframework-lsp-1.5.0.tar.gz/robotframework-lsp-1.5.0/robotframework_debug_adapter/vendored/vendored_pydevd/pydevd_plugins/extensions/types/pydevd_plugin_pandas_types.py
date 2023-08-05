import sys

from _pydevd_bundle.pydevd_constants import PANDAS_MAX_ROWS, PANDAS_MAX_COLS, PANDAS_MAX_COLWIDTH
from _pydevd_bundle.pydevd_extension_api import TypeResolveProvider, StrPresentationProvider
from _pydevd_bundle.pydevd_resolver import inspect, MethodWrapperType
from _pydevd_bundle.pydevd_utils import Timer

from .pydevd_helpers import find_mod_attr


def _get_dictionary(obj, replacements):
    ret = dict()
    cls = obj.__class__
    for attr_name in dir(obj):

        # This is interesting but it actually hides too much info from the dataframe.
        # attr_type_in_cls = type(getattr(cls, attr_name, None))
        # if attr_type_in_cls == property:
        #     ret[attr_name] = '<property (not computed)>'
        #     continue

        timer = Timer()
        try:
            replacement = replacements.get(attr_name)
            if replacement is not None:
                ret[attr_name] = replacement
                continue

            attr_value = getattr(obj, attr_name, '<unable to get>')
            if inspect.isroutine(attr_value) or isinstance(attr_value, MethodWrapperType):
                continue
            ret[attr_name] = attr_value
        except Exception as e:
            ret[attr_name] = '<error getting: %s>' % (e,)
        finally:
            timer.report_if_getting_attr_slow(cls, attr_name)

    return ret


class PandasDataFrameTypeResolveProvider(object):

    def can_provide(self, type_object, type_name):
        data_frame_class = find_mod_attr('pandas.core.frame', 'DataFrame')
        return data_frame_class is not None and issubclass(type_object, data_frame_class)

    def resolve(self, obj, attribute):
        return getattr(obj, attribute)

    def get_dictionary(self, obj):
        replacements = {
            # This actually calls: DataFrame.transpose(), which can be expensive, so,
            # let's just add some string representation for it.
            'T': '<transposed dataframe -- debugger:skipped eval>',

            # This creates a whole new dict{index: Series) for each column. Doing a
            # subsequent repr() from this dict can be very slow, so, don't return it.
            '_series': '<dict[index:Series] -- debugger:skipped eval>',

            'style': '<pandas.io.formats.style.Styler -- debugger: skipped eval>',
        }
        return _get_dictionary(obj, replacements)

    def get_str(self, df):
        # The default repr depends on the settings of:
        # pandas.set_option('display.max_columns', None)
        # pandas.set_option('display.max_rows', None)
        # which can make the repr **very** slow on some cases, so, let's use a
        # version which

        return df.to_string(
            max_rows=PANDAS_MAX_ROWS,
            max_cols=PANDAS_MAX_COLS,
            max_colwidth=PANDAS_MAX_COLWIDTH,
            show_dimensions=True,
        )


class PandasSeriesTypeResolveProvider(object):

    def can_provide(self, type_object, type_name):
        series_class = find_mod_attr('pandas.core.series', 'Series')
        return series_class is not None and issubclass(type_object, series_class)

    def resolve(self, obj, attribute):
        return getattr(obj, attribute)

    def get_dictionary(self, obj):
        replacements = {
            # This actually calls: DataFrame.transpose(), which can be expensive, so,
            # let's just add some string representation for it.
            'T': '<transposed dataframe -- debugger:skipped eval>',

            # This creates a whole new dict{index: Series) for each column. Doing a
            # subsequent repr() from this dict can be very slow, so, don't return it.
            '_series': '<dict[index:Series] -- debugger:skipped eval>',

            'style': '<pandas.io.formats.style.Styler -- debugger: skipped eval>',
        }
        return _get_dictionary(obj, replacements)

    def get_str(self, series):
        return (series.to_string(
            max_rows=PANDAS_MAX_ROWS,
        ))


class PandasStylerTypeResolveProvider(object):

    def can_provide(self, type_object, type_name):
        series_class = find_mod_attr('pandas.io.formats.style', 'Styler')
        return series_class is not None and issubclass(type_object, series_class)

    def resolve(self, obj, attribute):
        return getattr(obj, attribute)

    def get_dictionary(self, obj):
        replacements = {
            'data': '<Styler data -- debugger:skipped eval>',

            '__dict__': '<dict -- debugger: skipped eval>',
        }
        return _get_dictionary(obj, replacements)


if not sys.platform.startswith("java"):
    TypeResolveProvider.register(PandasDataFrameTypeResolveProvider)
    StrPresentationProvider.register(PandasDataFrameTypeResolveProvider)

    TypeResolveProvider.register(PandasSeriesTypeResolveProvider)
    StrPresentationProvider.register(PandasSeriesTypeResolveProvider)

    TypeResolveProvider.register(PandasStylerTypeResolveProvider)
