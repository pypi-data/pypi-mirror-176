import ast
import configparser
import copy
import inspect
import textwrap
import typing as t
from importlib.util import find_spec
from io import StringIO

from pyqtgraph.parametertree import (
    Interactor as PtreeInteractor,
    RunOptions as PtreeRunOpts,
)
from pyqtgraph.parametertree.interactive import PARAM_UNSET
from pyqtgraph.parametertree.Parameter import PARAM_TYPES

from qtextras import fns

T = t.TypeVar("T")


class FROM_PREV_IO(PARAM_UNSET):
    """
    Helper class to indicate whether a key in this IO is supposed to come from
    a previous process stage. Typical usage:
    ```if not hyperparam: self[k] = self.FROM_PREV_IO```

    Typically, process objects will have two IO dictionaries: One that hold the input
    spec (which makes use of `FROM_PREV_IO`) and one that holds the runtime process
    values. The latter IO will not make use of `FROM_PREV_IO`.
    """


class RunOptions(PtreeRunOpts):
    # Backwards compatibility
    ON_BUTTON = PtreeRunOpts.ON_ACTION


def bindInteractorOptions(overwrite=False, **opts):
    """
    Decorator to bind options to an interactor. This is useful for when the
    call to `interact` is separate from the function definition, but parameter
    options should be located with the function definition. Used as a decorator:
    >>> from qtextras import bindInteractorOptions as bind, QtExtrasInteractor
    >>> @bind(a=dict(step=5))
    ... def myFunc(a=1):
    ...     print(a)
    >>> step = QtExtrasInteractor().interact(myFunc).child("a").opts["step"]
    >>> assert step == 5
    """

    def wrapper(func: T) -> T:
        if hasattr(func, "__interactor_bind_options__") and not overwrite:
            func.__interactor_bind_options__.update(opts)
        else:
            func.__interactor_bind_options__ = opts
        return func

    return wrapper


class QtExtrasInteractor(PtreeInteractor):
    titleFormat = fns.nameFormatter
    displayIgnored = False

    def functionToParameterDict(self, function, **overrides):
        if hasattr(function, "__interactor_bind_options__"):
            newOverrides = function.__interactor_bind_options__
            if overrides:
                newOverrides = copy.deepcopy(newOverrides)
            for kk, vv in overrides.items():
                if not isinstance(vv, dict):
                    overrides[kk] = dict(value=vv)
            overrides = fns.hierarchicalUpdate(newOverrides, overrides)
        ret = super().functionToParameterDict(function, **overrides)
        for ch in ret.get("children", []):
            if ch["value"] is PARAM_UNSET:
                # Avoid causing failures from unspecified parameters, since qtextras
                # allows chaining multiple processes together
                ch["value"] = FROM_PREV_IO
        # By default, don't nest if no children are present
        return ret

    def resolveAndHookupParameterChild(
        self, functionGroup, childOpts, interactiveFunction
    ):
        extra = interactiveFunction.extra
        if childOpts["value"] is FROM_PREV_IO and childOpts["name"] not in extra:
            extra[childOpts["name"]] = FROM_PREV_IO
        if childOpts["name"] in extra or childOpts.get("ignore"):
            return None
        if childOpts.get("type") not in PARAM_TYPES:
            childOpts["type"] = "display"
            childOpts["value"] = extra.get(childOpts["name"], childOpts["value"])
            if not self.displayIgnored:
                # Avoid placing this child in the tree
                functionGroup = None
        return super().resolveAndHookupParameterChild(
            functionGroup, childOpts, interactiveFunction
        )

    def _resolveFunctionGroup(self, functionDict, interactiveFunction):
        # Possible for name to be overridden at the interactive level without
        # affecting the raw function name. In this case, prefer the interactive
        # name. Note in all cases where `interactiveFunc.__name__ == function.__name__`,
        # this is basically an inexpensive no-op.
        functionDict["name"] = interactiveFunction.__name__
        if self.titleFormat is not None:
            functionDict["title"] = self._nameToTitle(
                functionDict["name"], forwardStringTitle=True
            )

        return super()._resolveFunctionGroup(functionDict, interactiveFunction)


