#!/usr/bin/env python3.10

import argparse
import ast
import logging
import os
import random
import shutil
import subprocess
import sys
import types
import typing

import colorlog
import libcst as cst

ellipsis: typing.TypeAlias = type(Ellipsis)


def _add_c_func(name: str, c: str) -> None:
    Main.project.extra_funcs[name] = c


def _import(name: str) -> None:
    if name not in Main.project.imports:
        Main.project.imports.append(name)


def _import_module(module_name: str) -> None:
    if module_name in Main.project.modules:
        return

    fname: str = ""
    for loc in Main.package_locs:
        if os.path.exists(os.path.join(loc, module_name + ".py")):
            fname = os.path.join(loc, module_name + ".py")

    if fname == "":
        return

    with open(fname, "r") as f:
        contents = f.read()
        for stmt in cst.parse_module(contents).body:
            if type(stmt) is cst.FunctionDef and (
                stmt.name.value[:8] == "__pyg3a_" or stmt.name.value[:12] == "__for_pyg3a_"
            ):
                Main.project.custom_funcs[stmt.name.value] = _cst_to_code(stmt)
            elif type(stmt) is cst.FunctionDef and stmt.name.value == "__types_pyg3a":
                extra_func_globs: dict = {}
                exec(_cst_to_code(stmt), extra_func_globs)
                for item in extra_func_globs["__types_pyg3a"]().items():
                    Main.func_types[item[0]] = (item[1], [])
            elif type(stmt) is cst.SimpleStatementLine:
                for line in stmt.body:
                    if type(line) is cst.Import:
                        for alias in line.names:
                            for loc in [
                                os.path.join(Main.libfxcg, "include"),
                                "include",
                            ]:
                                if os.path.isfile(
                                    os.path.join(
                                        loc,
                                        Block._obj_to_c_str(alias.name).replace(".", "/") + ".hpp",
                                    )
                                ):
                                    _import(
                                        Block._obj_to_c_str(alias.name).replace(".", "/") + ".hpp"
                                    )
                                elif os.path.isfile(
                                    os.path.join(
                                        loc,
                                        Block._obj_to_c_str(alias.name).replace(".", "/") + ".h",
                                    )
                                ):
                                    _import(
                                        Block._obj_to_c_str(alias.name).replace(".", "/") + ".h"
                                    )
                    elif type(line) is cst.ImportFrom and type(line.module) is not None:
                        for loc in (Main.libfxcg, "include"):
                            if os.path.isfile(
                                os.path.join(
                                    loc,
                                    Block._obj_to_c_str(line.module).replace(".", "/") + ".hpp",
                                )
                            ):
                                _import(Block._obj_to_c_str(line.module).replace(".", "/") + ".hpp")
                            elif os.path.isfile(
                                os.path.join(
                                    loc,
                                    Block._obj_to_c_str(line.module).replace(".", "/") + ".h",
                                )
                            ):
                                _import(Block._obj_to_c_str(line.module).replace(".", "/") + ".h")

        Main.project.modules.append(module_name)


def _cst_to_code(node: cst.CSTNode) -> str:
    return cst.Module([node]).code


