#!/usr/bin/env python3

import typing

import libcst as cst

import pyg3a

from .block import Block


class Function:
    def __init__(self, func: cst.FunctionDef):
        self.cst = func

        self.name: str = func.name.value

        self.args: typing.Sequence[cst.Param] = func.params.params

        self.exprs: typing.Sequence[cst.BaseStatement] | typing.Sequence[
            cst.BaseSmallStatement
        ] = func.body.body

        self.ret: str = (
            typing.cast(cst.Name, func.returns.annotation).value
            if type(func.returns) is cst.Annotation
            else ""
        )
        if self.ret == "cstr":
            self.ret = "mutstr"

        missing_annotations: list[str] = []

        pyg3a.Main.func_types[self.name] = (
            self.ret,
            [
                Block._obj_to_c_str(arg.annotation.annotation, True)
                if type(arg.annotation) is cst.Annotation
                else missing_annotations.append(str(i))
                for i, arg in enumerate(self.args)
            ],
        )

        if len(missing_annotations) > 0:
            raise SyntaxError(
                "Missing type annotation on argument(s) "
                + ", ".join(missing_annotations)
                + " of function "
                + self.name
            )

    def __str__(self):
        return f"Function(\n\tname='{self.name}',\n\targs={self.args},\n\texprs={self.exprs},\n\tret='{self.ret}'\n)"

    def __repr__(self):
        return str(self)

    def _str_args(self) -> str:
        args: list[str] = []
        for arg in self.args:
            assert type(arg.annotation) is cst.Annotation
            args.append(f"{Block._obj_to_c_str(arg.annotation.annotation, True)} {arg.name.value}")

        return ", ".join(args)

    def construct(self):
        lines: list[str] = []

        scope: dict[str, str] = {}
        for arg in self.args:
            assert type(arg.annotation) is cst.Annotation
            scope[arg.name.value] = Block._obj_to_c_str(arg.annotation.annotation)

        block: Block = Block(self.exprs, 1, scope)
        lines.append(block.construct())

        if self.ret == "":
            self.ret = "None"
            self.cst.visit(FunctionVisitor(self, block.scope))
            pyg3a.Main.func_types[self.name] = (self.ret, pyg3a.Main.func_types[self.name][1])

        lines.insert(0, f"{pyg3a.Main.registry[self.ret]} {self.name}({self._str_args()}) {{")

        if self.name == "main":
            tmp_var: str = Block._gen_tmp_var(scope, "key")
            pyg3a.PyG3A._import("fxcg/keyboard.h")
            lines.append(f"\tint {tmp_var}; while (1) GetKey(&{tmp_var});")

        lines.append("}")
        return "\n".join(lines)


class FunctionVisitor(cst.CSTVisitor):
    def __init__(self, func: Function, scope: dict):
        self.func = func
        self.scope = scope

    def visit_Return(self, node: cst.Return) -> None:
        self.func.ret = Block._type(node.value, self.scope, False, False)
        if self.func.ret == "any":
            logging.warning(
                f"Return type of '{self.func.name}' could not be determined - automatically set to any"
            )
