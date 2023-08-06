#!/usr/bin/env python3

import abc
import logging
import random
import types
import typing

import libcst as cst

import pyg3a

ellipsis: typing.TypeAlias = type(Ellipsis)


class Block:
    CST_TO_C_EQV: dict[abc.ABCMeta, str] = {
        # Statements
        cst.Break: "break",
        cst.Continue: "continue",
        cst.Pass: "// PASS",
        #
        # Equivalence
        cst.Equal: "==",
        cst.Is: "==",
        cst.NotEqual: "!=",
        cst.IsNot: "!=",
        cst.GreaterThan: ">",
        cst.GreaterThanEqual: ">=",
        cst.LessThan: "<",
        cst.LessThanEqual: "<=",
        #
        # Logical
        cst.Or: "||",
        cst.And: "&&",
        cst.Not: "!",
        #
        # Operators
        cst.Add: "+",
        cst.Subtract: "-",
        cst.Multiply: "*",
        cst.Divide: "/",
        cst.Modulo: "%",
        # cst.Power - covered in cst.BinaryOperation as it requires math.h.
        # cst.FloorDivide - covered in cst.BinaryOperation as it requires math.h.
        #
        # Binary
        cst.BitAnd: "&",
        cst.BitOr: "|",
        cst.BitXor: "^",
        cst.BitInvert: "~",
        cst.LeftShift: "<<",
        cst.RightShift: ">>",
        #
        # Assign Operators
        cst.AddAssign: "+=",
        cst.SubtractAssign: "-=",
        cst.MultiplyAssign: "*=",
        cst.DivideAssign: "/=",
        cst.ModuloAssign: "%=",
        cst.BitAndAssign: "&=",
        cst.BitOrAssign: "|=",
        cst.BitXorAssign: "^=",
        cst.LeftShiftAssign: "<<=",
        cst.RightShiftAssign: ">>=",
        # cst.FloorDivideAssign - covered in cst.AugAssign as it does not have a 1-1 in C
        #
        # Pos and Neg
        cst.Plus: "+",
        cst.Minus: "-",
    }

    def __init__(
        self,
        exprs: typing.Sequence[cst.BaseStatement] | typing.Sequence[cst.BaseSmallStatement],
        tabs: int,
        scope: dict = None,
    ):
        if scope is None:
            scope = {}

        self.exprs: list[cst.CSTNode] = exprs
        for i, node in enumerate(self.exprs):
            if type(node) is cst.SimpleStatementLine:
                del self.exprs[i]
                for j, statement in enumerate(node.body):
                    self.exprs.insert(i + j, statement)

        self.tabs: str = tabs * "\t"
        self.tabnum: int = tabs
        self.scope: dict = scope.copy()

    @staticmethod
    def _const_to_py_obj(
        const: cst.BaseNumber | cst.BaseString | cst.Ellipsis | cst.Name,
    ) -> str | bool | int | float | complex | ellipsis | None:
        if type(const) is cst.Ellipsis:
            return ...

        if type(const) is cst.Imaginary:
            return complex(const.value)
        if type(const) is cst.Integer:
            if const.value[:2] == "0x":
                return int(const.value, 16)
            return int(const.value)
        if type(const) is cst.Float:
            return float(const.value)

        if type(const) is cst.SimpleString:
            return const.raw_value
        if type(const) is cst.FormattedString:
            raise SyntaxError("There is currently no support for formatted strings")
        if type(const) is cst.ConcatenatedString:
            if type(const.left) is cst.FormattedString or type(const.right) is cst.FormattedString:
                raise SyntaxError("There is currently no support for formatted strings")
            return const.left.raw_value + Block._const_to_py_obj(const.right)

        if type(const) is cst.Name:
            if const.value == "True":
                return True
            if const.value == "False":
                return False
            if const.value == "None":
                return None

        raise RuntimeError("Wrong argument passed to _const_to_py_obj: " + str(const))

    @staticmethod
    def _obj_to_c_str(
        obj: typing.Any,
        isType: bool = False,
        generateVoidLambda: bool = False,
        scope: dict[str, str] = {},
    ) -> str:
        if len(scope) == 0:
            scope = {}

        if type(obj) is int or type(obj) is float:
            return str(obj)
        if type(obj) is str:
            escaped_str: str = repr(obj).replace("'", '"')
            return f"String({escaped_str})"
        if type(obj) is bool:
            return "1" if obj is True else "0"
        if type(obj) is tuple:
            return f"{{{', '.join([Block._obj_to_c_str(o, scope=scope) for o in obj])}}}"
        if obj is None:
            pyg3a.pyg3a.PyG3A._import("stddef.h")
            return "NULL"
        if isinstance(obj, cst.CSTNode):
            if type(obj) is cst.SimpleStatementLine:
                obj = obj.body[0]

            if type(obj) is cst.Call and type(obj.func) is cst.Name:
                if "__pyg3a_" + obj.func.value in pyg3a.Main.project.custom_funcs:

                    def _correct_arg_types(ARG_TYPES: dict):
                        return all(
                            [
                                (
                                    (
                                        isinstance(
                                            arg,
                                            (cst.BaseNumber, cst.BaseString, cst.Ellipsis),
                                        )
                                        or (
                                            type(arg) is cst.Name
                                            and arg.value in ("True", "False", "None")
                                        )
                                    )
                                    and type(Block._const_to_py_obj(arg)) is ARG_TYPES[i]
                                )
                                or (
                                    all(
                                        [
                                            type(a) in (str, type, types.GenericAlias)
                                            for a in ARG_TYPES[i]
                                        ]
                                    )
                                    and Block._type(arg, scope, False)
                                    in [
                                        str(a)
                                        if (type(a) is types.GenericAlias or a is None)
                                        else (a if type(a) is str else a.__name__)
                                        for a in ARG_TYPES[i]
                                    ]
                                )
                                or (
                                    type(arg) is cst.Name
                                    and (
                                        arg.value in scope
                                        and (
                                            (
                                                scope[arg.value]
                                                in [
                                                    (
                                                        str(a)
                                                        if type(a) is types.GenericAlias
                                                        else (a if type(a) is str else a.__name__)
                                                    )
                                                    for a in ARG_TYPES[i]
                                                ]
                                            )
                                            or scope[arg.value] == "any"
                                        )
                                        or (
                                            arg.value in pyg3a.Main.func_types
                                            and pyg3a.Main.func_types[arg.value]
                                            in [
                                                (
                                                    (
                                                        str(a[0])
                                                        if (
                                                            type(a[0]) is types.GenericAlias
                                                            or a[0] is None
                                                        )
                                                        else (
                                                            a[0]
                                                            if type(a[0]) is str
                                                            else a[0].__name__
                                                        )
                                                    ),
                                                    a[1],
                                                )
                                                for a in ARG_TYPES[i]
                                            ]
                                        )
                                    )
                                )
                                or (
                                    type(arg) is cst.Call
                                    and (
                                        Block._obj_to_c_str(arg.func) in pyg3a.Main.func_types
                                        and type(arg.func) is cst.Name
                                        and pyg3a.Main.func_types[arg.func.value][0]
                                        in [
                                            str(a)
                                            if (type(a) is types.GenericAlias or a is None)
                                            else (a if type(a) is str else a.__name__)
                                            for a in ARG_TYPES[i]
                                        ],
                                    )
                                )
                                or (
                                    type(arg) is cst.Lambda
                                    and type(ARG_TYPES[i][0]) is tuple
                                    and all(
                                        [
                                            Block._type(
                                                Block._obj_to_c_str(
                                                    arg.params.params[j].name, scope=scope
                                                ),
                                                scope,
                                                False,
                                            )
                                            == (param if type(param) is str else param.__name__)
                                            for j, param in enumerate(ARG_TYPES[i][0][1])
                                        ]
                                    )
                                )
                                for i, arg in enumerate([arg.value for arg in obj.args])
                            ]
                        )

                    globs: dict = {
                        "cst": cst,
                        "_obj_to_c_str": lambda o, isType=False, generateVoidLambda=False: Block._obj_to_c_str(
                            o, isType, generateVoidLambda, scope=scope
                        ),
                        "_const_to_py_obj": Block._const_to_py_obj,
                        "_registry": pyg3a.Main.registry.copy(),
                        "CST_TO_C_EQV": Block.CST_TO_C_EQV.copy(),
                        "scope": scope.copy(),
                        "random": random,
                        "_add_c_func": pyg3a.PyG3A._add_c_func,
                        "types": types,
                        "logging": logging,
                        "_import": pyg3a.PyG3A._import,
                        "_gen_arg_str": pyg3a.PyG3A._gen_arg_str,
                        "_correct_arg_types": _correct_arg_types,
                        "NAME": obj.func.value,
                    }

                    exec(pyg3a.Main.project.custom_funcs["__pyg3a_" + obj.func.value], globs)
                    try:
                        return globs[f"__pyg3a_{obj.func.value}"](obj)
                    except Exception as e:
                        raise type(e)(f"'{pyg3a.PyG3A._cst_to_code(obj)}': {e.args[0]}") from None

                return f"{obj.func.value}({', '.join([Block._obj_to_c_str(a.value, scope=scope) for a in obj.args])})"
            if type(obj) is cst.Name:
                if obj.value in ("True", "False", "None"):
                    return Block._obj_to_c_str(Block._const_to_py_obj(obj), isType)
                if isType is True and obj.value in pyg3a.Main.registry:
                    return pyg3a.Main.registry[obj.value]
                return obj.value
            if isinstance(obj, Block._const_to_py_obj.__annotations__["const"]):
                return Block._obj_to_c_str(Block._const_to_py_obj(obj), isType)
            if type(obj) is cst.Subscript:
                if len(obj.slice) > 1:
                    raise SyntaxError(
                        f"'{pyg3a.PyG3A._cst_to_code(obj)}': You can only have one subscript"
                    )
                if type(obj.slice[0].slice) is not cst.Index:
                    raise SyntaxError("There is no support for slices")
                if type(obj.value) is cst.Name and type(obj.slice[0].slice.value) is cst.Name:
                    if isType and obj.value.value == "list":
                        pyg3a.PyG3A._import("list.hpp")
                        if obj.slice[0].slice.value.value in pyg3a.Main.registry.C_STRINGS:
                            return "List<char>"
                        return f"List<{pyg3a.Main.registry[obj.slice[0].slice.value.value]}>"
                    if isType and obj.value.value == "tuple":
                        if obj.slice[0].slice.value.value in pyg3a.Main.registry.C_STRINGS:
                            return f"char"
                        return f"{pyg3a.Main.registry[obj.slice[0].slice.value.value]}"
                return f"{Block._obj_to_c_str(obj.value, isType, scope=scope)}[{Block._obj_to_c_str(obj.slice[0].slice.value, scope=scope)}]"
            if type(obj) is cst.Attribute:
                if type(obj.attr is cst.Name):
                    return f"{Block._obj_to_c_str(obj.value, scope=scope)}.{obj.attr.value}"
            if type(obj) is cst.Comparison:
                return Block.CST_TO_C_EQV[cst.And].join(
                    [
                        f"{Block._obj_to_c_str(obj.left, scope=scope)} {Block.CST_TO_C_EQV[type(obj.comparisons[i].operator)]} ({Block._obj_to_c_str(obj.comparisons[i].comparator, scope=scope)})"
                        for i in range(len(obj.comparisons))
                    ]
                )
            if type(obj) is cst.BooleanOperation:
                return f"({Block._obj_to_c_str(obj.left, scope=scope)}) {Block.CST_TO_C_EQV[type(obj.operator)]} ({Block._obj_to_c_str(obj.right, scope=scope)})"
            if type(obj) is cst.BinaryOperation:
                if type(obj.operator) is cst.Power:
                    if "math.h" not in pyg3a.Main.project.imports:
                        pyg3a.Main.project.imports.append("math.h")
                    return f"pow({Block._obj_to_c_str(obj.left, scope=scope)}, {Block._obj_to_c_str(obj.right, scope=scope)})"
                if type(obj.operator) is cst.FloorDivide:
                    if "math.h" not in pyg3a.Main.project.imports:
                        pyg3a.Main.project.imports.append("math.h")

                    if (
                        Block._type(obj.left, scope=scope) in pyg3a.Main.registry.INTEGERS
                        and Block._type(obj.right, scope=scope) in pyg3a.Main.registry.INTEGERS
                    ):
                        return f"(({Block._obj_to_c_str(obj.left, scope=scope)}) / ({Block._obj_to_c_str(obj.right, scope=scope)}))"

                    return f"(float) ((int) (({Block._obj_to_c_str(obj.left, scope=scope)}) / ({Block._obj_to_c_str(obj.right, scope=scope)})))"

                if (
                    Block._type(obj.left, scope, False) in pyg3a.Main.registry.PY
                    and Block._type(obj.right, scope, False) in pyg3a.Main.registry.PY
                ):
                    return f"({Block._obj_to_c_str(obj.left, scope=scope)} {Block.CST_TO_C_EQV[type(obj.operator)]} {Block._obj_to_c_str(obj.right, scope=scope)})"

                raise SyntaxError(
                    f"'{pyg3a.PyG3A._cst_to_code(obj)}': Unsupported types {Block._type(obj.left, scope, False)} and {Block._type(obj.right, scope, False)} for operation {type(obj.operator).__name__}"
                )
            if type(obj) is cst.UnaryOperation:
                return f"{Block.CST_TO_C_EQV[type(obj.operator)]} ({Block._obj_to_c_str(obj.expression, scope=scope)})"
            if type(obj) is cst.NamedExpr:
                if type(obj.target) is cst.Name and obj.target.value not in scope:
                    raise SyntaxError(
                        f"type of variable '{obj.target.value}' must be defined in scope"
                    )
                elif (
                    type(obj.target) is cst.Subscript
                    and type(obj.target.value) is cst.Name
                    and obj.target.value.value not in scope
                ):
                    raise SyntaxError(
                        f"type of variable '{obj.target.value.value}' must be defined in scope"
                    )
                return f"{Block._obj_to_c_str(obj.target, scope=scope)} = {Block._obj_to_c_str(obj.value, scope=scope)}"
            if type(obj) is cst.Lambda:
                args: list[str] = [f"auto {param.name.value}" for param in obj.params.params]
                new_scope = scope.copy()
                for param in obj.params.params:
                    new_scope[param.name.value] = "any"
                stmt: str = Block._obj_to_c_str(obj.body, scope=new_scope)
                if generateVoidLambda:
                    return f"[]({', '.join(args)}){{{stmt};}}"
                return f"[]({', '.join(args)}){{return {stmt};}}"
            if type(obj) is cst.IfExp:
                return f"({Block._obj_to_c_str(obj.test, scope=scope)}) ? {Block._obj_to_c_str(obj.body, scope=scope)} : {Block._obj_to_c_str(obj.orelse, scope=scope)}"
            if type(obj) is cst.Set or type(obj) is cst.Tuple:
                return f"{{{', '.join([Block._obj_to_c_str(elt.value, scope=scope) for elt in obj.elements])}}}"
        return str(obj)

    def construct(self, nested_if: bool = False):
        lines: list[str] = []
        for exprc in self.exprs:
            expr: cst.CSTNode = exprc

            if type(expr) is cst.Expr:
                if (
                    type(expr.value) is cst.Call
                    and type(expr.value.func) is cst.Name
                    and Block._obj_to_c_str(expr.value.func) == "raw_c"
                    and len(expr.value.args) == 1
                    and type(expr.value.args[0]) is cst.Arg
                    and isinstance(expr.value.args[0].value, cst.BaseString)
                ):
                    lines.append(f"{self.tabs}{expr.value.args[0].value};")
                else:
                    lines.append(f"{self.tabs}{Block._obj_to_c_str(expr.value, scope=self.scope)};")
            elif type(expr) is cst.Assign or (
                type(expr) is cst.AnnAssign and type(expr.target) is cst.Name
            ):
                annotation: str = ""
                c_annotation: str = ""
                targets: list[cst.BaseAssignTargetExpression] = (
                    [expr.target]
                    if type(expr) is cst.AnnAssign
                    else [target.target for target in expr.targets]
                )

                for target in targets:
                    if type(expr) is cst.AnnAssign:
                        if (
                            type(expr.annotation.annotation) is cst.Subscript
                            and type(expr.annotation.annotation.value) is cst.Name
                            and len(expr.annotation.annotation.slice) == 1
                            and type(expr.annotation.annotation.slice[0].slice) is cst.Index
                            and type(expr.annotation.annotation.slice[0].slice.value) is cst.Name
                        ):
                            annotation = f"{expr.annotation.annotation.value.value}[{expr.annotation.annotation.slice[0].slice.value.value}]"
                        elif type(expr.annotation.annotation) is cst.Name:
                            annotation = expr.annotation.annotation.value

                        c_annotation = Block._obj_to_c_str(
                            expr.annotation.annotation, True, scope=self.scope
                        )
                    else:
                        if type(target) is cst.Name and target.value not in self.scope:
                            annotation = Block._type(expr.value, self.scope, False)

                            if annotation == "any":
                                logging.warning(
                                    f"Type of '{pyg3a.PyG3A._cst_to_code(target)}' not be determined - automatically set to any"
                                )

                            if annotation in pyg3a.Main.registry:
                                c_annotation = pyg3a.Main.registry[annotation]
                            else:
                                c_annotation = Block._obj_to_c_str(
                                    cst.parse_expression(annotation), True, scope=self.scope
                                )
                        elif (
                            type(target) is cst.Subscript
                            and type(target.value) is cst.Name
                            and target.value.value not in self.scope
                        ):
                            raise SyntaxError(
                                f"Type of '{pyg3a.PyG3A._cst_to_code(target.value)}' not defined in scope"
                            )

                    if type(target) is cst.Tuple:
                        tmp_var: str = Block._gen_tmp_var(self.scope, "tuple_unpack")
                        lines.append(
                            f"{self.tabs}auto {tmp_var} = {Block._obj_to_c_str(expr.value, scope=self.scope)};"
                        )
                        for i, elt in enumerate(target.elements):
                            if type(elt.value) is cst.Name:
                                if elt.value.value == "_":
                                    continue

                                if elt.value.value not in self.scope:
                                    raise SyntaxError(
                                        f"type of variable '{elt.value.value}' must be defined in scope"
                                    )

                                if (
                                    Block._obj_to_c_str(
                                        self.scope[elt.value.value], True, scope=self.scope
                                    )[-1]
                                    == "*"
                                ):
                                    if "stddef.h" not in pyg3a.Main.project.imports:
                                        pyg3a.Main.project.imports.append("stddef.h")
                                    lines.append(
                                        f"{self.tabs}if ({elt.value.value} != NULL) free({elt.value.value});"
                                    )

                                if self.scope[elt.value.value] in pyg3a.Main.registry.C_STRINGS:
                                    if "string.h" not in pyg3a.Main.project.imports:
                                        pyg3a.Main.project.imports.append("string.h")
                                    lines.append(
                                        f"{self.tabs}strcpy({elt.value.value}, {tmp_var}._{i});"
                                    )
                                else:
                                    lines.append(
                                        f"{self.tabs}{Block._obj_to_c_str(elt.value, scope=self.scope)} = {tmp_var}._{i};"
                                    )
                            else:
                                lines.append(
                                    f"{self.tabs}{Block._obj_to_c_str(elt.value, scope=self.scope)} = {tmp_var}._{i};"
                                )
                    else:
                        if (type(target) is cst.Name and target.value in self.scope) or (
                            type(target) is cst.Subscript
                            and type(target.value) is cst.Name
                            and target.value.value in self.scope
                        ):
                            if (
                                type(target) is cst.Name
                                and self.scope[target.value] in pyg3a.Main.registry
                                and pyg3a.Main.registry[self.scope[target.value]][-1] == "*"
                            ):
                                if "stddef.h" not in pyg3a.Main.project.imports:
                                    pyg3a.Main.project.imports.append("stddef.h")
                                lines.append(
                                    f"{self.tabs}if ({target.value} != NULL) free({target.value});"
                                )
                            if (
                                type(target) is cst.Name
                                and self.scope[target.value] in pyg3a.Main.registry.C_STRINGS
                            ):
                                if "string.h" not in pyg3a.Main.project.imports:
                                    pyg3a.Main.project.imports.append("string.h")
                                lines.append(
                                    f"{self.tabs}strcpy({target.value}, {Block._obj_to_c_str(expr.value, scope=self.scope)});"
                                )
                            else:
                                lines.append(
                                    f"{self.tabs}{Block._obj_to_c_str(target, scope=self.scope)} = {Block._obj_to_c_str(expr.value, scope=self.scope)};"
                                )
                        elif type(target) is cst.Name:
                            if (
                                type(expr.value) is cst.Name
                                and expr.value.value == "None"
                                and annotation not in pyg3a.Main.registry
                            ):
                                lines.append(f"{self.tabs}{c_annotation} {target.value};")
                            else:
                                if annotation == "cstr":
                                    if (
                                        type(expr.value) is cst.Name and expr.value.value != "None"
                                    ) or type(expr.value) is not cst.Name:
                                        self.scope[target.value] = "conststr"
                                        lines.append(
                                            f"{self.tabs}const char* {target.value} = {Block._obj_to_c_str(expr.value, scope=self.scope)};"
                                        )
                                    else:
                                        self.scope[target.value] = "arrstr"
                                        if (
                                            type(expr.value) is cst.Name
                                            and expr.value.value == "None"
                                        ):
                                            lines.append(f"{self.tabs}char {target.value}[257];")
                                        else:
                                            lines.append(
                                                f"{self.tabs}char* {target.value} = {Block._obj_to_c_str(expr.value, scope=self.scope)};"
                                            )
                                elif "[" in annotation and annotation[:5] == "tuple":
                                    tuple_val: str = Block._obj_to_c_str(
                                        expr.value, scope=self.scope
                                    )
                                    tuple_size: int = 0

                                    if tuple_val[0] == "{" and tuple_val[-1] == "}":
                                        tuple_size = len(
                                            [
                                                int(i)
                                                for i in tuple_val[1:-1].replace(" ", "").split(",")
                                            ]
                                        )

                                    lines.append(
                                        f"{self.tabs}{c_annotation} {target.value}[{tuple_size}] = {tuple_val};"
                                    )
                                else:
                                    lines.append(
                                        f"{self.tabs}{c_annotation} {target.value} = {Block._obj_to_c_str(expr.value, scope=self.scope)};"
                                    )

                        if len(annotation) > 0 and type(target) is cst.Name:
                            self.scope[target.value] = annotation
            elif type(expr) is cst.AugAssign:
                if type(expr.target) is cst.Name and expr.target.value not in self.scope:
                    raise SyntaxError(f"variable '{expr.target.value}' must be defined in scope")
                elif (
                    type(expr.target) is cst.Subscript
                    and type(expr.target.value) is cst.Name
                    and expr.target.value.value not in self.scope
                ):
                    raise SyntaxError(
                        f"variable '{expr.target.value.value}' must be defined in scope"
                    )

                if type(expr.operator) is cst.FloorDivideAssign:
                    lines.append(
                        f"{self.tabs}{Block._obj_to_c_str(expr.target, scope=self.scope)} = {Block._obj_to_c_str(cst.BinaryOperation(left=expr.target, operator=cst.FloorDivide(), right=expr.value), scope=self.scope)};"
                    )
                else:
                    lines.append(
                        f"{self.tabs}{Block._obj_to_c_str(expr.target, scope=self.scope)} {Block.CST_TO_C_EQV[type(expr.operator)]} {Block._obj_to_c_str(expr.value, scope=self.scope)};"
                    )
            elif type(expr) is cst.If:
                if not nested_if:
                    lines.append(
                        f"{self.tabs}if ({Block._obj_to_c_str(expr.test, scope=self.scope)}) {{"
                    )

                expressions: Block = Block(expr.body.body, self.tabnum + 1, self.scope)
                lines.append(expressions.construct())

                if expr.orelse is not None:
                    if type(expr.orelse) is cst.If:
                        lines.append(
                            f"{self.tabs}}} else if ({Block._obj_to_c_str(expr.orelse.test, scope=self.scope)}) {{"
                        )
                        expressions = Block(expr.orelse.body.body, self.tabnum, self.scope)
                        lines.append(expressions.construct(nested_if=True))
                    else:
                        lines.append(f"{self.tabs}}} else {{")
                        expressions = Block(expr.orelse.body.body, self.tabnum + 1, self.scope)
                        lines.append(expressions.construct())

                if not nested_if:
                    lines.append(f"{self.tabs}}}")
            elif type(expr) is cst.While:
                lines.append(
                    f"{self.tabs}while ({Block._obj_to_c_str(expr.test, scope=self.scope)}) {{"
                )

                expressions = Block(expr.body.body, self.tabnum + 1, self.scope)
                lines.append(expressions.construct())

                lines.append(f"{self.tabs}}}")
            elif type(expr) is cst.Return:
                if expr.value is None:
                    lines.append(f"{self.tabs}return;")
                else:
                    if (
                        type(expr.value) is cst.Name
                        and expr.value.value not in ("None", "True", "False")
                        and self.scope[expr.value.value]
                        in (
                            "mutstr",
                            "arrstr",
                        )
                    ):
                        if "stdlib.h" not in pyg3a.Main.project.imports:
                            pyg3a.Main.project.imports.append("stdlib.h")

                        tmp_name: str = Block._gen_tmp_var(self.scope, "ret_str")
                        lines.append(
                            f"{self.tabs}char* {tmp_name} = (char*) malloc(sizeof {expr.value.value});"
                        )
                        lines.append(f"{self.tabs}strcpy({tmp_name}, {expr.value.value});")
                        lines.append(f"{self.tabs}return {tmp_name};")
                    elif type(expr.value) is cst.Name and expr.value.value == "None":
                        lines.append(f"{self.tabs}return;")
                    else:
                        lines.append(
                            f"{self.tabs}return {Block._obj_to_c_str(expr.value, scope=self.scope)};"
                        )
            elif type(expr) is cst.For:
                if (
                    type(expr.iter) is cst.Call
                    and type(expr.iter.func) is cst.Name
                    and "__for_pyg3a_" + expr.iter.func.value in pyg3a.Main.project.custom_funcs
                ):
                    globs: dict = {
                        "cst": cst,
                        "_obj_to_c_str": lambda o, isType=False, generateVoidLambda=False: Block._obj_to_c_str(
                            o, isType, generateVoidLambda, scope=self.scope
                        ),
                        "_const_to_py_obj": Block._const_to_py_obj,
                        "_registry": pyg3a.Main.registry.copy(),
                        "CST_TO_C_EQV": Block.CST_TO_C_EQV.copy(),
                        "random": random,
                        "_add_c_func": pyg3a.PyG3A._add_c_func,
                        "types": types,
                        "logging": logging,
                        "_import": pyg3a.PyG3A._import,
                        "NAME": expr.iter.func.value,
                    }

                    exec(
                        pyg3a.Main.project.custom_funcs["__for_pyg3a_" + expr.iter.func.value],
                        globs,
                    )
                    lines.extend(
                        [
                            self.tabs + line
                            for line in globs[f"__for_pyg3a_{expr.iter.func.value}"](
                                expr, self.scope
                            )
                        ]
                    )

                    new_scope = self.scope.copy()
                else:
                    arr_name: str = Block._gen_tmp_var(self.scope, "for_arr")
                    iter_name: str = Block._gen_tmp_var(self.scope, "for_iter")

                    iter_str: str = Block._obj_to_c_str(expr.iter, scope=self.scope)
                    if iter_str[0] == "{" and iter_str[-1] == "}":
                        iter_items: list[str] = iter_str[1:-1].replace(" ", "").split(",")
                        lines.append(
                            f"{self.tabs}decltype({iter_items[0]}) {arr_name}[{len(iter_items)}] = {iter_str};"
                        )
                    else:
                        lines.append(f"{self.tabs}auto {arr_name} = {iter_str};")

                    lines.append(
                        f"{self.tabs}for (unsigned int {iter_name} = 0; {iter_name} < sizeof {arr_name}; {iter_name}++) {{"
                    )

                    if type(expr.target) is cst.Name:
                        target_type: str = "auto"
                        if (
                            type(expr.iter) is cst.Name
                            and Block._type(expr.iter, self.scope)[0:6] == "tuple["
                            and Block._type(expr.iter, self.scope)[-1] == "]"
                        ):
                            target_type = Block._type(expr.iter.value, self.scope)[6:-1]

                        lines.append(
                            f"{self.tabs}\t{target_type} {expr.target.value} = {arr_name}[{iter_name}];"
                        )

                        new_scope = self.scope.copy()
                        new_scope[expr.target.value] = (
                            target_type if target_type != "auto" else "any"
                        )

                expressions = Block(expr.body.body, self.tabnum + 1, new_scope)
                lines.append(expressions.construct())

                lines.append(f"{self.tabs}}}")
            elif type(expr) is cst.Del:
                targets: list[cst.CSTNode] = []
                if type(expr.target) is cst.Tuple:
                    targets.extend([el.value for el in expr.target.elements])
                else:
                    targets.append(expr.target)

                for target_ in targets:
                    if type(target_) is cst.Subscript:
                        raise SyntaxError(
                            f"'{pyg3a.PyG3A._cst_to_code(expr)}': You cannot delete an item of an array."
                        )
                    if (
                        type(target_) is cst.Name
                        and Block._type(target_, self.scope) in pyg3a.Main.registry.C_STRINGS
                    ):
                        pyg3a.PyG3A._import("stddef.h")
                        lines.append(
                            f"{self.tabs}if ({Block._obj_to_c_str(target_, scope = self.scope)} != NULL) free({Block._obj_to_c_str(target_, scope = self.scope)});"
                        )
                    else:
                        raise SyntaxError(
                            f"You cannot delete {Block._obj_to_c_str(target_, scope = self.scope)}"
                        )
            elif type(expr) is cst.Match:

                def _match_case_to_c_str(pattern: cst.pattern) -> str:
                    case_lines: list[str] = []
                    if type(pattern) is cst.MatchValue:
                        case_lines.append(
                            f"{self.tabs}\tcase {Block._obj_to_c_str(pattern.value, scope = self.scope)}:"
                        )
                    elif type(pattern) is cst.MatchAs:
                        if pattern.pattern is None:
                            case_lines.append(f"{self.tabs}\tdefault:")
                        else:
                            case_lines.append(_match_case_to_c_str(pattern.pattern))
                    elif type(pattern) is cst.MatchOr:
                        for option in pattern.patterns:
                            case_lines.append(_match_case_to_c_str(option))
                    else:
                        raise SyntaxError(
                            "Match statements only support: matching values, _ (default), as, | (or)"
                        )
                    return "\n".join(case_lines)

                lines.append(
                    f"{self.tabs}switch ({Block._obj_to_c_str(expr.subject, scope = self.scope)}) {{"
                )
                for case in expr.cases:
                    lines.append(_match_case_to_c_str(case.pattern))
                    lines.append(f"{self.tabs}\t\t{{")

                    if type(case.pattern) is cst.MatchAs and case.pattern.name is not None:
                        lines.append(
                            f"{self.tabs}\t\t\tauto {case.pattern.name} = {Block._obj_to_c_str(expr.subject, scope = self.scope)};"
                        )

                    body: Block = Block(case.body, self.tabnum + 3, self.scope)
                    lines.append(body.construct())
                    lines.append(f"{self.tabs}\t\t\tbreak;")

                    lines.append(f"{self.tabs}\t\t}}")

                if lines[-2] == f"{self.tabs}\t\tbreak;":
                    lines.pop(-2)

                lines.append(f"{self.tabs}}}")
            elif type(expr) is cst.ImportFrom:
                pyg3a.PyG3A._import_module(Block._obj_to_c_str(expr.module))
            elif type(expr) is cst.Import:
                for module in [i.name.value for i in expr.names]:
                    pyg3a.PyG3A._import_module(module)
            elif type(expr) is cst.FunctionDef:
                for func in [
                    fun for fun in pyg3a.Main.project.functions if fun.name == expr.name.value
                ]:
                    if func.name == "main" and not pyg3a.Main.main_function_overridden:
                        pyg3a.Main.main_function_overridden = True
                    else:
                        raise SyntaxError(f"Cannot override function '{func.name}'")

                pyg3a.Main.project.functions.append(pyg3a.Function(expr))
            elif type(expr) in Block.CST_TO_C_EQV:
                lines.append(f"{self.tabs}{Block.CST_TO_C_EQV[type(expr)]};")
        return "\n".join(lines)

    @staticmethod
    def _type(
        item: typing.Any, scope: dict, func_explicit: bool = True, scope_error: bool = True
    ) -> str:
        if type(item) is cst.Name:
            if item.value == "None":
                return "None"
            if item.value in ("True", "False"):
                return "bool"
            if item.value in scope:
                return scope[item.value]
            if item.value in pyg3a.Main.func_types:
                func_type: tuple = pyg3a.Main.func_types[item.value]
                if func_explicit:
                    return f"<function({', '.join(func_type[1])}) returns {func_type[0]}"
                return func_type[0]
            if scope_error:
                raise RuntimeError("Variable not in scope!")
            return "any"
        if isinstance(item, Block._const_to_py_obj.__annotations__["const"]):
            return type(Block._const_to_py_obj(item)).__name__
        if type(item) is cst.Call:
            if type(item.func) is cst.Name and item.func.value in pyg3a.Main.func_types:
                function_type: tuple = pyg3a.Main.func_types[item.func.value]
                if func_explicit:
                    return f"<function({', '.join(function_type[1])}) returns {function_type[0]}"
                return function_type[0]
        if type(item) is cst.Subscript and type(item.value) is cst.Name:
            if (
                type(item.slice[0].slice) is cst.Index
                and type(item.slice[0].slice.value) is cst.Name
                and item.slice[0].slice.value.value not in scope
            ):
                return f"{item.value.value}[{item.slice[0].slice.value.value}]"

            if "[" in (var := Block._type(item.value, scope, False, scope_error)):
                return var[var.find("[") + 1 : -1]
        if type(item) is cst.Lambda:
            if func_explicit:
                return f"<function({', '.join(['auto' for _ in item.params.params])}) returns any>"
            return "any"
        if type(item) is cst.Tuple:
            return f"tuple[{Block._type(item.elements[0].value, scope)}]"
        if type(item) is cst.List:
            return f"list[{Block._type(item.elements[0].value, scope)}]"
        if type(item) is cst.BinaryOperation:
            if (
                Block._type(item.left, scope, False) == "str"
                or Block._type(item.right, scope, False) == "str"
            ):
                return "str"
            elif (
                Block._type(item.left, scope, False) in pyg3a.Main.registry.NUMBERS
                and Block._type(item.right, scope, False) in pyg3a.Main.registry.NUMBERS
            ):
                if type(item.operator) in (
                    cst.Add,
                    cst.Subtract,
                    cst.Multiply,
                    cst.Modulo,
                    cst.Power,
                    cst.FloorDivide,
                ):
                    return (
                        Block._type(item.left, scope)
                        if Block._type(item.left, scope) in pyg3a.Main.registry.FLOATS
                        or Block._type(item.right, scope) in pyg3a.Main.registry.FLOATS
                        else Block._type(item.left, scope)
                    )
                if type(item.operator) is cst.Divide:
                    return "float"
                return Block._type(item.left, scope)
        return "None"

    @staticmethod
    def _gen_tmp_var(scope: dict, name: str = "var") -> str:
        if name in pyg3a.Main.tmp_nums:
            pyg3a.Main.tmp_nums[name] += 1
        else:
            pyg3a.Main.tmp_nums[name] = 0

        temp_name: str = f"__tmp_{name}_" + str(pyg3a.Main.tmp_nums[name])
        if temp_name not in scope:
            return temp_name

        raise RuntimeError(f"Too many temporary variables called {name}! Try using multiple files.")
