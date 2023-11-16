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
        #### Label을 그림 위에 나타내도록 하고, 울릉도는 날리기 (동해쪽의 비행제한, 금지 구역은 삭제)
    <img src="no_flight_folium.png" alt="No-flight zones"/>
    <figcaption>Figure 2. No-flight zones(Folium)</figcaption>
    </figure>
4. Marked locations with slopes more than 26 degrees on the map with QGIS.
    <figure>
    <img src="slope.png" alt="slope > 26"/>
    <figcaption>Figure 3. No-flight zones(matplotlib)</figcaption>
    </figure>
