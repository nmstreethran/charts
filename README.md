# Charts

&nbsp; | Source | Output
-- | -- | --
***Interactive charts***
**Google Charts** | [**Google's interactive visualisation library**](https://developers.google.com/chart)
Area chart | [![View HTML](badges/html.svg)](charts/google/areachart.html) [![View JavaScript](badges/javascript.svg)](charts/google/areachart.js) | [![View output on JSFiddle](badges/jsfiddle.svg)](https://jsfiddle.net/nithiya/yt7ab0Lo/)
Bar chart | [![View HTML](badges/html.svg)](charts/google/barchart.html) [![View JavaScript](badges/javascript.svg)](charts/google/barchart.js) | [![View output on JSFiddle](badges/jsfiddle.svg)](https://jsfiddle.net/nithiya/qxcpz345/)
Column chart | [![View HTML](badges/html.svg)](charts/google/columnchart.html) [![View JavaScript](badges/javascript.svg)](charts/google/columnchart.js) | [![View output on JSFiddle](badges/jsfiddle.svg)](https://jsfiddle.net/nithiya/df0bmjt1/)
Gantt chart | [![View HTML](badges/html.svg)](charts/google/ganttchart.html) [![View JavaScript](badges/javascript.svg)](charts/google/ganttchart.js) | [![View output on JSFiddle](badges/jsfiddle.svg)](https://jsfiddle.net/nithiya/s2kye3md/)
Pie chart | [![View HTML](badges/html.svg)](charts/google/piechart.html) [![View JavaScript](badges/javascript.svg)](charts/google/piechart.js) | [![View output on JSFiddle](badges/jsfiddle.svg)](https://jsfiddle.net/nithiya/nm5pgksj/)
**Bokeh**
Simple polygons | [![View Python script](badges/python.svg)](charts/python/bokeh_polygon.py) | [![View Jupyter Notebook](badges/jupyter.svg)](https://nbviewer.org/github/nmstreethran/charts/blob/main/docs/python/bokeh_polygon.ipynb)
Points | [![View Python script](badges/python.svg)](charts/python/bokeh_points.py) | [![View Jupyter Notebook](badges/jupyter.svg)](https://nbviewer.org/github/nmstreethran/charts/blob/main/docs/python/bokeh_points.ipynb)
***Static plots***
**Matplotlib**
Raster visualisation with rioxarray - digital terrain model | [![View Python script](badges/python.svg)](charts/python/rioxarray.py) | [![View Jupyter Notebook](badges/jupyter.svg)](https://nbviewer.org/github/nmstreethran/charts/blob/main/docs/python/rioxarray.ipynb)
Raster visualisation with rioxarray - land cover map | [![View Python script](badges/python.svg)](charts/python/rioxarray_lc.py) | [![View Jupyter Notebook](badges/jupyter.svg)](https://nbviewer.org/github/nmstreethran/charts/blob/main/docs/python/rioxarray_lc.ipynb)
Vector visualisation with GeoPandas | [![View Python script](badges/python.svg)](charts/python/geopandas.py) | [![View Jupyter Notebook](badges/jupyter.svg)](https://nbviewer.org/github/nmstreethran/charts/blob/main/docs/python/geopandas.ipynb)
**R**
Lattice levelplots | [![View R script](badges/r.svg)](charts/r/lattice_plot.r) | [![View Jupyter Notebook](badges/jupyter.svg)](https://nbviewer.org/github/nmstreethran/charts/blob/main/docs/r/lattice.ipynb)
Raster visualisation with rasterVis | [![View R script](badges/r.svg)](charts/r/rastervis_plot.r) | [![View Jupyter Notebook](badges/jupyter.svg)](https://nbviewer.org/github/nmstreethran/charts/blob/main/docs/r/rastervis.ipynb)
Simple vector feature visualisation with sf | [![View R script](badges/r.svg)](charts/r/sf_plot.r) | [![View Jupyter Notebook](badges/jupyter.svg)](https://nbviewer.org/github/nmstreethran/charts/blob/main/docs/r/sf.ipynb)

## QGIS maps

See [maps](maps).

## Environments

### Python

See [requirements.txt](requirements.txt)

### R

```sh
conda create --channel conda-forge --name r-env r-base r-essentials r-rgdal r-rastervis r-sf r-geojsonio jupyterlab
conda activate r-env
R -e "IRkernel::installspec()"
```

<!-- ### JavaScript

```sh
conda create --channel conda-forge --name js-env nodejs jupyterlab
conda activate js-env
npm install --global ijavascript
ijsinstall
``` -->

## References

1. [Ingesting chart data from Google Sheets](https://developers.google.com/chart/interactive/docs/spreadsheets)
2. [Using Google Charts to draw a Gantt chart using data from a Google Sheet](https://stackoverflow.com/a/42335062)
3. [Label Python data points on plot](https://stackoverflow.com/a/22272358)
4. [Matplotlib colormap reference](https://matplotlib.org/stable/gallery/color/colormap_reference.html)
5. [Matplotlib discrete colorbar](https://stackoverflow.com/q/14777066)
6. [Merge/mosaic of multiple TIFF files using rioxarray](https://gis.stackexchange.com/q/376685)
7. [GeoPandas Mapping and Plotting Tools](https://geopandas.org/en/stable/docs/user_guide/mapping.html)
8. [rasterVis FAQ](https://oscarperpinan.github.io/rastervis/FAQ.html)
9. [Customizing Matplotlib with style sheets and rcParams](https://matplotlib.org/stable/tutorials/introductory/customizing.html)
10. [Matplotlib style sheets reference](https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html)
11. [How to change the size of R plots in Jupyter](https://stackoverflow.com/a/60196822)
12. [R colorspace](https://colorspace.r-forge.r-project.org/)
13. [Using Bokeh with Jupyter](https://docs.bokeh.org/en/latest/docs/user_guide/jupyter.html)
14. [Mapping geo data with Bokeh](https://docs.bokeh.org/en/latest/docs/user_guide/geo.html)

<!-- 1. [IJavaScript](https://github.com/n-riesco/ijavascript)
1. [HTML output using IJavaScript](https://n-riesco.github.io/ijavascript/doc/custom.ipynb.html#$$.html(htmlString)) -->

## License

Code samples are licensed under the Apache License, Version 2.0 (Apache-2.0).

---

Copyright 2018-2022 Nithiya Streethran (nmstreethran at gmail dot com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

<https://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

---

Project badges are generated using [Shields.io](https://shields.io/) and [Simple Icons](https://simpleicons.org/).
