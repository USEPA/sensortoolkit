# sensortoolkit - Troubleshooting

## Table of Contents
* [Determining a site's AQS ID](#siteid)

## Using AirData to Determine a Site's AQS ID <a name="siteid"></a>

To determine the AQS Site ID for an ambient monitoring site at which sensors have been collocated alongside reference monitors, use EPA’s [AirData Air Quality Monitors Map](https://epa.maps.arcgis.com/apps/webappviewer/index.html?id=5f239fd3e72f424f98ef3d5def547eb5)

<img src="docs/source/data/AirData_1.png" width=800/>

<img src="docs/source/data/AirData_2.png" width=150 align="right"/>

Click ‘OK’ to close the splash screen.

In the top right-hand corner, click on the layers button (icon with a set of stacked squares). By default, the ‘USA States’ layer is selected.

Scroll through the list and find the pollutant you are interested in evaluating. Layers labeled ‘Active’ correspond to sites that are actively reporting to AQS.

<!--
<img src="docs/source/data/AirData_3.png" width=150 align="right"/>
-->

Clicking on a layer will display sites with reference monitors measuring the indicated pollutant.

Below, the “PM2.5 – Active” displays all US sites in the AQS database that are actively monitoring and reporting.

<img src="docs/source/data/AirData_4.png" width=800/>

<img src="docs/source/data/AirData_5.png" width=250 align="right" padding="10px"/>

Navigate to a site of interest, either via use of the search bar in the top left-hand corner or by manually zooming in on the region in which the site is located. Clicking on the site pin will bring up information about the site and monitors measuring the specified pollutant. Ensure the address and site name correspond to the site where the air sensors were collocated. The AQS Site ID is listed at the top of the site information menu.
