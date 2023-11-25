# Team Project (Contributors: PYB(Leader), PCH, CSK, PJC, and KYJ)
## Goal: Vertiport Placement in Gyeongsangbuk-do and Daegu for efficient middle-mile consignment of fresh food
See results of `mapping.ipynb` in [here](https://nbviewer.org/github/HowveYoobin/Big_Data_Design/blob/main/Team_project/mapping.ipynb)

## Progress of the project
### 1. Background Research
### 2. Scoped down the project topic and collected related data.
### 3. Mapped prohibited-, restricted-, and dangered- flight areas on the map of Gyeongsangbuk-do(w.o. Ulleung-do) and Daegu with Vworld API.  
    
<figure>
    <img src="./figures/no_ulleung_label.png" alt="No-flight zones"/>
    <figcaption>Figure 1. No-flight zones in Daegu and Gyeongsangbuk-do(w.o. Ulleung-do</figcaption>
    </figure>

### 4. Marked locations with high slopes according to EASA vertiport guidelines on the map with QGIS and python.
* Marked unavailable slopes according to EASA vertiport guidelines on the map by QGIS.
    <figure>
    <img src="./figures/slope.png" alt="Unavailable slope(QGIS)"/>
    <figcaption>**Figure 2.** Unavailable slopes marked by QGIS </figcaption>
    </figure>
* Marked slopes according to EASA vertiport guidelines on the map by matplotlib.pyplot (Python).
    <figure>
    <img src="./figures/slope_python.png" alt=Unavailable slope(python)"/>
    <figcaption>**Figure 3.** Available(middle) Unavailable slopes(right) marked by matplotlib.pyplot(Python)</figcaption>
    </figure> 

### 5. Marked warehouses, new-TK airport, and places with high slopes by matplotlib.pyplot.
<p align="center">
  <img src="./figures/warehouse+airport.png" align="center" width="49%">
  <img src="./figures/warehouse+airport+slope.png" align="center" width="49%">
  <figcaption align="center"><B>Figure 4.</B> Locations of the warehouses(blue point) and new TK airport(star) were marked on the left map. The places with unavailable slopes(gray point) were marked on the right map.</figcaption>
</p>

6. Finding out the relationship between warehouse size and the amount of delivery traffic in Hwaseong.
   * Reducing computational cost by using server
  
6. 기체 선정 및 middle mile에서 UAM의 필요성
