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
    * **Label을 그림 위에 나타내도록 하고, 울릉도는 날리기 (동해쪽의 비행제한, 금지 구역은 삭제)**  
    <img src="no_flight_folium.png" alt="No-flight zones"/>
    <figcaption>Figure 2. No-flight zones(Folium)</figcaption>
    </figure>
    
    <figure>
    <img src="no_ulleung_label.png" alt="no_ulleung"/>
    <figcaption>Figure 3. No-flight zones in Daegu and Gyeongsangbuk-do</figcaption>
    </figure>

    
4. Marked locations with slopes more than 26 degrees on the map with QGIS.
    <figure>
    <img src="slope.png" alt="slope > 26"/>
    <figcaption>Figure 4. No-flight zones(matplotlib)</figcaption>
    </figure>  
    * QGIS를 가지고 capability를 만들어오기.
5. Finding out the relationship between warehouse size and the amount of delivery traffic in Hwaseong.
   * Decrease the computational cost by ???
   * 빅데이터 사업단에서 운영하고 있는 서버 컴퓨터 사용하여 API 주소 작업을 끝내보자! (김경외 교수님께 김정현 교수님 cc 걸어서 문의)
   * warehouse와 물송량간의 관계를 정립해서 이영재 책임님께 확인받기
   * QGIS는 화요일에 capable하다는 것을 데모하는 수준으로 보여주면 좋을 것
  
6. 기체 선정 및 middle mile에서 UAM의 필요성
    * alia의 Travel time 추정 필요
    * 1. 가격, 2. tavel time
    * 기아 트럭에 맞춘 travel time/ traffic은 카카오네비 api 등을 이용해서 충분히 계산할 수 있을 것
    * 다 뿌린게 다 모아지는 것이 화성 창고의 demand
    * 창고의 크기 대비 수요량 상관관계 (CJ)
   Action item
* 일정: 다음주 화요일 (저녁 7시)
* 내부 미팅은 책임님 미팅 전에 오전 11시 15분
* 


Action item
* 충호 + 주찬 따로 하지 말고 같이 한 팀으로 하나로!
