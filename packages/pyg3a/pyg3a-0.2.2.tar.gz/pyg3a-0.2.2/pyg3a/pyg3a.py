#!/usr/bin/env python3.10

import abc
import argparse
import ast
import logging
import os
import shutil
import subprocess
import sys
import typing

import colorlog
import libcst as cst

from .block import Block
from .functions import Function, FunctionVisitor
from .type_registry import RegistryType, TypeRegistry


class PyG3A:
    @staticmethod
    def _add_c_func(name: str, c: str) -> None:
        Main.project.extra_funcs[name] = c

    @staticmethod
    def _import(name: str) -> None:
        if name not in Main.project.imports:
            Main.project.imports.append(name)

    @staticmethod
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
                if type(stmt) is cst.FunctionDef:
                    if stmt.name.value[:8] == "__pyg3a_" or stmt.name.value[:12] == "__for_pyg3a_":
                        Main.project.custom_funcs[stmt.name.value] = PyG3A._cst_to_code(stmt)
                    elif stmt.name.value == "__types_pyg3a":
                        extra_func_globs: dict = {}
                        exec(PyG3A._cst_to_code(stmt), extra_func_globs)
                        for item in extra_func_globs["__types_pyg3a"]().items():
                            Main.func_types[item[0]] = (item[1], [])
                    elif stmt.name.value == "__registry_types_pyg3a":
                        extra_types_globs: dict = {"RegistryType": RegistryType}
                        exec(PyG3A._cst_to_code(stmt), extra_types_globs)
                        for item in extra_types_globs["__registry_types_pyg3a"]().items():
                            if len(item[1]) > 1:
                                Main.registry.register(item[0], item[1][0], item[1][1])
                            else:
                                Main.registry.register(item[0], item[1][0])
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
                                            Block._obj_to_c_str(alias.name).replace(".", "/")
                                            + ".hpp",
                                        )
                                    ):
                                        PyG3A._import(
                                            Block._obj_to_c_str(alias.name).replace(".", "/")
                                            + ".hpp"
                                        )
                                    elif os.path.isfile(
                                        os.path.join(
                                            loc,
                                            Block._obj_to_c_str(alias.name).replace(".", "/")
                                            + ".h",
                                        )
                                    ):
                                        PyG3A._import(
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
                                    PyG3A._import(
                                        Block._obj_to_c_str(line.module).replace(".", "/") + ".hpp"
                                    )
                                elif os.path.isfile(
                                    os.path.join(
                                        loc,
                                        Block._obj_to_c_str(line.module).replace(".", "/") + ".h",
                                    )
                                ):
                                    PyG3A._import(
                                        Block._obj_to_c_str(line.module).replace(".", "/") + ".h"
                                    )

            Main.project.modules.append(module_name)

    @staticmethod
    def _cst_to_code(node: cst.CSTNode) -> str:
        return cst.Module([node]).code

    @staticmethod
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

    @staticmethod
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

        Main()

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

        PyG3A._import_module("stdpy")

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
                f"{Main.registry[fun.ret]} {fun.name}({', '.join([Block._obj_to_c_str(param.annotation.annotation, True) for param in fun.args])});"
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


class Main:
    libfxcg: str = "../../"
    verbose: bool = False
    package_locs: list[str] = [
        os.path.join(os.environ["HOME"], ".local", "lib", "pyg3a"),
        os.path.join(os.path.dirname(__file__), "packages"),
    ]
    project: Project = Project("NONE")
    func_types: dict = {}
    main_function_overridden: bool = False
    tmp_nums: dict[str, int] = {}
    registry: TypeRegistry = TypeRegistry()

    def __init__(self):
        Main.registry.auto_register(RegistryType.INTEGERS, RegistryType.NUMBERS)
        Main.registry.auto_register(RegistryType.FLOATS, RegistryType.NUMBERS)

        Main.registry.auto_register(RegistryType.INTEGERS, RegistryType.PY)
        Main.registry.auto_register(RegistryType.FLOATS, RegistryType.PY)

        Main.registry.register("None", "void", RegistryType.NONE)

        Main.registry.register("any", "auto", RegistryType.PY)
        Main.registry.register("str", "String", RegistryType.PY)

        Main.registry.register("int", "int", RegistryType.INTEGERS)
        Main.registry.register("unsint", "unsigned int*", RegistryType.INTEGERS)
        Main.registry.register("char", "char", RegistryType.INTEGERS)
        Main.registry.register("float", "float", RegistryType.FLOATS)

        Main.registry.register("cstr", "const char*", RegistryType.C_STRINGS)
        Main.registry.register("mutstr", "char*", RegistryType.C_STRINGS)
        Main.registry.register("conststr", "const char*", RegistryType.C_STRINGS)
        Main.registry.register("arrstr", "char", RegistryType.C_STRINGS)
        Main.registry.register("unsstr", "unsigned char*", RegistryType.C_STRINGS)


if __name__ == "__main__":
    PyG3A.main()