def _gen_arg_str(ARG_TYPES: dict, OPTIONAL_ARGS: dict):
    return ", ".join(
        [
            "|".join(
                [
                    (
                        str(a)
                        if type(a) is types.GenericAlias
                        else (
                            a
                            if type(a) is str
                            else (
                                f"<function({', '.join([Block._obj_to_c_str(o, True) for o in a[1]])}) returns {str(a[0]) if (type(a[0]) is types.GenericAlias or a[0] is None) else a[0].__name__}>"
                                if type(a) is tuple
                                else a.__name__
                            )
                        )
                    )
                    + ("?" if arg in OPTIONAL_ARGS else "")
                    for a in ARG_TYPES[arg]
                ]
            )
            for arg in ARG_TYPES.keys()
        ]
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pyFile", type=str, nargs=1, help="name of python file to convert")
    parser.add_argument("-l", dest="libfxcg", type=str, nargs=1, help="libfxcg location")
    parser.add_argument("--debug", dest="debug", action="store_true", help="use debug mode")
    parser.add_argument(
        "--verbose", dest="verbose", action="store_true", help="print command names in make"
    )
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    colorlog.basicConfig(format="\033[1m%(log_color)s%(levelname)s:\033[39m %(message)s")

    if os.path.isfile(args.pyFile[0]):
        Main.project = Project(os.path.splitext(os.path.basename(args.pyFile[0]))[0])
        Main.libfxcg = os.path.abspath(args.libfxcg[0])
        Main.verbose = args.verbose

        if os.path.exists("selected.bmp") and os.path.exists("unselected.bmp"):
            Main.project.create()
        else:
            Main.project.create(
                os.path.join(os.path.dirname(__file__), "selected.bmp"),
                os.path.join(os.path.dirname(__file__), "unselected.bmp"),
            )

        Main.project.load(args.pyFile[0])
        Main.project.write()
        try:
            Main.project.make()
        except subprocess.CalledProcessError as e:
            sys.exit(e.returncode)


class Project:
    def __init__(self, name: str):
        self.name = name
        self.c = ""

    def write(self):
        try:
            main = open(f".pyg3a_build/{self.name}/src/main.cpp", "w")
            main.write(self.c)
            main.close()
        except FileNotFoundError as err:
            raise RuntimeError("Please run create() first") from None

    def create(
        self,
        sel_loc: str = "selected.bmp",
        unsel_loc: str = "unselected.bmp",
    ):
        if os.path.exists(f".pyg3a_build/{self.name}/src/"):
            return

        os.makedirs(f".pyg3a_build/{self.name}/src/", exist_ok=True)

        makefile = open(f".pyg3a_build/{self.name}/Makefile", "w")
        makefile.write(
            ".SUFFIXES:\n"
            + f"export FXCGSDK := $(abspath {Main.libfxcg})\n"
            + "include $(FXCGSDK)/toolchain/prizm_rules\n"
            + ("export CXX    := @$(CXX)\n" if not Main.verbose else "")
            + ("export MKG3A  := @$(MKG3A)\n" if not Main.verbose else "")
            + """TARGET		:=	$(notdir $(CURDIR))
BUILD		:=	build
SOURCES		:=	src
DATA		:=	data
"""
            + f"INCLUDES := {os.path.dirname(os.path.abspath(__file__))}/include\n"
            + f"MKG3AFLAGS := -n basic:{self.name} -i uns:{os.path.abspath(unsel_loc)} -i sel:{os.path.abspath(sel_loc)}"
            + """
CFLAGS	= -Os -Wall $(MACHDEP) $(INCLUDE) -ffunction-sections -fdata-sections -fno-exceptions
CXXFLAGS	=	$(CFLAGS)

LDFLAGS	= $(MACHDEP) -T$(FXCGSDK)/toolchain/prizm.x -Wl,-static -Wl,-gc-sections -fno-exceptions

LIBS	:=	 -lc -lfxcg -lgcc
"""
            + f"LIBDIRS	:= {os.path.dirname(os.path.abspath(__file__))}"
            + """
ifneq ($(BUILD),$(notdir $(CURDIR)))

export OUTPUT	:=	$(CURDIR)/$(TARGET)

export VPATH	:=	$(foreach dir,$(SOURCES),$(CURDIR)/$(dir)) 					$(foreach dir,$(DATA),$(CURDIR)/$(dir))

export DEPSDIR	:=	$(CURDIR)/$(BUILD)

CFILES		:=	$(foreach dir,$(SOURCES),$(notdir $(wildcard $(dir)/*.c)))
CPPFILES	:=	$(foreach dir,$(SOURCES),$(notdir $(wildcard $(dir)/*.cpp)))
sFILES		:=	$(foreach dir,$(SOURCES),$(notdir $(wildcard $(dir)/*.s)))
SFILES		:=	$(foreach dir,$(SOURCES),$(notdir $(wildcard $(dir)/*.S)))
BINFILES	:=	$(foreach dir,$(DATA),$(notdir $(wildcard $(dir)/*.*)))

ifeq ($(strip $(CPPFILES)),)
	export LD	:=	$(CC)
else
	export LD	:=	$(CXX)
endif

export OFILES	:=	$(addsuffix .o,$(BINFILES)) 					$(CPPFILES:.cpp=.o) $(CFILES:.c=.o) 					$(sFILES:.s=.o) $(SFILES:.S=.o)

export INCLUDE	:=	$(foreach dir,$(INCLUDES), -iquote $(CURDIR)/$(dir)) 					$(foreach dir,$(LIBDIRS),-I$(dir)/include) 					-I$(CURDIR)/$(BUILD) -I$(LIBFXCG_INC)

export LIBPATHS	:=	$(foreach dir,$(LIBDIRS),-L$(dir)/lib) 					-L$(LIBFXCG_LIB)

export OUTPUT	:=	$(CURDIR)/$(TARGET)
.PHONY: all clean

all: $(BUILD)
	@make --no-print-directory -C $(BUILD) -f $(CURDIR)/Makefile

$(BUILD):
	@mkdir $@

export CYGWIN := nodosfilewarning
clean:
	$(call rmdir,$(BUILD))
	$(call rm,$(OUTPUT).bin)
	$(call rm,$(OUTPUT).g3a)

else

DEPENDS	:=	$(OFILES:.o=.d)

$(OUTPUT).g3a: $(OUTPUT).bin
$(OUTPUT).bin: $(OFILES)


-include $(DEPENDS)

endif
"""
        )
        makefile.close()

    def make(self):
        try:
            if os.path.isfile(f".pyg3a_build/{self.name}/Makefile"):
                subprocess.run(["/bin/make"], cwd=f".pyg3a_build/{self.name}", check=True)
            else:
                raise RuntimeError("Please run write() first")
        except FileNotFoundError:
            raise RuntimeError("Please run create() first") from None

        try:
            shutil.copyfile(
                os.path.abspath(f".pyg3a_build/{self.name}/{self.name}.g3a"), f"{self.name}.g3a"
            )
        except FileNotFoundError:
            raise err

    def load(self, filename: str):
        py_file = open(filename, "r")
        parsed: cst.Module = cst.parse_module(py_file.read())
        py_file.close()

        self.functions: list[Function] = [
            Function(
                cst.FunctionDef(
                    name=cst.Name(value="main"),
                    params=cst.Parameters(params=[]),
                    body=cst.IndentedBlock(body=parsed.body),
                    returns=cst.Annotation(annotation=cst.Name(value="int")),
                )
            )
        ]
        self.modules: list[str] = []
        self.imports: list[str] = ["str.hpp"]
        self.custom_funcs: dict[str, str] = {}
        self.extra_funcs: dict = {}

        lines: list[str] = []
        func_lines: dict[str, str] = {}

        _import_module("stdpy")

        for func in self.functions:
            func_lines[func.name] = func.construct() + "\n"

        if logging.root.level == logging.DEBUG:
            lines.append("/* --- Imports --- */\n")

        for imp in self.imports:
            lines.append(f"#include <{imp}>")
        lines.append("")

        if logging.root.level == logging.DEBUG:
            lines.append("/* --- Package helpers --- */\n")

        lines.append("\n\n".join(self.extra_funcs.values()))
        lines.append("")

        if logging.root.level == logging.DEBUG:
            lines.append("/* --- Function declarations --- */\n")

        lines.extend(
            [
                f"{Block.PY_C_TYPES[fun.ret]} {fun.name}({', '.join([Block.PY_C_TYPES[param.annotation.annotation.value] for param in fun.args])});"
                for fun in self.functions
                if fun.name != "main"
            ]
        )
        lines.append("")

        if logging.root.level == logging.DEBUG:
            lines.append("/* --- Functions --- */\n")

        lines.extend(func_lines.values())

        self.c = "\n".join(lines)

        logging.debug(self.c)

        logging.debug("modules: " + ", ".join(self.modules))
        logging.debug("imports: " + ", ".join(self.imports))


class Block:
    PY_C_TYPES = {
        "None": "void",
        "unsint": "unsigned int",
        "int": "int",
        "str": "String",
        "cstr": "const char*",
        "mutstr": "char*",
        "conststr": "const char*",
        "arrstr": "char",
        "unsstr": "unsigned char*",
        "char": "char",
        "any": "auto",
        "float": "float",
    }

    CST_TO_C_EQV = {
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
            _import("stddef.h")
            return "NULL"
        if isinstance(obj, cst.CSTNode):
            if type(obj) is cst.SimpleStatementLine:
                obj = obj.body[0]

            if type(obj) is cst.Call and type(obj.func) is cst.Name:
                if "__pyg3a_" + obj.func.value in Main.project.custom_funcs:

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
                                            arg.value in Main.func_types
                                            and Main.func_types[arg.value]
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
                                        Block._obj_to_c_str(arg.func) in Main.func_types
                                        and type(arg.func) is cst.Name
                                        and Main.func_types[arg.func.value][0]
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
                        "PY_C_TYPES": Block.PY_C_TYPES.copy(),
                        "CST_TO_C_EQV": Block.CST_TO_C_EQV.copy(),
                        "scope": scope.copy(),
                        "random": random,
                        "_add_c_func": _add_c_func,
                        "types": types,
                        "logging": logging,
                        "_import": _import,
                        "_gen_arg_str": _gen_arg_str,
                        "_correct_arg_types": _correct_arg_types,
                        "NAME": obj.func.value,
                        "STR_TYPES": Main.str_types,
                    }

                    exec(Main.project.custom_funcs["__pyg3a_" + obj.func.value], globs)
                    try:
                        return globs[f"__pyg3a_{obj.func.value}"](obj)
                    except Exception as e:
                        raise type(e)(f"'{_cst_to_code(obj)}': {e.args[0]}") from None

                return f"{obj.func.value}({', '.join([Block._obj_to_c_str(a.value, scope=scope) for a in obj.args])})"
            if type(obj) is cst.Name:
                if obj.value in ("True", "False", "None"):
                    return Block._obj_to_c_str(Block._const_to_py_obj(obj), isType)
                if isType is True and obj.value in Block.PY_C_TYPES:
                    return Block.PY_C_TYPES[obj.value]
                return obj.value
            if isinstance(
                obj, tuple([ann for ann in Block._const_to_py_obj.__annotations__.values()])
            ):
                return Block._obj_to_c_str(Block._const_to_py_obj(obj), isType)
            if type(obj) is cst.Subscript:
                if len(obj.slice) > 0:
                    raise SyntaxError("You can only have one subscript")
                if type(obj.slice[0].slice) is not cst.Index:
                    raise SyntaxError("There is no support for slices")
                if type(obj.value) is cst.Name and type(obj.slice[0].slice.value) is cst.Name:
                    if isType and obj.value.value == "list":
                        _import("list.hpp")
                        if obj.slice[0].slice.value.value in Main.str_types:
                            return "List<char>"
                        return f"List<{Block.PY_C_TYPES[obj.slice[0].slice.value.value]}>"
                    if isType and obj.value.value == "tuple":
                        if obj.slice[0].slice.value.value in Main.str_types:
                            return f"char"
                        return f"{Block.PY_C_TYPES[obj.slice[0].slice.value.value]}"
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
                    if "math.h" not in Main.project.imports:
                        Main.project.imports.append("math.h")
                    return f"pow({Block._obj_to_c_str(obj.left, scope=scope)}, {Block._obj_to_c_str(obj.right, scope=scope)})"
                if type(obj.operator) is cst.FloorDivide:
                    if "math.h" not in Main.project.imports:
                        Main.project.imports.append("math.h")
                    if (
                        Block._type(obj.left, scope=scope) == "int"
                        and Block._type(obj.left, scope=scope) == "int"
                    ):
                        return f"(({Block._obj_to_c_str(obj.left, scope=scope)}) / ({Block._obj_to_c_str(obj.right, scope=scope)}))"
                    return f"(float) ((int) (({Block._obj_to_c_str(obj.left, scope=scope)}) / ({Block._obj_to_c_str(obj.right, scope=scope)})))"
                if Block._type(obj.left, scope, False) in ["float", "int", "str"]:
                    return f"({Block._obj_to_c_str(obj.left, scope=scope)} {Block.CST_TO_C_EQV[type(obj.operator)]} {Block._obj_to_c_str(obj.right, scope=scope)})"
                raise SyntaxError(
                    f"Unsupported types {Block._type(obj.left, scope, False)} and {Block._type(obj.right, scope, False)} for operation {type(obj.operator).__name__}"
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
                            annotation = f"{expr.annotation.annotation.value.value}[{expr.annotation.annotation.slice[0].slice.value}]"
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
                                    f"Type of '{_cst_to_code(target)}' not be determined - automatically set to any"
                                )

                            if annotation in Block.PY_C_TYPES:
                                c_annotation = Block.PY_C_TYPES[annotation]
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
                                f"Type of '{_cst_to_code(target.value)}' not defined in scope"
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
                                    if "stddef.h" not in Main.project.imports:
                                        Main.project.imports.append("stddef.h")
                                    lines.append(
                                        f"{self.tabs}if ({elt.value.value} != NULL) free({elt.value.value});"
                                    )

                                if self.scope[elt.value.value] in Main.str_types:
                                    if "string.h" not in Main.project.imports:
                                        Main.project.imports.append("string.h")
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
                                and self.scope[target.value] in Block.PY_C_TYPES
                                and Block.PY_C_TYPES[self.scope[target.value]][-1] == "*"
                            ):
                                if "stddef.h" not in Main.project.imports:
                                    Main.project.imports.append("stddef.h")
                                lines.append(
                                    f"{self.tabs}if ({target.value} != NULL) free({target.value});"
                                )
                            if (
                                type(target) is cst.Name
                                and self.scope[target.value] in Main.str_types
                            ):
                                if "string.h" not in Main.project.imports:
                                    Main.project.imports.append("string.h")
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
                                and annotation not in Block.PY_C_TYPES
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
                        if "stdlib.h" not in Main.project.imports:
                            Main.project.imports.append("stdlib.h")

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
                    and "__for_pyg3a_" + expr.iter.func.value in Main.project.custom_funcs
                ):
                    globs: dict = {
                        "cst": cst,
                        "_obj_to_c_str": lambda o, isType=False, generateVoidLambda=False: Block._obj_to_c_str(
                            o, isType, generateVoidLambda, scope=self.scope
                        ),
                        "_const_to_py_obj": Block._const_to_py_obj,
                        "PY_C_TYPES": Block.PY_C_TYPES.copy(),
                        "CST_TO_C_EQV": Block.CST_TO_C_EQV.copy(),
                        "random": random,
                        "_add_c_func": _add_c_func,
                        "types": types,
                        "logging": logging,
                        "_import": _import,
                        "NAME": expr.iter.func.value,
                        "STR_TYPES": Main.str_types,
                    }

                    exec(Main.project.custom_funcs["__for_pyg3a_" + expr.iter.func.value], globs)
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
                            f"'{_cst_to_code(expr)}': You cannot delete an item of an array."
                        )
                    if (
                        type(target_) is cst.Name
                        and Block._type(target_, self.scope) in Main.str_types
                    ):
                        _import("stddef.h")
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
                _import_module(Block._obj_to_c_str(expr.module))
            elif type(expr) is cst.Import:
                for module in [i.name.value for i in expr.names]:
                    _import_module(module)
            elif type(expr) is cst.FunctionDef:
                for func in [fun for fun in Main.project.functions if fun.name == expr.name.value]:
                    if func.name == "main" and not Main.main_function_overridden:
                        Main.main_function_overridden = True
                    else:
                        raise SyntaxError(f"Cannot override function '{func.name}'")

                Main.project.functions.append(Function(expr))
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
            if item.value in Main.func_types:
                func_type: tuple = Main.func_types[item.value]
                if func_explicit:
                    return f"<function({', '.join(func_type[1])}) returns {func_type[0]}"
                return func_type[0]
            if scope_error:
                raise RuntimeError("Variable not in scope!")
            return "any"
        if isinstance(
            item, tuple([ann for ann in Block._const_to_py_obj.__annotations__.values()])
        ):
            return type(Block._const_to_py_obj(item)).__name__
        if type(item) is cst.Call:
            if type(item.func) is cst.Name and item.func.value in Main.func_types:
                function_type: tuple = Main.func_types[item.func.value]
                if func_explicit:
                    return f"<function({', '.join(function_type[1])}) returns {function_type[0]}"
                return function_type[0]
        if (
            type(item) is cst.Subscript
            and type(item.value) is cst.Name
            and type(item.slice[0].slice) is cst.Index
            and type(item.slice[0].slice.value) is cst.Name
        ):
            return f"{item.value.value}[{item.slice[0].slice.value.value}]"
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
            elif Block._type(item.left, scope, False) in ("int", "float") and Block._type(
                item.right, scope, False
            ) in ("int", "float"):
                if type(item.operator) in (
                    cst.Add,
                    cst.Subtract,
                    cst.Multiply,
                    cst.Modulo,
                    cst.Power,
                    cst.FloorDivide,
                ):
                    return (
                        "float"
                        if Block._type(item.left, scope) == "float"
                        or Block._type(item.right, scope) == "float"
                        else "int"
                    )
                if type(item.operator) is cst.Divide:
                    return "float"
                return "int"
        return "None"

    @staticmethod
    def _gen_tmp_var(scope: dict, name: str = "var") -> str:
        if name in Main.tmp_nums:
            Main.tmp_nums[name] += 1
        else:
            Main.tmp_nums[name] = 0

        temp_name: str = f"__tmp_{name}_" + str(Main.tmp_nums[name])
        if temp_name not in scope:
            return temp_name

        raise RuntimeError(f"Too many temporary variables called {name}! Try using multiple files.")


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

        Main.func_types[self.name] = (
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
            Main.func_types[self.name] = (self.ret, Main.func_types[self.name][1])

        lines.insert(0, f"{Block.PY_C_TYPES[self.ret]} {self.name}({self._str_args()}) {{")

        if self.name == "main":
            tmp_var: str = Block._gen_tmp_var(scope, "key")
            _import("fxcg/keyboard.h")
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


class Main:
    libfxcg: str = "../../"
    verbose: bool = False
    package_locs: list[str] = [
        os.path.join(os.environ["HOME"], ".local", "lib", "pyg3a"),
        os.path.join(os.path.dirname(__file__), "packages"),
    ]
    project: Project = Project("NONE")
    str_types: tuple[str, str, str, str] = ("cstr", "mutstr", "conststr", "arrstr")
    func_types: dict = {}
    main_function_overridden: bool = False
    tmp_nums: dict[str, int] = {}


if __name__ == "__main__":
    main()
