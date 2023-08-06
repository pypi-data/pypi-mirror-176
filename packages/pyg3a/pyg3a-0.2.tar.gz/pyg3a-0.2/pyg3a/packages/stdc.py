def __pyg3a_ref(obj: cst.CSTNode) -> str:
    if len(obj.args) == 1 and type(obj.args[0]) is ast.Name:
        return f"&{obj.args[0].id}"


def __pyg3a_deref(obj: cst.CSTNode) -> str:
    if len(obj.args) == 1:
        return f"*({_obj_to_c_str(obj.args[0])})"


def __pyg3a_cast_unsstr(obj: cst.CSTNode) -> str:
    if len(obj.args) == 1:
        return f"(unsigned char*) {_obj_to_c_str(obj.args[0])}"


def __pyg3a_cast_unsint(obj: cst.CSTNode) -> str:
    if len(obj.args) == 1:
        return f"(unsigned int*) {_obj_to_c_str(obj.args[0])}"


def __pyg3a_cast_int(obj: cst.CSTNode) -> str:
    if len(obj.args) == 1:
        return f"(int) {_obj_to_c_str(obj.args[0])}"


def __pyg3a_cast_str(obj: cst.CSTNode) -> str:
    if len(obj.args) == 1:
        return f"(char*) {_obj_to_c_str(obj.args[0])}"


def __types_pyg3a() -> dict[str, str]:
    func_types: dict[str, str] = {}
    func_types["cast_unsstr"] = "unsstr"
    func_types["cast_unsint"] = "unsint"
    func_types["cast_int"] = "int"
    func_types["cast_str"] = "mutstr"

    return func_types
