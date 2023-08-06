#!/usr/bin/env python3
import fxcg.app
import fxcg.display
import fxcg.keyboard
import fxcg.system


def pyg3a_template(obj: cst.CSTNode) -> str:
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

        return f"{NAME}({', '.join(args)})"
    raise SyntaxError(
        f"Incorrect type(s) of arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
    )


def __pyg3a_PrintXY(obj: cst.CSTNode) -> str:
    ARG_TYPES = {0: [int], 1: [int], 2: [str], 3: [int], 4: [int]}
    OPTIONAL_ARGS = {3: 0, 4: 0}
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

        if type(obj.args[2].value) is cst.SimpleString:
            if len(obj.args[2].value.raw_value) < 2 or (
                obj.args[2].value.raw_value[0] != " " and obj.args[2].value.raw_value[1] != " "
            ):
                args[2] = f'"  {obj.args[2].value.raw_value}"'
        else:
            args[2] = f'(String("  ") + {args[2]}).c_str()'

        return f"{NAME}({', '.join(args)})"
    raise SyntaxError(
        f"Incorrect type(s) of arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
    )


def __pyg3a_EditMBStringChar(obj: cst.CSTNode) -> str:
    ARG_TYPES = {0: [str], 1: [int], 2: [int]}
    RETURN_TYPES = ("String", "int")
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

        _add_c_func(
            f"_{NAME}_struct",
            f"struct _{NAME}_struct"
            + "{"
            + "".join(["\n\t" + f"{arg} _{i};" for i, arg in enumerate(RETURN_TYPES)])
            + "\n};\n",
        )
        _add_c_func(
            f"_{NAME}",
            f"_{NAME}_struct _{NAME}"
            + """(String MB_string, int xpos, int char_to_insert) {
\tString new_str = String(MB_string, MB_string.length() + 1);
\tint cursor = EditMBStringChar((unsigned char*) new_str.c_str(), MB_string.length() + 1, xpos, char_to_insert);
\t_EditMBStringChar_struct ret_struct = {
\tnew_str,
\tcursor
\t};
\treturn ret_struct;
};""",
        )

        args = [_obj_to_c_str(arg.value) for arg in obj.args]
        if len(obj.args) < len(ARG_TYPES):
            args.extend(
                [
                    _obj_to_c_str(OPTIONAL_ARGS[i])
                    for i in [item for item in ARG_TYPES.keys() if item not in range(len(obj.args))]
                ]
            )

        return f"_{NAME}({', '.join(args)})"
    raise SyntaxError(
        f"Incorrect type(s) of arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
    )


def __pyg3a_DisplayMBString(obj: cst.CSTNode) -> str:
    ARG_TYPES = {0: [str], 1: [int], 2: [int], 3: [int], 4: [int]}
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

        args[0] = f"(unsigned char*) {args[0]}.c_str()"
        return f"{NAME}({', '.join(args)})"
    raise SyntaxError(
        f"Incorrect type(s) of arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
    )


def __pyg3a_EditMBStringCtrl(obj: cst.CSTNode) -> str:
    ARG_TYPES = {0: [str], 1: [int], 2: [int], 3: [int], 4: [int]}
    RETURN_TYPES = ("String", "int", "int", "int")
    OPTIONAL_ARGS = {4: 256}
    if _correct_arg_types(ARG_TYPES):
        if len(obj.args) < len(ARG_TYPES) - len(OPTIONAL_ARGS):
            raise SyntaxError(
                f"Too few arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
            )
        if len(obj.args) > len(ARG_TYPES):
            raise SyntaxError(
                f"Too many arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
            )

        _add_c_func(
            f"_{NAME}_struct",
            f"struct _{NAME}_struct"
            + "{"
            + "".join(["\n\t" + f"{arg} _{i};" for i, arg in enumerate(RETURN_TYPES)])
            + "\n};\n",
        )
        _add_c_func(
            "_EditMBStringCtrl",
            """_EditMBStringCtrl_struct _EditMBStringCtrl(String MB_string, int key, int x, int y, int posmax) {
\tint start_val = 0;
\tint xpos_val = 0;
\tint* start = &start_val;
\tint* xpos = &xpos_val;
\tString new_str = String(MB_string, posmax);
\tEditMBStringCtrl((unsigned char*) new_str.c_str(), posmax, start, xpos, &key, x, y);
\t_EditMBStringCtrl_struct ret_struct = {
\tnew_str,
\t*start,
\t*xpos,
\tkey
\t};
\treturn ret_struct;
};""",
        )

        args = [_obj_to_c_str(arg.value) for arg in obj.args]
        if len(obj.args) < len(ARG_TYPES):
            args.extend(
                [
                    _obj_to_c_str(OPTIONAL_ARGS[i])
                    for i in [item for item in ARG_TYPES.keys() if item not in range(len(obj.args))]
                ]
            )

        return f"_EditMBStringCtrl({', '.join(args)})"
    raise SyntaxError(
        f"Incorrect type(s) of arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
    )


