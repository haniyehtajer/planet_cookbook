import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from astropy import units as u
from scipy.stats import ks_2samp


#This function reads .out files, and extracts collision times, collision types, and number of bodies versus time
def extract_data_outfile(file_path):
    """
    Extracts collision time, types, and t versus number of bodies in simulation from the output file.
    Returns two pandas dataframes:
    1. t_type: with columns ['coll_times', 'coll_types']
    2. t_n: with columns ['t', 'n_bodies']
    """
    coll_time = []
    coll_types = []
    n_bodies_list = []
    
    # Open and read the file
    with open(file_path, 'r') as file:
        for line in file:
            # Check if the line contains the desired phrase
            if "TIME OF COLLISION:" in line:
                # Extract the value after "TIME OF COLLISION:"
                time_value = float(line.split(":")[1].strip())
                coll_time.append(time_value)
            
            if "COLLISION TYPE:" in line:
                # Extract the value after "COLLISION TYPE:"
                type_value = line.split(":")[1].strip()
                coll_types.append(type_value)
                
            if "N_tot=" in line and "t=" in line:
                # Extract N_tot and time values
                parts = line.split()
                n_bodies = int(parts[1])  # Extract the value after "N_tot="
                t = int(float(parts[3]))  # Extract the time value and convert to integer
                # Append the (t, n_bodies) as a tuple to the list
                n_bodies_list.append((t, n_bodies))
                
    # Convert lists to numpy arrays for structured data
    n_bodies = np.array(n_bodies_list, dtype=[('t', 'i4'), ('n_bodies', 'i4')])
    
    # Create pandas DataFrame for collision time and types
    t_type = pd.DataFrame({
        'coll_times': coll_time,
        'coll_types': coll_types
    })
    
    # Create pandas DataFrame for n_bodies (t and n_bodies)
    t_n = pd.DataFrame(n_bodies)
    
    return t_type, t_n

def extract_data_outfile_full(file_path):
    """
    Extracts collision time, types, and t versus number of bodies in simulation from the output file.
    Returns one panda's dataframe with everything!
    """
    df = pd.DataFrame(columns=['time', 'hash_t', 'Mt', 'hash_p', 'Mp',
                                'Mp/Mt', 'Mlr/Mt', 'Mlr/Mtot', 'b/Rt', 'Vimp/Vesc', 'Q/Q*', 'type'])
    index = 0

    with open(file_path, 'r') as file:
            for line in file:
                # Check if the line contains the desired phrase
                if "TIME OF COLLISION:" in line:
                    # Extract the value after "TIME OF COLLISION:"
                    df.loc[index, 'time'] = float(line.split(":")[1].strip())
                
                if "Target hash, mass =" in line:
                    hash_mass_t = line.split("=")[1].strip()
                    df.loc[index, 'hash_t'], df.loc[index, 'Mt'] = hash_mass_t.split()
                    
                if "Projectile hash, mass =" in line:
                    hash_mass_p = line.split("=")[1].strip()
                    df.loc[index, 'hash_p'], df.loc[index, 'Mp'] = hash_mass_p.split()
                    
                if "Mp/Mt:" in line:
                    df.loc[index, 'Mp/Mt'] = float(line.split(":")[1].strip())
                
                if "Mlr/Mt:" in line:
                    df.loc[index, 'Mlr/Mt'] = float(line.split(":")[1].strip())
                
                if "Mlr/Mtot:" in line:
                    df.loc[index, 'Mlr/Mtot'] = float(line.split(":")[1].strip())
                
                if "b/Rtarg:" in line:
                    df.loc[index, 'b/Rt'] = float(line.split(":")[1].strip())
                
                if "Vimp/Vesc:" in line:
                    df.loc[index, 'Vimp/Vesc'] = float(line.split(":")[1].strip())
                
                if "Q/ Qstar:" in line:
                    df.loc[index, 'Q/Q*'] = float(line.split(":")[1].strip())
                
                if "COLLISION TYPE:" in line:
                    df.loc[index, 'type'] = str(line.split(":")[1].strip())
                    index += 1
    return df

