g_su2 = 0.6534


def gH():
    return gv * ch


def gF():
    return g_su2 * g_su2 * cq / gv


ch = -0.556
cq = -1.316
gv = 1

print(f"Model A -> gH={gH()}, gF={gF()}")
ch = -0.976
cq = 1.024
gv = 3
print(f"Model B -> gH={gH()}, gF={gF()}")

ch = 1
cq = 0
gv = 1

print(f"Model C -> gH={gH()}, gF={gF()}")
