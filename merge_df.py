import os
import numpy as np
import pandas as pd

Vprime = 'W'
Vprime = 'Z'

df_list = []
m_values = [1000, 2000, 3000, 4000]
gv_values = [1, 3]
gF_values = np.arange(-1.6, 1.7, 0.2)
gF_values = [round(x,3) for x in gF_values]
gF_values = [x if abs(x)!=0 else 0.0 for x in gF_values]

for mass in m_values:
    for gv in gv_values:
        for gF in gF_values:
            csv_file = f'BRs_{Vprime}prime_M{mass}_gv{gv}_gf{gF}.csv'
            if not os.path.exists(csv_file):
                print("MISSING", csv_file)
            else:
                df_list.append(pd.read_csv(csv_file))
                

csv_file = f'BRs_{Vprime}prime.csv' 
df = pd.concat(df_list)
df = df.astype('float32')
df.to_csv(csv_file, index=False)