def __pyg3a_PrintMini(obj: cst.CSTNode) -> str:
    ARG_TYPES = {0: [int], 1: [int], 2: [str], 3: [int], 4: [int], 5: [int], 6: [int], 7: [int]}
    RETURN_TYPES = ("int", "int")
    OPTIONAL_ARGS = {3: 0, 4: 0xFFFFFFFF, 5: 0, 6: 0xFFFF, 7: 1}
    if _correct_arg_types(ARG_TYPES):
        if len(obj.args) < len(ARG_TYPES) - len(OPTIONAL_ARGS):
            raise SyntaxError(
                f"Too few arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
            )
        if len(obj.args) > len(ARG_TYPES):
            raise SyntaxError(
                f"Too many arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
            )

        _add_c_func(
            f"_{NAME}_struct",
            f"struct _{NAME}_struct"
            + "{"
            + "".join(["\n\t" + f"{arg} _{i};" for i, arg in enumerate(RETURN_TYPES)])
            + "\n};\n",
        )
        _add_c_func(
            f"_{NAME}",
            """_PrintMini_struct _PrintMini(int x, int y, String string, int mode_flags, int xlimit, int colour, int back_colour, int writeflag) {
\tPrintMini(&x, &y, string.c_str(), mode_flags, (unsigned int) xlimit, 0, 0, colour, back_colour, writeflag, 0);
\t_PrintMini_struct ret_struct = {
\tx,
\ty
\t};
\treturn ret_struct;
};""",
        )

        args = [_obj_to_c_str(arg.value) for arg in obj.args]
        if len(obj.args) < len(ARG_TYPES):
            args.extend(
                [
                    _obj_to_c_str(OPTIONAL_ARGS[i])
                    for i in [item for item in ARG_TYPES.keys() if item not in range(len(obj.args))]
                ]
            )

        return f"_{NAME}({', '.join(args)})"
    raise SyntaxError(
        f"Incorrect type(s) of arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
    )


def __pyg3a_Bdisp_AreaClr(obj: cst.CSTNode) -> str:
    ARG_TYPES = {0: ["display_fill"], 1: [bool], 2: [int]}
    OPTIONAL_ARGS = {2: 0}
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

        args[0] = f"&{_obj_to_c_str(obj.args[0].value)}"
        return f"{NAME}({', '.join(args)})"
    raise SyntaxError(
        f"Incorrect type(s) of arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
    )


