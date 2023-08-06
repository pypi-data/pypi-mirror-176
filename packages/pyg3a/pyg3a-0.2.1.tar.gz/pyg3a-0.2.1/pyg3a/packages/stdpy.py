#!/usr/bin/env python3


def __pyg3a_len(obj: cst.CSTNode) -> str:
    ARG_TYPES = {0: [str]}
    OPTIONAL_ARGS = {}
    if _correct_arg_types(ARG_TYPES):
        if len(obj.args) < len(ARG_TYPES) - len(OPTIONAL_ARGS):
            raise SyntaxError(
                f"Too few arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
            )
        if len(obj.args) > len(ARG_TYPES):
            raise SyntaxError(
                f"Too many arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
            )

        args = [_obj_to_c_str(arg.value) for arg in obj.args]
        if len(obj.args) < len(ARG_TYPES):
            args.extend(
                [
                    _obj_to_c_str(OPTIONAL_ARGS[i])
                    for i in [item for item in ARG_TYPES.keys() if item not in range(len(obj.args))]
                ]
            )

        _import("string.h")
        return f"strlen({args[0]}.c_str())"
    raise SyntaxError(
        f"Incorrect type(s) of arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
    )


def __pyg3a_str(obj: cst.CSTNode) -> str:
    ARG_TYPES = {0: [int]}
    OPTIONAL_ARGS = {}
    if _correct_arg_types(ARG_TYPES):
        if len(obj.args) < len(ARG_TYPES) - len(OPTIONAL_ARGS):
            raise SyntaxError(
                f"Too few arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
            )
        if len(obj.args) > len(ARG_TYPES):
            raise SyntaxError(
                f"Too many arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
            )

        args = [_obj_to_c_str(arg.value) for arg in obj.args]
        if len(obj.args) < len(ARG_TYPES):
            args.extend(
                [
                    _obj_to_c_str(OPTIONAL_ARGS[i])
                    for i in [item for item in ARG_TYPES.keys() if item not in range(len(obj.args))]
                ]
            )

        _import("fxcg/misc.h")
        _add_c_func(
            "_str",
            """String _str(int val) {
\tunsigned char buffer[256];
\titoa(val, buffer);
\treturn String((char*) buffer);
}""",
        )

        return f"_str({', '.join(args)})"
    raise SyntaxError(
        f"Incorrect type(s) of arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
    )


def __pyg3a_range(obj: cst.CSTNode) -> str:
    ARG_TYPES = {0: [int], 1: [int], 2: [int]}
    if len(obj.args) == 1:
        ARG_TYPES = {0: [int]}

    OPTIONAL_ARGS = {2: 1}
    if len(obj.args) == 1:
        OPTIONAL_ARGS = {}

    if _correct_arg_types(ARG_TYPES):
        if len(obj.args) < len(ARG_TYPES) - len(OPTIONAL_ARGS):
            raise SyntaxError(
                f"Too few arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
            )
        if len(obj.args) > len(ARG_TYPES):
            raise SyntaxError(
                f"Too many arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
            )

        args = [_obj_to_c_str(arg.value) for arg in obj.args]
        if len(obj.args) < len(ARG_TYPES):
            args.extend(
                [
                    _obj_to_c_str(OPTIONAL_ARGS[i])
                    for i in [item for item in ARG_TYPES.keys() if item not in range(len(obj.args))]
                ]
            )

        if len(args) == 1:
            return f"{{{', '.join([str(i) for i in range(int(args[0]))])}}}"

        return f"{{{', '.join([str(i) for i in range(int(args[0]), int(args[1]), int(args[2]))])}}}"
    raise SyntaxError(
        f"Incorrect type(s) of arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
    )


def __for_pyg3a_range(expr: cst.For, scope: dict[str, str]) -> list[str]:
    scope[expr.target.value] = "int"
    if len(expr.iter.args) == 1:
        return [
            f"for (int {expr.target.value} = 0; {expr.target.value} < {_obj_to_c_str(expr.iter.args[0].value)}; {expr.target.value}++) {{"
        ]
    elif len(expr.iter.args) == 2:
        return [
            f"for (int {expr.target.value} = {_obj_to_c_str(expr.iter.args[0].value)}; {expr.target.value} < {_obj_to_c_str(expr.iter.args[1])}; {expr.target.value}++) {{"
        ]
    return [
        f"for (int {expr.target.value} = {_obj_to_c_str(expr.iter.args[0].value)}; {expr.target.value} < {_obj_to_c_str(expr.iter.args[1].value)}; {expr.target.value} += {_obj_to_c_str(expr.iter.args[2].value)}) {{"
    ]


