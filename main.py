from endfield_industries import *

def main():
    # 原料以及每分钟产量
    # Material(名称, 每分钟产量)
    valley_materials = [
        Material("源矿", 560),
        Material("紫晶矿", 240),
        Material("蓝铁矿", 1080),
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

    valley = Area("四号谷地", valley_materials)
    valley.formulas += formulas
    valley.solve()

    wuling_materials = [
        Material("源矿", 290),
        Material("紫晶矿", 0),
        Material("蓝铁矿", 90),
        Material("息壤", 60),
    ]

    formulas += [
        Formula("低容武陵电池", 10, 25, [30, 0, 0, 5]),
        Formula("芽针针剂", 10, 16, [0, 0, 20, 0]),
    ]

    wuling = Area("武陵", wuling_materials)
    wuling.formulas += formulas
    wuling.solve()

if __name__ == "__main__":
    main()
