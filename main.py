from endfield_industries import *

def main():
    # 原料以及每分钟产量
    # Material(名称, 每分钟产量)
    materials = [
        Material("源矿", 510),
        Material("紫晶矿", 240),
        Material("蓝铁矿", 760)
    ]

    # 配方
    # Formula(名称, 制造时长, 调度券数量, [原料1, 原料2, 原料3...])
    formulas = [
        Formula("晶体外壳", 2, 1, [1, 0, 0]),
        Formula("紫晶零件", 2, 1, [0, 1, 0]),
        Formula("铁质零件", 2, 1, [0, 0, 1]),
        Formula("钢质零件", 2, 3, [0, 0, 2]),
        Formula("胶囊/罐头", 10, 10, [0, 10, 0]),
        Formula("优质胶囊/罐头", 10, 27, [0, 0, 20]),
        Formula("精选胶囊/罐头", 10, 70, [0, 0, 40]),
        Formula("低容谷地电池", 10, 16, [10, 5, 0]),
        Formula("中容谷地电池", 10, 30, [15, 0, 10]),
        Formula("高容谷地电池", 10, 70, [30, 0, 20]),
    ]
    
    endfield = EndfieldIndustries(materials)
    endfield.add_formulas(formulas)
    endfield.solve()

if __name__ == "__main__":
    main()