class ParameterlessInteractor(QtExtrasInteractor):
    """
    Places every key in "extra" instead of making parameters
    """

    def interact(self, function, *, ignores=None, **kwargs):
        if ignores is None:
            ignores = []
        ignores = set(ignores)
        funcDict = self.functionToParameterDict(function, **kwargs.get("overrides", {}))
        ignores.update(ch["name"] for ch in funcDict["children"])
        return super().interact(function, ignores=ignores, **kwargs)


class _DocstringInteractor(QtExtrasInteractor):
    streamFormat = "ini"
    titleFormat = fns.nameFormatter
    runActionTemplate = dict(defaultName="Run", type="shortcut")

    def functionToParameterDict(self, function, **overrides):
        docDict = docParser(function.__doc__, self.streamFormat)
        for kk in overrides:
            overrideVal = overrides[kk]
            if kk in docDict:
                if isinstance(overrideVal, dict):
                    docDict[kk].update(overrideVal)
                else:
                    docDict[kk]["value"] = overrideVal
            else:
                docDict[kk] = overrideVal
        docDict.pop("tip", None)
        return super().functionToParameterDict(function, **docDict)


def docParser(docstring: str, streamFormat="ini"):
    """
    From a function docstring, extracts relevant information for how to create smarter
      parameter boxes.

    Parameters
    ----------
    docstring
        Function docstring
    streamFormat
        Format of the docstring, either yaml or ini
    """
    if streamFormat == "yaml":
        parser = parseYamlDocstring
    elif streamFormat == "ini":
        parser = parseIniDocstring
    else:
        raise ValueError(f"Unknown docstring stream format: {streamFormat}")
    return parser(docstring)


def parseYamlDocstring(doc: str):
    out = {}
    parsed = dp.parse(doc)
    out["tip"] = "\n".join(
        [
            desc
            for desc in [parsed.short_description, parsed.long_description]
            if desc is not None
        ]
    )
    for param in parsed.params:
        stream = StringIO(param.description)
        try:
            paramDoc = fns.yamlLoad(stream)
        except fns.YAMLError:
            # Some problem parsing, treat as string
            paramDoc = param.description
        if isinstance(paramDoc, str):
            paramDoc = {"tip": paramDoc}
        if paramDoc is None:
            continue
        out[param.arg_name] = dict(name=param.arg_name, **paramDoc)
    return out


def parseIniDocstring(doc: str):
    """
    Parses function documentation for relevant parameter definitions. `doc` must be
    formatted like an .ini file, where each option's parameters are preceded by a
    ``[<arg>.options]`` header. See the examples in tests/parametertree/test_docparser
    for valid configurations. Note that if the `docstring_parser` module is available
    in the python environment, section headers as described above are *not required*
    since they can be inferred from the properly formatted docstring. The return value
    is a dict where each entry contains the found specifications of a given argument,
    i.e {"param1": {"limits": [0, 10], "title": "hi"}, "param2": {...}}, etc. Note that
    currently only literal evaluation with builtin objects is supported, i.e. the
    return result of ast.literal_eval on the value string of each option.

    Parameters
    ----------
    doc
      Documentation to parse
    """
    # Use docstring parser if it's available, otherwise basic parsing
    if find_spec("docstring_parser") is not None:
        return _parseIniDocstring_docstringParser(doc)
    else:
        return _parseIniDocstring_basic(doc)


def _parseIniDocstring_docstringParser(doc):
    """
    Use docstring_parser for a smarter version of the ini parser. Doesn't require
    ``[<arg>.options]`` headers and can handle more dynamic parsing cases
    """
    # Revert to basic method if ini headers are already present
    if not doc or ".options]\n" in doc:
        return _parseIniDocstring_basic(doc)
    import docstring_parser

    out = {}
    parsed = docstring_parser.parse(doc)
    out["tip"] = "\n".join(
        [
            desc
            for desc in [parsed.short_description, parsed.long_description]
            if desc is not None
        ]
    )
    for param in parsed.params:
        # Construct mini ini file around each parameter
        header = f"[{param.arg_name}.options]"
        miniDoc = param.description
        if header not in miniDoc:
            miniDoc = f"{header}\n{miniDoc}"
        # top-level parameter no longer represents whole function
        update = _parseIniDocstring_basic(miniDoc)
        update.pop("tip", None)
        out.update(update)
    return out


