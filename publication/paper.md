---
title: 'sensortoolkit: A Python Code Library for Standardizing the Ingestion, Analysis, and Reporting of Air Sensor Data for Performance Evaluations'
tags:
  - Python
  - air sensors
  - air quality
  - performance evaluation
  - sensor data analysis
  - data visualization
authors:
  - name: Samuel G. Frederick
    orcid: 0000-0000-0000-0000
    affiliation: 1
  - name: Karoline K. Barkjohn
    affiliation: 2
  - name: Rachelle M. Duvall
    affiliation: 2
  - name: Andrea L. Clements^[Corresponding author]
    affiliation: 2
affiliations:
 - name: Oak Ridge Associated Universities (ORAU), contractor to U.S. Environmental Protection Agency through the National Student Services Contract, 100 ORAU Way, Oak Ridge, TN 37830
   index: 1
 - name: U.S. Environmental Protection Agency, Office of Research and Development, 109 T.W. Alexander Drive, Research Triangle Park, NC 27711
   index: 2
date: 5 May 2022
bibliography: paper.bib

---

# Summary

Past efforts to establish open-source software tools for reporting air sensor performance have been limited. Sensor and reference data formats vary widely, and in turn, many existing software packages evaluate only one type of sensor model. Other packages allow broader utilization of air quality data yet may not be specifically tailored for evaluating sensor performance against reference data. Additionally, these packages do not provide means for summarizing sensor performance in a reporting template using common statistical metrics and figures. To encourage broader utilization of the U.S. Environmental Protection Agency’s (EPA) recommended performance metrics and target values for sensors measuring fine particulate matter (PM<sub>2.5</sub>) and ozone (O<sub>3</sub>), EPA has developed an open-source Python package named **sensortoolkit**. The package compares collocated sensor data against reference monitor data and includes methodology to re-format both datasets into a standardized format using an interactive setup module. Library modules are included for calculating EPA’s recommended sensor performance metrics and for making relevant plots. These metrics and plots can be used to better understand sensor accuracy, precision between sensors of the same make and model, and the influence of meteorological parameters at 1-hour and 24-hour averages. Results can be compiled into the reporting template included alongside EPA’s performance targets documents. The **sensortoolkit** package is designed for broad accessibility, making it suitable for individuals ranging from users curious about their air quality to researchers evaluating the performance of air sensors.  

# Statement of Need

Air sensors have undergone rapid adoption in recent years, heralding a new era for air quality monitoring and environmental data collection that is marked by broader access to insightful air quality data. Air sensors have been used in numerous non-regulatory, supplemental, and informational monitoring (NSIM) applications such as community-wide network deployments which increase the spatial density of local monitoring, analysis of high-time resolution temporal trends in pollutant concentrations, and educational programs aimed at increasing community awareness of local pollutant sources and air quality trends [@RN32, @RN65, @RN65, @RN17]. Heightened public awareness and contribution regarding the use of air sensors in NSIM applications has allowed an unprecedented level of engagement between community members directly affected by the impacts of air pollution and regulatory agencies that oversee existing regulatory monitoring networks and are thus able to aid programs by offering a wealth of institutional knowledge and monitoring data.

Despite the significant transformation air sensors have facilitated in altering how monitoring efforts are undertaken, it is well established that the data quality of air sensors varies widely, including sensors measuring particulate matter (PM) [@RN21, @RN15] and sensors measuring gaseous pollutants (e.g., O<sub>3</sub>, NO<sub>2</sub>, SO<sub>2</sub>) [@RN21, @RN78]. Air sensors are not subject to the rigorous standards for measurement accuracy and precision that regulatory-grade instruments must meet. In the United States, the U.S. Environmental Protection Agency (U.S. EPA) designates candidate methods as either Federal Reference Methods (FRMs) or Federal Equivalent Methods (FEMs) following extensive testing to ensure compliance with performance standards set by the Agency [guidelines for applicants, 50 CFR part 53]. Conducting air sensor performance evaluations by collocated devices alongside FRM/FEM instruments at ambient monitoring sites is crucial to quantifying the accuracy, precision, and bias of sensor measurements. Furthermore, consistent protocols for evaluating and reporting air sensor performance are essential to equipping sensor users, regardless of skillset, with adequate knowledge for selecting sensors suited for their intended applications.

In February 2021, U.S. EPA released two documents outlining performance testing protocols, metrics, and target values for sensors measuring either particulate matter smaller than 2.5 microns in aerodynamic diameter (PM<sub>2.5</sub>) [@RN42] or sensors measuring O<sub>3</sub> [@RN54]. These documents, subsequently referred to as U.S. EPA’s Performance Targets Reports, provide recommended procedures for testing sensors for use in ambient, outdoor, fixed-site settings. Testing is divided into two phases, including “base testing” of sensors at an ambient monitoring site and “enhanced testing” in a laboratory chamber. During each phase, sensors are collocated alongside an FRM or FEM. For base testing, U.S. EPA’s Performance Targets Reports recommend evaluating sensor performance against a suite of performance metrics and associated target ranges and goal values. Testers are encouraged to compile base testing results, including figures and tabular statistics, into a reporting template included alongside each Performance Targets Report.

