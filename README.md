# VOC_RECAP

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10655470.svg)](https://doi.org/10.5281/zenodo.10655470)
Citation: https://doi.org/10.1016/j.atmosenv.2024.120847

Shenglun Wu
Correspondance should be addressed to shlwu@ucdavis.edu

## Summary
This repository is for data analysis of results from VOC measurements in Pasadena and Redlands during RECAP-CA 2021. The goal of this project is to understand the importance of different source of VOCs especially biogenic VOC (BVOC) and volatile chemical products (VCPs) to Ozone ($O_3$) formation in the South Coast Air Basin (SoCAB)

## Overview
This repository contains data, code, result.
- code
    - src
    - script
- data
    - raw
        - /Model_input_nosource: box model input file (no tag)
        - df_VOC_CARB_Chamber_DNPHcorrected.csv: VOC measurement data in Redlands (DNPH sample corrected)
        - PMF_input_conc.csv
        - PMF_input_uncertainty.csv
        - PMF_species_saprc.csv: PMF input VOC compounds and their SAPRC name
        - saprc11_rev4_bgX.doc: notes of SAPRC11 tag species
        - TEMP_PICKDATA_2021-12-31_RL.csv: ambient temperature data, published by CARB
        - VOC_reactivity_MIR_redlands.csv: VOC reactivity and MIR coefficients
        - WINSPD_PICKDATA_2021-10-31.csv: ambient wind profile, published by CARB 
    - intermediate
    - final
- result
