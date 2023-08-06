#!/usr/bin/env python3

import fxcg.display


def __pyg3a_show_screen(obj: cst.CSTNode) -> str:
    ARG_TYPES = {}
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

        return "Bdisp_PutDisp_DD()"
    raise SyntaxError(
        f"Incorrect type(s) of arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
    )


def __pyg3a_clear_screen(obj: cst.CSTNode) -> str:
    ARG_TYPES = {}
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
            """void _clear_screen() {
\tunsigned int *p = (unsigned int*) GetVRAMAddress();
\tfor (int i = 0; i < LCD_WIDTH_PX; i++) {
\t\tfor (int j = 0; j < LCD_HEIGHT_PX; j++) *p++ = 0;
\t}
};""",
        )

        return ""
    raise SyntaxError(
        f"Incorrect type(s) of arguments to {NAME}({_gen_arg_str(ARG_TYPES, OPTIONAL_ARGS)})"
    )


def __pyg3a_set_pixel(obj: cst.CSTNode) -> str:
    ARG_TYPES = {0: [int], 1: [int], 2: [tuple[int]]}
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
            "_RGB_struct",
            """struct _RGB_struct {
\tint _0;
\tint _1;
\tint _2;
};""",
        )
        _add_c_func(
            f"_{NAME}",
            """void _set_pixel(int x, int y, _RGB_struct colour) {
\tBdisp_SetPoint_VRAM(x, y, ((colour._0 & 248) << 8) | ((colour._1 & 252) << 3) | (colour._2 >> 3));
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


def __pyg3a_get_pixel(obj: cst.CSTNode) -> str:
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

        _add_c_func(
            "_RGB_struct",
            """struct _RGB_struct {
\tint _0;
\tint _1;
\tint _2;
};""",
        )
        _add_c_func(
            f"_{NAME}",
            """_RGB_struct _get_pixel(int x, int y) {
\tunsigned short colour = Bdisp_GetPoint_VRAM(x, y);
\t_RGB_struct ret_struct = {
\t((colour >> 11) & 0x1F) << 1,
\t(colour >> 5) & 0x2F,
\t(x & 0x1F) << 1
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


def __pyg3a_draw_string(obj: cst.CSTNode) -> str:
    ARG_TYPES = {0: [int], 1: [int], 2: [str], 3: [tuple[int]], 4: [str]}
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
            "_RGB_struct",
            """struct _RGB_struct {
\tint _0;
\tint _1;
\tint _2;
};""",
        )
        _add_c_func(
            "__asm__PrintMiniMini2",
            """void PrintMiniMini2(int* x, int* y, const char* message, int mode, unsigned int xlimit, int P6, int P7, unsigned short color, unsigned short back_color, int writeflag, int P11);

__asm__(".text; .align 2; .global _PrintMiniMini2; "
\t"_PrintMiniMini2: mov.l sc_addr, r2; mov.l 1f, r0; "
\t"jmp @r2; nop; 1: .long 0x23f; "
\t"sc_addr: .long 0x80020070");""",
        )
        _add_c_func(
            f"_{NAME}",
            """void _draw_string(int x, int y, String text, _RGB_struct colour, String size) {
\tif (size == String("large"))
\t\tPrintCXY(x, y, text.c_str(), TEXT_MODE_NORMAL, -1, ((colour._0 & 248) << 8) | ((colour._1 & 252) << 3) | (colour._2 >> 3), COLOR_WHITE, 1, 0);
\telse if (size == String("medium"))
\t\tPrintMini(&x, &y, text.c_str(), TEXT_MODE_NORMAL, -1, 0, 0, ((colour._0 & 248) << 8) | ((colour._1 & 252) << 3) | (colour._2 >> 3), COLOR_WHITE, 1, 0);
\telse
\t\tPrintMiniMini2(&x, &y, text.c_str(), TEXT_MODE_NORMAL, -1, 0, 0, ((colour._0 & 248) << 8) | ((colour._1 & 252) << 3) | (colour._2 >> 3), COLOR_WHITE, 1, 0);
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


def __types_pyg3a() -> dict[str, str]:
    func_types: dict[str, str] = {}
    func_types["show_screen"] = "None"
    func_types["clear_screen"] = "None"
    func_types["set_pixel"] = "None"
    func_types["get_pixel"] = "tuple[int]"
    func_types["draw_string"] = "None"

    return func_types
