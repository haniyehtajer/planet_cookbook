import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from planet_cookbook import read_reports as rr
import os
import rebound
pd.set_option("display.float_format", "{:.3e}".format)

sol_to_earth = 332946.078
G = 6.6743* 10**(-11) #N⋅m2/kg2
M_sun = 1.989e+33 #g
AU = 1.496e+13 #cm

def get_particle_evolution_history(simarchive_path, hash):
    simarchive = rebound.Simulationarchive(simarchive_path)
    sim_dataframe = pd.DataFrame(columns=['t', 'm', 'a'])
    for i in range(int(len(simarchive))):
        instance = simarchive[i]
        sim_dataframe.loc[i, 't'] = instance.t
        
        for particle in instance.particles:
            if particle.hash.value == int(hash):
                sim_dataframe.loc[i, 'm'] = particle.m
                sim_dataframe.loc[i, 'a'] = particle.a
                break  # stop once found

    
    sim_dataframe['m'] = sim_dataframe['m'] * sol_to_earth
    return sim_dataframe

def get_particle_collision_history(coll_report_path, hash):
    coll_hist_array = np.loadtxt(coll_report_path,  usecols=(0, 1, 2, 3, 4, 5, 6, 7) )
    coll_hist = pd.DataFrame(coll_hist_array, columns=['t', 'type', 'b', 'hash_t', 'm_t', 'r_t', 'hash_p', 'r_p'])
    return coll_hist

def plot_a_m_hist(evolution_hist, coll_hist, xlim):
    plt.figure(figsize=(20,6))

    plt.subplot(2,1,1)
    plt.scatter(evolution_hist['t'], evolution_hist['a'])
    plt.grid('True', alpha = 0.2)
    plt.ylabel('Semi-major axis (AU)')
    plt.xlim(0,xlim)

    plt.subplot(2,1,2)
    for t, type in zip(coll_hist['t'], coll_hist['type']):
        if (type == 3) | (type == 4):
            color = 'red'
        if type == 1:
            color = 'blue'
        if type == 0:
            color = 'gray'
        if type == 2:
            color = 'green'
        plt.axvline(t, color = color, alpha = 0.5)

    plt.scatter(evolution_hist['t'], evolution_hist['m'])
    plt.grid('True', alpha = 0.2)
    plt.ylabel(r'$Mass (M_{\oplus})$')
    plt.xlabel('Time (years)')
    plt.xlim(0,xlim)

    plt.tight_layout()
    plt.show()


