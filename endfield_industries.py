from dataclasses import dataclass
from typing import Optional
from pulp import LpMaximize, LpProblem, LpVariable

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

class EndfieldIndustries:
    formulas: list[Formula] = []
    name = "终末地工业"

    def __init__(self, materials: list[Material]) -> None:
        self.materials = materials
    
    def add_formula(self, formula: Formula):
        if len(formula.materials) == len(self.materials):
            self.formulas.append(formula)
        else:
            raise Exception("配方原料种类数不匹配")
    
    def add_formulas(self, formulas: list[Formula]):
        for formula in formulas:
            self.add_formula(formula)

    def solve(self):
        formulas_indice = range(0, len(self.formulas))
        materials_indice = range(0, len(self.materials))

        model = LpProblem(name=self.name, sense=LpMaximize)
        variables = [LpVariable(name=i.name, lowBound=0, cat='Integer') for i in self.formulas]
        model += sum([self.formulas[i].stock_bills * variables[i] for i in formulas_indice]), "总计调度券数量"
        for material_index in materials_indice:
            material = self.materials[material_index]
            model += sum([self.formulas[i].materials[material_index] / self.formulas[i].duration * 2 * variables[i] for i in formulas_indice]) <= (material.yield_per_min / 30), material.name
        model.solve()

        print(f"状态: {model.status}")

        print("最优生产线配比:")
        for formulas_index in formulas_indice:
            value = safe_to_int(require_not_none(variables[formulas_index].value()))
            if value != 0:
                print(f"    {self.formulas[formulas_index].name}: {value}")

        print(f"最大利润: {safe_to_int(model.objective.value())}") # pyright: ignore
        
        print("原材料消耗量:")
        for material_index in materials_indice:
            material = self.materials[material_index]
            value = sum([self.formulas[i].materials[material_index] / self.formulas[i].duration * 2 * require_not_none(variables[i].value()) for i in formulas_indice])
            print(f"    {material.name}: {safe_to_int(value) * 30}/min")
