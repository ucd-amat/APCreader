import numpy as np
import pandas as pd
from scipy.interpolate import LinearNDInterpolator

def parse_APC_data(file_name):
    APC_keys = ["V_mph","J","Pe","Ct", "Cp", "PWR_hp", "Torque_inlbf", "Thrust_lbf", "PWR_W", "Torque_Nm", "Thrust_N", "THR/PWR_gpW", "Mach", "Reyn", "FOM"]
    data = {key:[] for key in ["RPM"]+APC_keys}
    # read filename
    with open(file_name, 'r') as f:
        lines = f.read().splitlines()
    lines = [' '.join(line.split()) for line in lines if line.strip()]
    rpm_index  = [i for i, line in enumerate(lines) if "PROP RPM" in line]
    
    for i,_ in enumerate(rpm_index):
        # first find the bounds of the data
        try:
            rpm = float(lines[rpm_index[i]].split()[-1])
            final_idx = rpm_index[i+1]-(len(lines[rpm_index[i+1]-1].split())<15)
        except:
            final_idx = len(lines)
            final_idx = final_idx-(len(lines[final_idx-1].split())<15)
            
        # add the data to the list
        for line in lines[rpm_index[i]+3: final_idx]:
            data["RPM"].append(rpm)
            for key, col in zip(APC_keys, map(float, line.split())):
                data[key].append(col)
        
        # for key in APC_keys:
        #     data["RPM"].append(0)
        #     data[key].append(0)         
        
    data = {k:np.array(v) for k,v in data.items()}

    
    # print(data)
    interpolators = {}
    for key in APC_keys:
        interpolators[key] = LinearNDInterpolator(list(zip(data["RPM"],data["J"])),data[key])
        
    def APC_interpolator(RPM, J):
        return {key: interpolators[key](RPM,J) for key in APC_keys}
    
    return APC_interpolator

if __name__ == "__main__":
    # Usage
    file_name = 'data/PER3_16x8.dat'  # Replace with your actual filename
    prop_performance = parse_APC_data(file_name)
    print(prop_performance(1000,0.5))