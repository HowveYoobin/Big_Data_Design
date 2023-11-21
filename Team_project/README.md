# Team Project
## Contriutors: PCH, CSK, PJC, and KYJ
## Vertiport Placement in Gyeongsangbuk-do and Daegu for efficient middle-mile consignment of the fresh food
---
mapping.ipynb -> https://nbviewer.org/github/HowveYoobin/Big_Data_Design/blob/main/Team_project/mapping.ipynb

### Progress
1. Background Research
2. Scoped down project topic and collected data.
3. Mapped prohibited-, restricted-, dangered- flight area on the map of Gyeongsangbuk-do and Daegu with Vworld API.
    <figure>
    <img src="no_flight_plt.png" alt="No-flight zones"/>
    <figcaption>Figure 1. No-flight zones(matplotlib)</figcaption>  
        
    <img src="no_flight_folium.png" alt="No-flight zones"/>
    <figcaption>Figure 2. No-flight zones(Folium)</figcaption>

    <img src="no_ulleung_label.png" alt="no_ulleung"/>
    <figcaption>Figure 3. No-flight zones in Daegu and Gyeongsangbuk-do</figcaption>
    </figure>
    
4. Marked locations with slopes more than 26 degrees on the map with QGIS.
    <figure>
    <img src="slope.png" alt="slope by QGIS"/>
    <figcaption>Figure 4. QGIS slopes(>26)</figcaption>
    </figure>  
    * QGIS -> python matplotlib
    <figure>
    <img src="slope_python.png" alt="slope by python"/>
    <figcaption>Figure 5. Python slopes (matplotlib)</figcaption>
    </figure> 
5. Finding out the relationship between warehouse size and the amount of delivery traffic in Hwaseong.
   * Reducing computational cost by using server
  
6. 기체 선정 및 middle mile에서 UAM의 필요성
    * alia의 Travel time 추정 필요
          1. 가격
          2. tavel time
    * 기아 트럭에 맞춘 travel time/ traffic은 카카오네비 api 등을 이용해서 충분히 계산할 수 있을 것
