import ast, builtins
from decimal import Decimal

NUMBER_TYPES = (int, float)
APPROVED_TYPES = (Decimal, str, bool, bytes)

ALLOWED_AST_TYPES = {
    ast.Module,
    ast.Eq,
    ast.Call,
    ast.Dict,
    ast.Attribute,
    ast.Pow,
    ast.Index,
    ast.Not,
    ast.alias,
    ast.If,
    ast.FunctionDef,
    ast.Global,  # Used for setting up resources in seed function during compilation
    ast.GtE,
    ast.LtE,
    ast.Load,
    ast.arg,
    ast.Add,
    #ast.Lambda,    # raghu todo consider removing it
    ast.Import,
    ast.ImportFrom,
    ast.Name,
    ast.Num,
    ast.BinOp,
    ast.Store,
    ast.Assert,
    ast.Assign,
    ast.AugAssign,
    ast.Subscript,
    ast.Compare,
    ast.Return,
    ast.NameConstant,
    ast.Expr,
    ast.keyword,
    ast.Sub,
    ast.arguments,
    ast.List,
    ast.Set,
    ast.Str,
    ast.UnaryOp,
    ast.Pass,
    ast.Tuple,
    ast.Div,
    ast.In,
    ast.NotIn,
    ast.Gt,
    ast.Lt,
    ast.Starred,
    ast.Mod,
    ast.NotEq,
    # Loops
    ast.For,
    ast.While,
    # comprehension
    ast.ListComp,
    ast.comprehension,
    ast.Slice,
    ast.USub,
    # Conditonals
    ast.BoolOp,
    ast.And,
    ast.Or,
    ast.Mult,

    # TODO: Decide if we actually want these
    # Error handling
    # ast.ExceptHandler,
    # ast.Try,
}

VIOLATION_TRIGGERS = {

    "S1": "Illegal seneca syntax type used",
    "S2": "Illicit use of '_' before variable",
    "S3": "Illicit use of Nested imports",
    "S4": "ImportFrom ast nodes not yet supported",
    "S5": "Contract not found in lib",
    "S6": "Illicit use of classes",
    "S7": "Illicit use of Async functions",
    "S8": "Invalid decorator used",
    "S9": "Multiple use of constructors detected",
    "S10": "Illicit use of multiple decorators",
    "S11": "Illicit keyword overloading",
    "S12": "Multiple targets to ORM definition detected"
}

SENECA_LIBRARY_PATH = 'seneca.libs'

ALLOWED_IMPORT_PATHS = [
    'seneca.contracts',
    'test_contracts'
]

_SAFE_NAMES = [
    '__import__',

    'None',
    'False',
    'True',

    'callable',
    'isinstance',
    'issubclass',

    'abs',
    'bool',
    'chr',
    'complex',
    'divmod',
    # 'float',
    'hash',
    'hex',
    'id',
    # 'int',

    'len',
    'oct',
    'ord',
    'pow',
    'range',
    'repr',
    'round',
    'slice',
    'str',
    'bytes',
    'tuple',
    'zip',

    # Iteration
    'map',
    'list',

    # JUST FOR TESTING! TODO remove this irl
    # 'dir',
    # 'help',
    'print',
    # 'globals',
    # 'locals',
    # 'type'
]

_SAFE_EXCEPTIONS = [
    'ArithmeticError',
    'AssertionError',
    'AttributeError',
    'BaseException',
    'BufferError',
    'BytesWarning',
    'DeprecationWarning',
    'EOFError',
    'EnvironmentError',
    'Exception',
    'FloatingPointError',
    'FutureWarning',
    'GeneratorExit',
    'IOError',
    'ImportError',
    'ImportWarning',
    'IndentationError',
    'IndexError',
    'KeyError',
    'KeyboardInterrupt',
    'LookupError',
    'MemoryError',
    'NameError',
    'NotImplementedError',
    'OSError',
    'OverflowError',
    'PendingDeprecationWarning',
    'ReferenceError',
    'RuntimeError',
    'RuntimeWarning',
    'StopIteration',
    'SyntaxError',
    'SyntaxWarning',
    'SystemError',
    'SystemExit',
    'TabError',
    'TypeError',
    'UnboundLocalError',
    'UnicodeDecodeError',
    'UnicodeEncodeError',
    'UnicodeError',
    'UnicodeTranslateError',
    'UnicodeWarning',
    'UserWarning',
    'ValueError',
    'Warning',
    'ZeroDivisionError',
]

SAFE_BUILTINS = {}

for name in _SAFE_NAMES:
    SAFE_BUILTINS[name] = getattr(builtins, name)

for name in _SAFE_EXCEPTIONS:
    SAFE_BUILTINS[name] = getattr(builtins, name)