#function to read number of bodies in simulation at every time point
def read_num_bodies(filepath):
    time = []
    df = []
    with open(filepath, 'r') as file:
        for line in file:
            if "N_tot=" in line and "t=" in line:
                        # Extract N_tot and time values
                        parts = line.split()
                        n_bodies = int(parts[1])  # Extract the value after "N_tot="
                        t = int(float(parts[3]))  # Extract the time value and convert to integer
                        # Append the (t, n_bodies) as a tuple to the list
                        df.append((t, n_bodies))

    n_bodies = np.array(df, dtype=[('t', 'i4'), ('n_bodies', 'i4')])
    t_n = pd.DataFrame(n_bodies)

    return t_n


def read_dbct_output(filename):
    df = pd.DataFrame(columns=['hash', 'mass', 'cmf'])

    data = np.loadtxt(filename)
    df['hash'] = data[:,0]
    df['mass'] = data[:,1]
    df['cmf'] = data[:,2]

    return df

#extract vi/vesc and b/b_crit

#This function reads .out files, and extracts collision times, collision types, and number of bodies versus time
def extract_data_impact(file_path):
    """
    Extracts collision time, types, and t versus number of bodies in simulation from the output file.
    """
    vi_vesc = []
    b_bcrit = []
    
    # Open and read the file
    with open(file_path, 'r') as file:
        for line in file:
            # Check if the line contains the desired phrase
            if "Vimp/Vesc:" in line:
                # Extract the value after "TIME OF COLLISION:"
                vi_vesc_value = float(line.split(":")[1].strip())
                vi_vesc.append(vi_vesc_value)
            
            if "b/Rtarg:" in line:
                # Extract the value after "COLLISION TYPE:"
                b_bcrit_value = float(line.split(":")[1].strip())
                b_bcrit.append(b_bcrit_value)
                

    vi_vesc = np.array(vi_vesc)
    b_bcrit = np.array(b_bcrit)
    
    
    return vi_vesc, b_bcrit

#This function can be used to extract data from collision_report files, with the
#format used as input files for Differentiated Body Composition Tracker
def extract_data_report(file_path):
    time = []
    type = []
    
    with open(file_path, "r") as file:
        for line in file:
            # Split the line into elements
            values = line.split()
            time.append(float(values[0]))
            type.append(int(values[1]))
    
    time = np.array(time)
    type = np.array(type)
    return time, type


#Function to get data from DBCT output file
def extract_dbct_report(file_path):
    mass = []
    cmf = []
    hash = []
    
    with open(file_path, "r") as file:
        for line in file:
            # Split the line into elements
            values = line.split()
            hash.append(int(values[0]))
            mass.append(float(values[1]))
            cmf.append(float(values[2]))
            
    hash = np.array(hash)
    mass = np.array(mass)
    cmf = np.array(cmf)
    return hash, mass, cmf

#function to plot v versus v
def plot_b_v(b, v, type):
    plt.clf()
    shape = np.zeros(len(type), dtype=object)
    color = np.zeros(len(type), dtype=object)
    
    for i in range(len(type)):
        if type[i] == 'EFFECTIVELY MERGED':
            shape[i] = 'D'
            color[i] = 'blue'
        
        elif type[i] == 'SIMPLY MERGED':
            shape[i] = 'D'
            color[i] = 'red'
        
        elif type[i] == 'PARTIAL ACCRETION':
            shape[i] = 'o'
            color[i] = 'black'
        
        elif type[i] == 'PARTIAL EROSION':
            shape[i] = '^'
            color[i] = 'grey'
    
        elif type[i] == 'SUPER-CATASTROPHIC':
            shape[i] = '^'
            color[i] = 'magenta'
            
        elif type[i] == 'GRAZE AND MERGE':
            shape[i] = 'o'
            color[i] = 'green'
        
        elif type[i] == 'ELASTIC BOUNCE':
            shape[i] = '*'
            color[i] = 'brown'
            
        elif type[i] == 'HIT AND RUN':
            shape[i] = '^'
            color[i] = 'orange'
            
        else:
            shape[i] = '*'
            color[i] = 'cyan'
            
    plt.figure(figsize=(10,6))

    # Track the types already used in the legend
    used_labels = set()

    for i in range(len(type)):
        label = type[i] if type[i] not in used_labels else None  # Only add label if it hasn't been used
        if label:
            used_labels.add(type[i])  # Add the label to the set

        plt.scatter(
        b[i], v[i], 
        label=label,
        marker=shape[i], 
        color=color[i]
        )
    plt.yscale('log')
    plt.xlabel('b/R_target')
    plt.ylabel('v/v_esc')
    plt.legend(loc='upper left')  # Show legend if needed

    plt.show()
    
    

    
