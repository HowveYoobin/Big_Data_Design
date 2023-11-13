# Assignment 2. EDA report
## Exploratory Data Analysis report
  * Submit analytic reports regarding the given data (Use Markdown)
  * Explore the data and find recognizable pattern or any meaningful information
  * From this finding, create your own topic (or problem) and suggest possible solution
  * Data exploration + visualization • Structure
  * Data overview: descriptives statistics on overall data (sample size, number of variables, data type, data range, distribution, etc.)
  * Univariate analysis: understanding key variables from various aspects
  * Multivariate analysis: finding patterns between variables (correlation, clustering, etc.)
  * Suggestion: Based on the insights you obtained from the previous stages, propose the potential project idea

## Guidelines
  * Minimum 3, Maximum 6 figures→explanations for each figures are necessary • Minimum 1, maximum 3 tables→explanations for each figures are necessary
  * Evaluation (Rank evaluation, professor:classmate = 7:3)
  * Requirements (5 %): figures & tables
  * Format (5 %): format and sections
  * Logical flow (20 %): Is the storyline of EDA report well made?
  * Writing quality (15 %): Is the report written in a high quality?
  * Visualization quality (15 %): Is the visualized figure create in a high quality?
  * Novelty of suggested solution (10 %): Is the suggested solution novel?
  * Appropriateness of suggested solution (10 %): Is the suggested solution appropriate?
  * Proofreading (5 %): Full credit only if there is no typo or grammar error
  * Comments (15 %): Evaluated by professor
---
## Feedback
* 보고서에는 필요한 그림만 골라서 넣어야 한다. 그림이 너무 많아서 변수들이 잘 보이지 않는다.
* 그림들이 맞는지 확인하고 이를 설명할 수 있는 그림만 넣자.
* 내 컴퓨터 소스가 어쩌고는 적지 말자. 읽는 사람 입장에서는 '어쩌라고?' 생각이 든다. 컴퓨터가 버벅거리더라도 해낼 수 있도록 스킬을 고도화하자.
* 주어진 데이터는 **Pannel data**인데 이에 대해 처리를 안했다. 원데이터를 면밀하게 검토하자.
* 원데이터에서 너무 많은 데이터를 날리면 안된다.

### Panel data
* 종단자료 또는 경시적 자료 (longitudinal data)라고도 하며, **특정 개체들**을 선정하고 이들을 **복수의 시간**에 걸쳐서 동일한 항목에 대해 반복적으로 추적하여 얻는 데이터
* 조사 대상 개체를 **패널**이라고 한다.
* 패널 데이터의 각 변수가 가지는 두 차원의 변동
  1. 개체 차원: 동일한 시기라 하더라도 변수의 값은 개체 간에 상이할 수 있다.
  2. 시간 차원: 각 개체의 변수값은 시간에 따라 변화할 수 있다. 




### Panel data vs cross-sectional data vs time-series data

|    |Panel data|Cross-sectional data|time-series data|
|:--:|:---:|:---:|:---:|
|특징|특정 개체들을 선정하고 이들을 복수의 시간에 걸쳐서 반복적으로 추적| 특정 시간에 복수의 개체들을 관측|한 대상을 복수의 시간에 걸쳐 관측|
|시점|여러 개|하나|여러 개|
|개체|여러 개|여러 개|하나|
|변수|${x_{it}}$|${x_i}$|${x_t}$|

* 예시
  
    ${log(임금_{it}=\alpha_t + \beta학력_i + \gamma\log(국민소득_t)+u_{it}}$

    * 임금: 개인별, 시간별로 다를 수 있는 변수
    * 학력: 개인별로는 다를 수 있지만 시간에 걸쳐서는 동일하다.
    * 국민소득: 모든 개인들에게 동일하지만 시간에 따라서 변화한다.
    * 오차항: 개인들 간에도 다르고 시간에 따라서도 변화한다.
    * ${\alpha}$: 절편은 시간에 따라 다르다.
    * ${\beta,\gamma}$: 모든 개인과 시간에 걸쳐 동일하다.
  
### Analysis of Panel Data
* 분석을 하기전에 자료들의 여러 feature들을 살펴보고, 반복된 시점에 따라 각 개체(패널)의 변동을 나타내는 그림을 그리면 좋다.
* 패널 수가 많으면 패널들 중 일부를 무작위하게 선정하여 선정한 패널들이 시점에 따라 어떻게 변하는지를 나타내도 좋다.
* 설명 변수(${X}$)의 그룹에 따른 비교를 하고 싶으면 각 그룹별로 분포를 비교하면 도움이 됨.
