###################################
## filename : shpower_predict_peak.py
###################################

import pandas as pd
import numpy as np
from statsmodels.tsa.api import VAR
import datetime
import warnings

warnings.filterwarnings(action='ignore')

class ShPowerPeakPredict:
    def powerPeakPredict(self, power_total_df, pred_cnt):

        power_total_df.reset_index(drop=True)

        # 새로운 15분 전력 속성(power15) 새로 만들기
        power_total_df['power15'] = None
        power_total_df['power15'] = power_total_df['power15'].astype('float')

        power_len =len(power_total_df)

        # 15분 전력량 속성(power15)값 계산하기
        for i in range (2, power_len) :
            power_total_df.iloc[i, 2] = round(power_total_df.iloc[i-2, 1] + power_total_df.iloc[i-1, 1] + power_total_df.iloc[i, 1],2)

        # 15분 전력량 nuul행(2개) 제거
        power_total_df = power_total_df.dropna(subset=['power15'], axis=0).reset_index(drop=True)

        # 데이터의 마지막 시각 설정
        current_time = power_total_df.iloc[-1]['date']

        # 시계열 date를 index로 지정
        power_total_df.index = power_total_df['date']
        power_total_df.set_index('date', inplace=True)

        # 훈련 및 시험 실측 데이터
        train_df = power_total_df[:-pred_cnt]

        test_df = power_total_df[-pred_cnt:]

        train = train_df.values
        test_power = test_df.values

        # VAR 모델 설정
        forecasting_model = VAR(train)
        results_aic = []

        # VAR 모델 학습
        results = forecasting_model.fit(maxlags=12, trend='ct')

        # 지연 12(60분), 6개(현재시각 포함 25분 후까지) 예측
        laaged_values = train_df.values[-12:]
        forecast = pd.DataFrame(results.forecast(y=laaged_values, steps=pred_cnt), index=test_df.index, 
                                columns=['predictpower5', 'predictpower15'])

        return forecast