#Function to make CDF
def make_cdf(data):
    data_sorted = np.sort(data)
    cdf = np.arange(1, len(data_sorted) + 1) / len(data_sorted)
    return data_sorted, cdf
    

def plot_v_cdf(v,color, label):
    v_plot, cdf = make_cdf(v)
    
    plt.plot(np.log(v_plot), cdf, color=color, label=label)

    plt.xlabel('log(vi_vesc)')
    plt.ylabel('CDF')
    plt.title('CDF of vi/vesc')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    


def perform_ks_test(data1, data2, alpha=0.05):
    """
    Perform a Kolmogorov-Smirnov (K-S) test on two datasets.

    Parameters:
        data1 (array-like): First dataset.
        data2 (array-like): Second dataset.
        alpha (float): Significance level for the test. Default is 0.05.

    Returns:
        dict: A dictionary containing the test statistic, p-value, 
              and a conclusion about the null hypothesis.
    """
    # Perform the K-S test
    statistic, p_value = ks_2samp(data1, data2)
    
    # Interpretation of the result
    result = {
        "statistic": statistic,
        "p_value": p_value,
        "conclusion": "Reject H0: The datasets are significantly different."
                     if p_value < alpha else
                     "Fail to reject H0: No significant difference in the datasets."
    }
    return result




def extract_data_outfile_limited(file_path, limit):
    """
    Extracts data from the output file related to collisions and the number of bodies over time,
    filtering the results to only include rows where 't' < limit.
    
    Parameters:
        file_path (str): Path to the output file.
        limit (float): The upper limit for the 't' values.
    
    Returns:
        tuple: Two pandas DataFrames:
            1. t_type: Columns ['coll_times', 'coll_types'] for collision times and types.
            2. t_n: Columns ['t', 'n_bodies'] for time and number of bodies in the simulation,
                    filtered by 't' < limit.
    """
    coll_time = []
    coll_types = []
    n_bodies_list = []

    try:
        # Open and read the file
        with open(file_path, 'r') as file:
            for line in file:
                # Extract collision time
                if "TIME OF COLLISION:" in line:
                    try:
                        time_value = float(line.split(":")[1].strip())
                        coll_time.append(time_value)
                    except ValueError:
                        print(f"Error parsing collision time in line: {line.strip()}")

                # Extract collision type
                if "COLLISION TYPE:" in line:
                    type_value = line.split(":")[1].strip()
                    coll_types.append(type_value)

                # Extract time and number of bodies
                if "N_tot=" in line and "t=" in line:
                    try:
                        parts = line.split()
                        n_bodies = int(parts[1])  # Extract the value after "N_tot="
                        t = float(parts[3])       # Extract the time value
                        if t < limit:             # Only include if t < limit
                            n_bodies_list.append((t, n_bodies))
                    except (IndexError, ValueError):
                        print(f"Error parsing N_tot or time in line: {line.strip()}")

        # Create pandas DataFrames
        t_type = pd.DataFrame({
            'coll_times': coll_time,
            'coll_types': coll_types
        })

        t_n = pd.DataFrame(n_bodies_list, columns=['t', 'n_bodies'])

        return t_type, t_n

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None


def remove_outliers_iqr(data):
    """
    Remove outliers from a dataset using the IQR method.

    Parameters:
        data (array-like): Input dataset (1D or 2D).

    Returns:
        np.ndarray: Dataset with outliers removed.
    """
    data = np.array(data)
    if len(data.shape) == 1:  # For 1D data
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        return data[(data >= lower_bound) & (data <= upper_bound)]
    else:  # For 2D data
        clean_data = []
        for col in range(data.shape[1]):
            q1 = np.percentile(data[:, col], 25)
            q3 = np.percentile(data[:, col], 75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            clean_col = data[(data[:, col] >= lower_bound) & (data[:, col] <= upper_bound)]
            clean_data.append(clean_col)
        return np.vstack(clean_data)
