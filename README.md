# Airflow
- 머신러닝 기반 주가 예측 프로젝트의 데이터를 자동으로 수집해옵니다. 

- 파일 실행환경
  1. Ubuntu Server 18.04 LTS version
  2. Python 3.6.9 version
  
 - 모듈 설치
 ```
 $pip install -r requirements.txt
 ```

------------

### test_dag.py
 Apache Airflow DAG 구성 테스트 코드 입니다. 3개의 수집 코드를 스케줄링 합니다.
 
 - 테스트 실행 방법 
 ```
 $python test [dag_id] [task_id] [date]
 ```
 - example
 ```
 $python airflow test test_dag get_price 20200101
 ```   

------------

### get_price_airflow.py
 코드를 돌린 해당 날짜의 삼성전자 주가 데이터를 수집하여 Cosmos DB에 적재하는 코드입니다.
 
 - 사용법
 1. 파일을 Airflow 폴더에 저장합니다.
 2. 파일을 열어 insert_price 함수 안에 있는 config 변수에 Cosmos DB의 end point값(URL)과 primary key 값을 입력합니다.
 
 - 파일만 개별적으로 실행시켜보고 싶을 경우, cmd 또는 terminal에 아래 명령어를 입력합니다.
 ```
 $python get_price_airflow.py
 ```
 
 
------------

### get_fs_airflow.py
 가장 최근의 재무제표 데이터와 코드를 돌린 해당 날짜의 주가 데이터를 활용해 PER,PBR,ROE 지표를 계산한 후 Cosmos DB에 적재하는 코드입니다.
 

- 사용법
1. 파일을 Airflow 폴더에 저장합니다.
2. concat_years_report함수 안에 DART API key 값을 입력합니다. 
  - DART는 전자공시시스템이며 Open API를 제공합니다.
  - https://opendart.fss.or.kr/ 에서 인증키 신청/관리 → 인증키 신청을 눌러 이메일 인증을 하면 API key를 받을 수 있습니다.
3. get_stockprice함수와 insert_fs함수 안에 있는 config 변수에 Cosmos DB의 end point값(URL)과 primary key 값을 입력합니다.


- 파일만 개별적으로 실행시켜보고 싶을 경우, cmd 또는 terminal에 아래 명령어를 입력합니다.
 ```
 $python get_fs_airflow.py
 ```  

------------

### get_bond_airflow.py
 코드를 돌린 해당 날짜의 한국 채권 10Y 데이터를 수집하여 Cosmos DB에 적재하는 코드입니다. 

본인의 end point값과 primary key 값을 넣어주면 azure cosmosdb container에 CSV파일 데이터가 적재됩니다.  
 
 - 사용법
 1. 파일을 Airflow 폴더에 저장합니다.
 2. 파일을 열어 insert_bond 함수 안에 있는 config 변수에 Cosmos DB의 end point값(URL)과 primary key 값을 입력합니다.

 - 파일만 개별적으로 실행시켜보고 싶을 경우, cmd 또는 terminal에 아래 명령어를 입력합니다.
 ```
 $python get_bond_airflow.py
 ```