def __pyg3a_SetGetkeyToMainFunctionReturnFlag(obj: cst.CSTNode) -> str:
    ARG_TYPES = {0: [bool]}
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
            """/* CODE (originally) BY SIMON LOTHAR, AVAILABLE ON "fx_calculators_SuperH_based.chm" version 16 */
// the function assumes, that the RAM-pointer to GetkeyToMainFunctionReturnFlag is loaded
// immediately by a "Move Immediate Data"-instruction
void _SetGetkeyToMainFunctionReturnFlag(int enabled) {
    int addr, addr2;

    // get the pointer to the syscall table
    addr = *(unsigned char*)0x80020071;     // get displacement

    addr++;
    addr *= 4;
    addr += 0x80020070;
    addr = *(unsigned int*)addr;

    if ( addr < (int)0x80020070 ) return;
    if ( addr >= (int)0x81000000 ) return;

    // get the pointer to syscall 1E99
    addr += 0x1E99*4;
    if ( addr < (int)0x80020070 ) return;
    if ( addr >= (int)0x81000000 ) return;

    addr = *(unsigned int*)addr;
    if ( addr < (int)0x80020070 ) return;
    if ( addr >= (int)0x81000000 ) return;

    switch ( *(unsigned char*)addr ){
            case 0xD0 : // MOV.L @( disp, PC), Rn (REJ09B0317-0400 Rev. 4.00 May 15, 2006 page 216)
            case 0xD1 :
            case 0xD2 :
            case 0xD3 :
            case 0xD4 :
            case 0xD5 :
            case 0xD6 :
            case 0xD7 :
            case 0xD8 :
                    addr2 = *(unsigned char*)( addr + 1 );  // get displacement
                    addr2++;
                    addr2 *= 4;
                    addr2 += addr;
                    addr2 &= ~3;

                    if ( addr2 < (int)0x80020070 ) return;
                    if ( addr2 >= (int)0x81000000 ) return;

                    addr = *(unsigned int*)addr2;
                    if ( ( addr & 0xFF000000 ) != 0x88000000 && ( addr & 0xFF000000 ) != 0x8C000000 ) return; // MODIFIED for CG50 or CG10/20 (memory address change)

                    // finally perform the desired operation and set the flag:
                    if ( enabled ) *(unsigned char*)addr = 0;
                    else *(unsigned char*)addr = 3;

                    break;

            default : addr = 0x100;
    }
}""",
        )

        return f"_{NAME}({', '.join(args)})"
    raise SyntaxError(
        f"Incorrect type(s) of arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
    )


def __pyg3a_Timer_Install(obj: cst.CSTNode) -> str:
    ARG_TYPES = {0: [(None, [])], 1: [int], 2: [int]}
    OPTIONAL_ARGS = {1: 0, 2: 1}
    if _correct_arg_types(ARG_TYPES):
        if len(obj.args) < len(ARG_TYPES) - len(OPTIONAL_ARGS):
            raise SyntaxError(
                f"Too few arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
            )
        if len(obj.args) > len(ARG_TYPES):
            raise SyntaxError(
                f"Too many arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
            )

        args = [_obj_to_c_str(arg.value, generateVoidLambda=True) for arg in obj.args]
        if len(obj.args) < len(ARG_TYPES) + 1:
            args.extend(
                [
                    _obj_to_c_str(OPTIONAL_ARGS[i])
                    for i in [item for item in ARG_TYPES.keys() if item not in range(len(obj.args))]
                ]
            )

        return f"{NAME}({args[1]}, {args[0]}, {args[2]})"
    raise SyntaxError(
        f"Incorrect type(s) of arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
    )


def __pyg3a_PowerOff(obj: cst.CSTNode) -> str:
    ARG_TYPES = {0: [bool]}
    OPTIONAL_ARGS = {0: True}
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

        return f"{NAME}({', '.join(args)})"
    raise SyntaxError(
        f"Incorrect type(s) of arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
    )


def __pyg3a_GetLatestUserInfo(obj: cst.CSTNode) -> str:
    ARG_TYPES = {}
    RETURN_TYPES = ("String", "String", "String")
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
            f"_GetUserInfo_struct",
            f"struct _GetUserInfo_struct"
            + "{"
            + "".join(["\n\t" + f"{arg} _{i};" for i, arg in enumerate(RETURN_TYPES)])
            + "\n};\n",
        )
        _add_c_func(
            f"_{NAME}",
            """_GetUserInfo_struct _GetLatestUserInfo() {
        // Search through user info
        char* flagpointer = (char*) 0x80BE0000;
        int counter = 0;
        while (*flagpointer == 0x0F) {
            flagpointer = flagpointer + 0x40;
            counter++;
        }

        // Set password from latest info
        _GetUserInfo_struct info;
        if (counter) {
            flagpointer = flagpointer - 0x40;
            if(*(flagpointer+0x2C) != '\\0') {
                info = {String(flagpointer+0x04), String(flagpointer+0x18), String(flagpointer+0x2C)};
            }
        }
        return info;
}""",
        )

        return f"_{NAME}({', '.join(args)})"
    raise SyntaxError(
        f"Incorrect type(s) of arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
    )