def _parseIniDocstring_basic(doc):
    """
    Implements quite primitive parsing of parameter signatures. Looks for
    ``[<param-name>.options]`` blocks in the config string and parses them with a
    ConfigParser. Note that all ``*.options`` blocks are expected to start at the
    same indentation level. Options shared across all parameters can be specified under
    a ``[DEFAULT]`` block.
    """
    out = {}
    # Adding "[DEFAULT] to the beginning of the doc will consume non-parameter
    # descriptions Account for things in commonly supported docstring formats:
    fmtDoc = _formatOptionsFromDoc(doc or "")

    parser = configparser.ConfigParser(allow_no_value=True)
    # Save case sensitivity
    parser.optionxform = str
    try:
        parser.read_string(fmtDoc)
    except configparser.Error:
        # Many things can go wrong reading a badly-formatted docstring, so failsafe by
        # returning early
        return out
    defaultKeys = set(parser.defaults())
    for kk, vv in parser.items():
        if not kk.endswith(".options"):
            continue
        paramName = kk.split(".")[0]
        # vv is a section with options for the parameter, but each option must be
        # literal eval'd for non-string values
        paramValues = dict(vv)
        # Consolidate all non-valued key strings into a single tip since they likely
        # belong to the argument documentation. Since dict preserves order, it should
        # come back out in the right order.
        backupTip = ""
        for paramK, paramV in list(paramValues.items()):
            if paramV is None:
                # Considered a tip of the current option if no corresponding value
                # and not a default option
                if paramK not in defaultKeys:
                    backupTip = f"{backupTip} {paramK}"
                # Remove this from the return value since it isn't really meaningful
                del paramValues[paramK]
                continue
            # noinspection PyBroadException
            try:
                paramValues[paramK] = ast.literal_eval(paramV)
            except Exception:
                # There are many reasons this can fail, a safe fallback is the original
                # string value
                pass
        if backupTip:
            paramValues.setdefault("tip", backupTip.strip())
        out[paramName] = paramValues
    # Since function documentation can be used as a description for whatever group
    # parameter hosts these parameters, store it in a name guaranteed not to collide
    # with parameter names since its invalid variable syntax (contains '-')
    out["tip"] = "\n".join(parser.defaults())
    return out


def _stripNSpaces(string, n):
    for ii in range(min(n, len(string))):
        if not string[ii].isspace():
            break
    else:
        ii = 0
    return string[ii:]


def _countStartingSpaces(line):
    ii = 0
    for ii in range(len(line)):
        if line[ii].isspace():
            ii += 1
    return ii


def _formatOptionsFromDoc(doc):
    """
    Dedents doc to [*.options] level for ConfigParser parsing and removes leading ":"
    from each line if needed. These are both factors that complicate config parsing
    later on
    """
    dedent = None
    docLines = doc.splitlines()
    defaultLine = -1
    for ii, line in enumerate(docLines):
        if dedent is None and ".options]" in line:
            dedent = _countStartingSpaces(line)
        stripped = line.strip()
        if stripped.startswith(":"):
            # :param: style documentation violates ini standards
            docLines[ii] = line.replace(":", "", 1)
        elif stripped == "[DEFAULT]":
            defaultLine = ii
    if defaultLine > -1:
        # Remove all lines before default if it's present, since they can't be parsed
        docLines = docLines[defaultLine:]
    if dedent is not None:
        doc = "\n".join(_stripNSpaces(line, dedent) for line in docLines)
    else:
        doc = textwrap.dedent(doc)

    # Now that wrapping ensures lines start without whitespace relative to options,
    # default block can be added if needed
    if defaultLine < 0:
        doc = f"[DEFAULT]\n{doc}"

    return doc