def __pyg3a_int(obj: cst.CSTNode) -> str:
    ARG_TYPES = {0: [float]}
    OPTIONAL_ARGS = {}
    if _correct_arg_types(ARG_TYPES):
        if len(obj.args) < len(ARG_TYPES) - len(OPTIONAL_ARGS):
            raise SyntaxError(
                f"Too few arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
            )
        if len(obj.args) > len(ARG_TYPES):
            raise SyntaxError(
                f"Too many arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
            )

        args = [_obj_to_c_str(arg.value) for arg in obj.args]
        if len(obj.args) < len(ARG_TYPES):
            args.extend(
                [
                    _obj_to_c_str(OPTIONAL_ARGS[i])
                    for i in [item for item in ARG_TYPES.keys() if item not in range(len(obj.args))]
                ]
            )

        return f"(int) ({', '.join(args)})"
    raise SyntaxError(
        f"Incorrect type(s) of arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
    )


def __pyg3a_round(obj: cst.CSTNode) -> str:
    ARG_TYPES = {0: [float]}
    OPTIONAL_ARGS = {}
    if _correct_arg_types(ARG_TYPES):
        if len(obj.args) < len(ARG_TYPES) - len(OPTIONAL_ARGS):
            raise SyntaxError(
                f"Too few arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
            )
        if len(obj.args) > len(ARG_TYPES):
            raise SyntaxError(
                f"Too many arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
            )

        args = [_obj_to_c_str(arg.value) for arg in obj.args]
        if len(obj.args) < len(ARG_TYPES):
            args.extend(
                [
                    _obj_to_c_str(OPTIONAL_ARGS[i])
                    for i in [item for item in ARG_TYPES.keys() if item not in range(len(obj.args))]
                ]
            )

        _add_c_func(
            f"_{NAME}",
            """int _round(float val) {
\tif (val < 0.0)
\t\treturn (int) (val - 0.5);
\treturn (int) (val + 0.5);
}""",
        )

        return f"_{NAME}({', '.join(args)})"
    raise SyntaxError(
        f"Incorrect type(s) of arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
    )


def __pyg3a_max(obj: cst.CSTNode) -> str:
    ARG_TYPES = {0: [int], 1: [int]}
    OPTIONAL_ARGS = {}
    if _correct_arg_types(ARG_TYPES):
        if len(obj.args) < len(ARG_TYPES) - len(OPTIONAL_ARGS):
            raise SyntaxError(
                f"Too few arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
            )
        if len(obj.args) > len(ARG_TYPES):
            raise SyntaxError(
                f"Too many arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
            )

        args = [_obj_to_c_str(arg.value) for arg in obj.args]
        if len(obj.args) < len(ARG_TYPES):
            args.extend(
                [
                    _obj_to_c_str(OPTIONAL_ARGS[i])
                    for i in [item for item in ARG_TYPES.keys() if item not in range(len(obj.args))]
                ]
            )

        _add_c_func(
            f"_{NAME}",
            """int _max(int a, int b) {
\tif (a > b)
\t\treturn a;
\treturn b;
}""",
        )

        return f"_{NAME}({', '.join(args)})"
    raise SyntaxError(
        f"Incorrect type(s) of arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
    )


def __pyg3a_min(obj: cst.CSTNode) -> str:
    ARG_TYPES = {0: [int], 1: [int]}
    OPTIONAL_ARGS = {}
    if _correct_arg_types(ARG_TYPES):
        if len(obj.args) < len(ARG_TYPES) - len(OPTIONAL_ARGS):
            raise SyntaxError(
                f"Too few arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
            )
        if len(obj.args) > len(ARG_TYPES):
            raise SyntaxError(
                f"Too many arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
            )

        args = [_obj_to_c_str(arg.value) for arg in obj.args]
        if len(obj.args) < len(ARG_TYPES):
            args.extend(
                [
                    _obj_to_c_str(OPTIONAL_ARGS[i])
                    for i in [item for item in ARG_TYPES.keys() if item not in range(len(obj.args))]
                ]
            )

        _add_c_func(
            f"_{NAME}",
            """int _min(int a, int b) {
\tif (a < b)
\t\treturn a;
\treturn b;
}""",
        )

        return f"_{NAME}({', '.join(args)})"
    raise SyntaxError(
        f"Incorrect type(s) of arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
    )


def __types_pyg3a() -> dict[str, str]:
    func_types: dict[str, str] = {}
    func_types["str"] = "str"
    func_types["len"] = "int"
    func_types["int"] = "int"
    func_types["round"] = "int"
    func_types["max"] = "int"
    func_types["min"] = "int"

    return func_types
