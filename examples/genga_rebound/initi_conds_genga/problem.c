#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "rebound.h"

char TITLE[100] = "merger_";


double get_radii(double m, double rho){
    return pow((3*m)/(4*M_PI*rho),1./3.);
}

int main(int argc, char* argv[]){
    struct reb_simulation* r = reb_simulation_create();
    r->G = 39.476926421373;
    r->dt = 6./365.;
    //r->exit_max_distance = 100.; 

    // The random seed is passed as a command line argument
    if (argc == 2){
        r->rand_seed = atoi(argv[1]);
        strcat(TITLE, argv[1]);
    }
    r->integrator = REB_INTEGRATOR_MERCURIUS;
    r->collision = REB_COLLISION_DIRECT;
    r->collision_resolve = reb_collision_resolve_merge;

        //Assigning mass and number of planetary embryos and planetesimals
    double rho = 5.05e6; //3 g/cm^3
    int n_emb = 14; //number of planetary embryos
    double m_emb = 2.8e-7; //mass of each embryo
    int n_pl = 140; //number of planetesimals
    double m_pl = 2.8e-08;
    int ef = 1;
    double a_pl[n_pl];  // Array to hold the values of planetesimal semi-major axis
    double a_emb[n_emb]; // Same for embryos

    FILE *file_pl = fopen("cham_bimodal_pl_samples_sep3.txt", "r");
    for (int i = 0; i < n_pl; i++) {
        fscanf(file_pl, "%lf", &a_pl[i]);}
    // Close the file after reading
    fclose(file_pl);

    FILE *file_emb = fopen("cham_bimodal_emb_samples_sep3.txt", "r");
    for (int i = 0; i < n_emb; i++) {
        fscanf(file_emb, "%lf", &a_emb[i]);}
    // Close the file after reading
    fclose(file_emb);


    struct reb_particle star = {0};
    star.m = 1.00;
    star.r = 0.1; 
    star.hash = 0; 
    reb_simulation_add(r, star);
    FILE* of_dbcti = fopen("genga_input.txt","a+");
    
    // Add planetary embryos
    
    for (int i=0; i<n_emb; i++){
        double a = a_emb[i];      // semi major axis
        double m = m_emb;
        double inc = reb_random_uniform(r,0,0.0175);
        double ecc = reb_random_uniform(r,0,0.01);
        double omega = reb_random_uniform(r,0,2*M_PI);
        double Omega = reb_random_uniform(r,0,2*M_PI);
        double f = reb_random_uniform(r,0,2*M_PI);
        double hash = i + 1;
        //now build particle from orbit
        struct reb_particle emb = reb_particle_from_orbit(r->G, star, m, a, ecc, inc, Omega, omega, f);
        emb.r = get_radii(m, rho)*ef;
        emb.hash = hash;
        
        reb_simulation_add(r, emb); 

        fprintf(of_dbcti, "%e\t", m);
        fprintf(of_dbcti, "%e\t", a);
        fprintf(of_dbcti, "%e\t", ecc);
        fprintf(of_dbcti, "%e\t", inc);
        fprintf(of_dbcti, "%e\t", Omega);
        fprintf(of_dbcti, "%e\t", omega);
        fprintf(of_dbcti, "%e\t", f);

        fprintf(of_dbcti, "\n"); 
    }
    //add planetesimals
    for (int i=0; i<n_pl; i++){
        double a = a_pl[i];      // semi major axis
        double m = m_pl;
        double inc = reb_random_uniform(r,0,0.0175);
        double ecc = reb_random_uniform(r,0,0.01);
        double omega = reb_random_uniform(r,0,2*M_PI);
        double Omega = reb_random_uniform(r,0,2*M_PI);
        double f = reb_random_uniform(r,0,2*M_PI);
        double hash = n_emb + i + 1;
        //now build particle from orbit
        struct reb_particle pl = reb_particle_from_orbit(r->G, star, m, a, ecc, inc, Omega, omega, f);
        pl.r = get_radii(m, rho)*ef;
        pl.hash = hash;
        
        reb_simulation_add(r, pl); 

        fprintf(of_dbcti, "%e\t", m);
        fprintf(of_dbcti, "%e\t", a);
        fprintf(of_dbcti, "%e\t", ecc);
        fprintf(of_dbcti, "%e\t", inc);
        fprintf(of_dbcti, "%e\t", Omega);
        fprintf(of_dbcti, "%e\t", omega);
        fprintf(of_dbcti, "%e\t", f);
    }

    fclose(of_dbcti);



    reb_simulation_move_to_com(r);  // This makes sure the planetary systems stays within the computational domain and doesn't drift.
    double run_time = 1;
    reb_simulation_save_to_file_interval(r,TITLE,1.e5);
    reb_simulation_integrate(r, run_time);
}

//void heartbeat(struct reb_simulation* r){
//    if (reb_simulation_output_check(r, 1.e3)){  
//        reb_simulation_output_timing(r, 0);
//        printf("Walltime(s) = %f \n", r->walltime); 
//    }
//}

