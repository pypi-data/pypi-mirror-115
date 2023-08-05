###################################
## filename : shsqlpeak.py
###################################

import pandas as pd
import pymssql as sql

# 원시데이터 로딩 및 예측결과 데이터 저장    
class ShPowerPeakData():
    # 검색조건에 대한 데이터를 읽어옴
    # 5분 전력량 데이터를 읽어오는 Query
    def selectPowerPeak(self, conn, siteCode, buildingNo, mmicd):
        query = "SELECT CONVERT(CHAR(16), CONVERT(DATETIME, SaveTime), 120) AS date"
        # 테스트를 위해 전력량 데이터가 작아 전력 데이터로 대치
        query += " , IIF(CurrentPowerKw < 0, 0, CurrentPowerKw) AS power"
        # 전력량 데이터(15분 데이터로 계산하기 위해 4를 곱해줌)
        #query += " , IIF(PowerKwInc < 0, 0, PowerKwInc)*4 AS power"
        query += " FROM T_POWER_PEAK_SAVE"
        query += " WHERE SITECODE = '" + siteCode + "'"
        query += " AND BuildingNo = '" + buildingNo + "'"
        query += " AND MMIEquipmentID = '" + mmicd + "'"
        query += " AND SaveTime BETWEEN CONVERT(VARCHAR(23), DATEADD(DAY, -14, GETDATE()),120) AND CONVERT(VARCHAR(23), GETDATE(),120)"
        query += " AND CurrentPowerKw > 0"
        query += " ORDER BY date"

        # 읽어온 데이터를 DataFrame에 저장
        total_df = pd.read_sql(query, conn, parse_dates='date')

        return total_df

    # 예측 결과데이터 저장
    def savePowerPeak(self, conn, siteCode, buildingNo, current_time, pred_cnt, forecast):
        # 예측 소비전력량 1일 단위 전력량 예측 테이블에 데이터 저장
        cursor = conn.cursor()
        for k in range(pred_cnt):
            predict_time = current_time + pd.DateOffset(minutes=(k+1)*5)
            #print(predict_time, "예측 5분전력: {:.2f}, 예측 15분전력: {:.2f}". 
            #      format(forecast.iloc[k,0], forecast.iloc[k,1]))
            
            #예측정보를 DB에 저장할 SQL 조립
            insertSql = "MERGE INTO T_POWER_PREDICT_15M F"
            insertSql += " USING (SELECT '" + siteCode + "', '" + buildingNo + "'"
            insertSql += " , CONVERT(CHAR(16), CONVERT(DATETIME, '" + str(predict_time) + "'), 120)) AS S"
            insertSql += " (SITECODE, BUILDINGNO, PREDICTDATETIME)"
            insertSql += " ON F.SITECODE = S.SITECODE AND F.BUILDINGNO= S.BUILDINGNO"
            insertSql += " AND F.PREDICTDATETIME = S.PREDICTDATETIME"
            insertSql += " WHEN MATCHED THEN"
            insertSql += " UPDATE SET"
            insertSql += " PREDICTPOWER5M = '" + str(round(forecast.iloc[k,0],2)) + "'"
            insertSql += " , PREDICTPOWER15M = '" + str(round(forecast.iloc[k,1],2)) + "'"
            insertSql += " , SAVETIME = GETDATE()"
            insertSql += " WHEN NOT MATCHED THEN"
            insertSql += " INSERT (SITECODE, BUILDINGNO, PREDICTDATETIME, PREDICTPOWER5M, PREDICTPOWER15M, SAVETIME)"
            insertSql += " VALUES('" + siteCode + "', '" + buildingNo + "'"
            insertSql += " , CONVERT(CHAR(16), CONVERT(DATETIME, '" + str(predict_time) + "'),120)"
            insertSql += " , '" + str(round(forecast.iloc[k,0],2)) + "', '" + str(round(forecast.iloc[k,1],2)) + "', GETDATE());"

            #예측정보를 테이블에 저장
            cursor.execute(insertSql)

        conn.commit()
    