def __pyg3a_GetKey(obj: cst.CSTNode) -> str:
    if len(obj.args) == 1:
        if (
            type(obj.args[0].value) is cst.Call
            and type(obj.args[0].value.func) is cst.Name
            and obj.args[0].value.func.value == "ref"
        ):
            return f"{NAME}({_obj_to_c_str(obj.args[0].value)})"
        return f"{NAME}(&{_obj_to_c_str(obj.args[0].value)})"
    if len(obj.args) == 0:
        _add_c_func(
            "_GetKey",
            "int _GetKey() {\n\tint _tmp_var;\n\tGetKey(&_tmp_var);\n\treturn _tmp_var;\n}",
        )
        return "_GetKey()"
    raise SyntaxError(f"Incorrect number of arguments to {NAME}()")


def __pyg3a_GetKeyWait_OS(obj: cst.CSTNode) -> str:
    ARG_TYPES = {0: [int], 1: [int], 2: [int]}
    RETURN_TYPES = ("int", "int", "int")
    OPTIONAL_ARGS = {0: 0, 1: 0, 2: 0}
    if _correct_arg_types(ARG_TYPES):
        if len(obj.args) < len(ARG_TYPES) - len(OPTIONAL_ARGS):
            raise SyntaxError(
                f"Too few arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
            )
        if len(obj.args) > len(ARG_TYPES):
            raise SyntaxError(
                f"Too many arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
            )

        _add_c_func(
            f"_{NAME}_struct",
            f"struct _{NAME}_struct"
            + "{"
            + "".join(["\n\t" + f"{arg} _{i};" for i, arg in enumerate(RETURN_TYPES)])
            + "\n};\n",
        )
        _add_c_func(
            f"_{NAME}",
            """_GetKeyWait_OS_struct _GetKeyWait_OS(int type_of_waiting, int timeout_period, int menu) {
\tint column, row;
\tunsigned short keycode;
\tGetKeyWait_OS(&column, &row, type_of_waiting, timeout_period, menu, &keycode);
\t_GetKeyWait_OS_struct ret_struct = {
\tcolumn,
\trow,
\t(int) keycode
\t};
\treturn ret_struct;
};""",
        )

        args = [_obj_to_c_str(arg.value) for arg in obj.args]
        if len(obj.args) < len(ARG_TYPES):
            args.extend(
                [
                    _obj_to_c_str(OPTIONAL_ARGS[i])
                    for i in [item for item in ARG_TYPES.keys() if item not in range(len(obj.args))]
                ]
            )

        return f"_{NAME}({', '.join(args)})"
    raise SyntaxError(
        f"Incorrect type(s) of arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
    )


def __pyg3a_GetMainBatteryVoltage(obj: cst.CSTNode) -> str:
    return "GetMainBatteryVoltage(1)"


def __types_pyg3a() -> dict[str, str]:
    func_types: dict[str, str] = {}
    func_types["PrintXY"] = "None"
    func_types["DisplayMBString"] = "None"
    func_types["Bdisp_AreaClr"] = "None"
    func_types["SetGetkeyToMainFunctionReturnFlag"] = "None"
    func_types["Timer_Install"] = "int"
    func_types["PowerOff"] = "None"
    func_types["GetKey"] = "int"
    func_types["GetMainBatteryVoltage"] = "int"
    func_types["GetKeyWait_OS"] = "_GetKeyWait_OS_struct"
    func_types["GetLatestUserInfo"] = "_GetUserInfo_struct"

    return func_types


def __registry_types_pyg3a() -> dict[str, tuple[str, RegistryType]]:
    PY_C_TYPES: dict[str, tuple[str, RegistryType]] = {}
    PY_C_TYPES["color"] = ("color_t", RegistryType.INTEGERS)

    return PY_C_TYPES
