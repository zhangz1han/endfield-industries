from dataclasses import dataclass
from typing import Optional
from pulp import LpMaximize, LpProblem, LpVariable, PULP_CBC_CMD

@dataclass
class Material:
    name: str
    """原料名称"""

    yield_per_min: int
    """每分钟产量"""

@dataclass
class Formula:
    name: str
    """配方名称"""

    duration: int
    """加工时长，单位：秒。一般为 2 或 10"""

    stock_bills: int
    """交易得到的调度券数量"""

    materials: list[int]
    """所需各种原料的数量"""

def require_not_none[T](value: Optional[T], message: str = "the value cannot be \"None\"") -> T:
    if value == None:
        raise Exception(message)
    else:
        return value

def safe_to_int(value: float) -> int:
    result = int(value)
    if float(result) == value:
        return result
    else:
        raise Exception("can not safe transform float to int")

def get_or_default[T](collection: list[T], index: int, default_value: T) -> T:
    if 0 <= index < len(collection):
        return collection[index]
    else:
        return default_value

def get_or_zero(collection: list[int], index: int) -> int:
    return get_or_default(collection, index, 0)

def print_indent(indent: int, text: str):
    print("    " * indent + text)

class Area:
    def __init__(self, name: str ,materials: list[Material]) -> None:
        self.materials = materials
        self.name = name
        self.formulas: list[Formula] = []

    def solve(self):
        formulas_indice = range(0, len(self.formulas))
        materials_indice = range(0, len(self.materials))

        model = LpProblem(name=self.name, sense=LpMaximize)

        variables = [LpVariable(name=self.name + i.name, lowBound=0, cat='Integer') for i in self.formulas]

        model += sum([self.formulas[i].stock_bills * variables[i] for i in formulas_indice]), f"{self.name}_总计调度券数量"

        for material_index in materials_indice:
            material = self.materials[material_index]
            model += sum([get_or_zero(self.formulas[i].materials, material_index) / self.formulas[i].duration * 2 * variables[i] for i in formulas_indice]) <= (material.yield_per_min / 30), f"{self.name}_{material.name}"
        
        model.solve(PULP_CBC_CMD(msg=False))

        print(f"“{self.name}”生产线计算:")
        print_indent(1, "最优生产线配比:")
        for formulas_index in formulas_indice:
            value = safe_to_int(require_not_none(variables[formulas_index].value()))
            if value != 0:
                print_indent(2, f"{self.formulas[formulas_index].name}: {value}")

        print_indent(1, f"最大利润: {safe_to_int(model.objective.value())}") # pyright: ignore
        
        print_indent(1, "原材料消耗量:")
        for material_index in materials_indice:
            material = self.materials[material_index]
            value = sum([get_or_zero(self.formulas[i].materials, material_index) / self.formulas[i].duration * 2 * require_not_none(variables[i].value()) for i in formulas_indice])
            print_indent(2, f"{material.name}: {safe_to_int(value) * 30}/min")