While numerous standards have been recommended for evaluating air sensors, including those detailed in U.S. EPA’s Performance Targets Reports, protocols developed by South Coast Air Quality Management District’s (SCAQMD) Air Quality Sensor Performance Evaluation Center (AQ-SPEC) [@RN109], AIRLAB (Airparif)(include?), a significant challenge towards standardized methods persists due to the lack of a consistent formatting standard for how air sensor data are recorded. As a result, individuals intending to evaluate air sensor data may need to develop custom code for data analysis, including functions for data ingestion, calculation of statistical metrics, and the creation of figures which visualize sensor performance relative to reference methods. Such code may not be extensible to numerous sensor data formats or pollutants, requiring individuals to create sensor-specific code. This fragmented approach to analyzing sensor data is time-intensive and complicates the accessibility of air sensor use if extensive coding knowledge is required to draft insights regarding sensor performance.

In response to the need for software utilities that allow analysis and visualization of data acquired from air sensors, numerous groups and companies have proposed solutions. However, existing utilities are limited by scope and/or access. Some sensor manufacturers offer online platforms for viewing sensor measurements, status, and occasionally the ability to download data via an application programming interface (API). These platforms are frequently offered to customers via a “software as a service” business model, whereby the sensor user pays a periodic subscription fee, granting them access to the platform. Such platforms may prove costly for individuals or groups operating under a limited budget. Other tools for analyzing sensor data are provided as downloadable software packages. These packages are typically comprised of modules and functions, written in one or multiple coding languages, which allow users to import sensor data on the user’s system or acquire data from an API and generate various statistical values and figures. Software packages are commonly provided as free and open-source software and may be built on open-source programming languages such as R or Python. Existing open-source packages for analyzing air sensor data may be limited to a single sensor, such as the AirSensor R package developed by SCAQMD and Mazama Science [cite] which provides an extensive set of tools for analyzing data collected by the PurpleAir PA-II.  Other software packages, such as OpenAir [cite] allow broader utilization of air quality data; however, such software may not be specifically tailored to air sensor data and thus lack important in-package utilities for evaluating air sensor performance against regulatory-grade data.

We introduce the free and open-source Python package ****sensortoolkit**** for the analysis of air sensor data. Use of the **sensortoolkit** package can be divided into three main categories: 1) the ingestion and import of both sensor and reference data from a variety of data formats into a consistent and standardized formatting scheme, 2) time averaging and analysis of sensor data using statistical metrics and target values recommended by U.S EPA’s Performance Targets Reports as well as visualization of sensor data trends via scatter plots, time series graphs, etc., and 3) compilation of performance evaluation results into the standardized reporting template provided alongside the Performance Targets Reports. The **sensortoolkit** library is most suitable for individuals who have some prior coding experience in Python. The library is equipped with an API that allows for ease of navigation and selection of library modules and methods. The library’s functionality is mediated by a user-friendly object-oriented approach. This streamlines the need for user-end input while allowing for reliable interoperability between **sensortoolkit** subroutines.

<!--
# Mathematics

Single dollars ($) are required for inline mathematics e.g. $f(x) = e^{\pi/x}$

Double dollars make self-standing equations:

$$\Theta(x) = \left\{\begin{array}{l}
0\textrm{ if } x < 0\cr
1\textrm{ else}
\end{array}\right.$$

You can also use plain \LaTeX for equations
\begin{equation}\label{eq:fourier}
\hat f(\omega) = \int_{-\infty}^{\infty} f(x) e^{i\omega x} dx
\end{equation}


# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.


For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"


# Figures


Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
![Caption for example figure.](figure.png){ width=20% }

-->
# Disclaimer

The views expressed in this publication are those of the author(s) and do not necessarily represent the views or policies of the U.S. Environmental Protection Agency. Any mention of trade names, products, or services does not imply an endorsement by the U.S. Government or the U.S. Environmental Protection Agency. The EPA does not endorse any commercial products, services, or enterprises.

# Acknowledgements

The authors wish to acknowledge the contribution of numerous individuals both internal and external to EPA who provided meaningful insight regarding the development of the **sensortoolkit** code library: James Hook (EPA-OLEM), Terry Brown (EPA-ORD), Kenneth Docherty and Brittany Thomas (Jacobs), and Ashely Collier-Oxandale (South Coast Air Quality Management District).


# References
