# -*- coding: utf-8 -*-
"""졸프_10_31(GRU)

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13y9qRP2wsG2LCPrbC5Kt_j8YVhVzhf_n
"""

#코스피 지수 오류로 야후 데이터로 임시 진행

# !pip install -U finance-datareader

# # 라이브러리 임포트
# import FinanceDataReader as fdr
# import pandas as pd
# import numpy as np
# from datetime import datetime, date, timedelta

# from sklearn.preprocessing import MinMaxScaler
# from sklearn.model_selection import train_test_split
# from keras.models import Sequential
# from keras.layers import GRU, Dense
# from sklearn.metrics import mean_squared_error

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import GRU, Dense
from sklearn.metrics import mean_squared_error

# 데이터 가져오기
train_start = '2016-01-01'
train_end = '2024-10-30'

# # 삼성전자 주가, KOSPI 주가, 환율 데이터 가져오기
# df_ss = fdr.DataReader('005930', train_start, train_end)  # 삼성전자 주가
# df_ks = fdr.DataReader('KS11', train_start, train_end)    # KOSPI 지수
# df_fx = fdr.DataReader('USD/KRW', train_start, train_end) # 환율 데이터

# yfinance로 삼성전자, KOSPI, 환율 데이터 가져오기
df_ss = yf.download("005930.KS", start=train_start, end=train_end)  # 삼성전자 주가
df_ks = yf.download("^KS11", start=train_start, end=train_end)      # KOSPI 지수
df_fx = yf.download("KRW=X", start=train_start, end=train_end)      # 환율 데이터

# 공통 날짜 기준으로 필터링
df_ss_common = df_ss[df_ss.index.isin(df_fx.index)]
df_ks_common = df_ks[df_ks.index.isin(df_fx.index)]
df_fx_common = df_fx[df_fx.index.isin(df_ss.index) & df_fx.index.isin(df_ks.index)]

# 결측치 확인
print("삼성전자 데이터 결측치 확인:", df_ss_common.isna().sum())
print("KOSPI 데이터 결측치 확인:", df_ks_common.isna().sum())
print("환율 데이터 결측치 확인:", df_fx_common.isna().sum())

# 'Close' 열만 선택하여 병합
ss_close = df_ss_common['Close'].values.reshape(-1, 1)  # 삼성전자 종가
ks_close = df_ks_common['Close'].values.reshape(-1, 1)  # KOSPI 종가
fx_close = df_fx_common['Close'].values.reshape(-1, 1)  # 환율 종가

# 데이터 정규화 (MinMaxScaler 사용)
scaler_ss = MinMaxScaler()
scaler_ks = MinMaxScaler()
scaler_fx = MinMaxScaler()
scaled_ss = scaler_ss.fit_transform(ss_close)
scaled_ks = scaler_ks.fit_transform(ks_close)
scaled_fx = scaler_fx.fit_transform(fx_close)

time_step = 15
epochs = 50
batch_size = 8

# 데이터를 병합 (삼성전자, KOSPI)
time_step = 10
combined_data = []

for i in range(len(scaled_ss) - time_step):
    combined_data.append(np.concatenate((scaled_ss[i:i+time_step], scaled_ks[i:i+time_step], scaled_fx[i:i+time_step]), axis=1))
combined_data = np.array(combined_data)

# 학습 및 테스트 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(combined_data[:, :-1], combined_data[:, -1], test_size=0.1, random_state=42)


# 모델 정의 (GRU Layers)
model = Sequential()
model.add(GRU(128, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(GRU(128, return_sequences=True))
model.add(GRU(128, return_sequences=False))
model.add(Dense(128))
model.add(Dense(1))

# 컴파일 (손실 함수 및 최적화 방법)
model.compile(optimizer='adam', loss='mean_squared_error')

# 모델 학습 (에폭과 배치 사이즈를 명시)
model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)

# 테스트 데이터에 대한 성능 평가
loss = model.evaluate(X_test, y_test)

# 예측할 날짜 범위 설정
prediction_results = []
predict_start = '2024-03-01'
end_date = datetime.today().strftime('%Y-%m-%d')
current_date = datetime.strptime(predict_start, '%Y-%m-%d')

while current_date <= datetime.strptime(end_date, '%Y-%m-%d'):
    ahead = current_date - timedelta(days=30)
    try:
        # yfinance를 사용하여 데이터 가져오기
        df_ss = yf.download("005930.KS", start=ahead, end=current_date)
        df_ks = yf.download("^KS11", start=ahead, end=current_date)
        df_fx = yf.download("KRW=X", start=ahead, end=current_date)

        # 공통 날짜 기준으로 필터링
        df_ss_common = df_ss[df_ss.index.isin(df_ks.index) & df_ss.index.isin(df_fx.index)]
        df_ks_common = df_ks[df_ks.index.isin(df_ss.index) & df_ks.index.isin(df_fx.index)]
        df_fx_common = df_fx[df_fx.index.isin(df_ss.index) & df_fx.index.isin(df_ks.index)]

        # 'Close' 열만 선택하여 병합
        ss_close = df_ss_common['Close'].values.reshape(-1, 1)
        ks_close = df_ks_common['Close'].values.reshape(-1, 1)
        fx_close = df_fx_common['Close'].values.reshape(-1, 1)

        # 데이터 정규화
        scaler_ss = MinMaxScaler()
        scaler_ks = MinMaxScaler()
        scaler_fx = MinMaxScaler()
        scaled_ss = scaler_ss.fit_transform(ss_close)
        scaled_ks = scaler_ks.fit_transform(ks_close)
        scaled_fx = scaler_fx.fit_transform(fx_close)

        # 예측에 사용할 데이터 생성
        combined_data = []
        for i in range(len(scaled_ss) - time_step):
            combined_data.append(np.concatenate((scaled_ss[i:i+time_step], scaled_ks[i:i+time_step], scaled_fx[i:i+time_step]), axis=1))
        combined_data = np.array(combined_data)

        # 예측 데이터 준비
        X_pred = combined_data[:, :-1]

        # 예측 수행 (모델 재학습 없음)
        predicted_data_scaled = model.predict(X_pred)
        predicted_data = scaler_ss.inverse_transform(predicted_data_scaled)
        prediction = predicted_data[-1][0]

        # 결과 저장 및 출력
        prediction_results.append((current_date, prediction))
        print(f'Prediction for {current_date.date()}: {prediction}')

    except ValueError as e:
        print(f"Skipping {current_date.date()}: {e}")
        pass

    current_date += timedelta(days=1)



model.summary()
print()
print(loss)
print()
print(prediction)

# prediction_results

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import FinanceDataReader as fdr

# 예측 결과를 데이터프레임으로 변환
df_prediction = pd.DataFrame(prediction_results, columns=['Date', 'Prediction'])

# 실제 삼성전자 주가 데이터를 가져와 공통된 날짜로 필터링
df_ss = fdr.DataReader('005930', predict_start, end_date)
df_ss_common = df_ss[df_ss.index.isin(df_prediction['Date'])]

# 예측 날짜와 실제 데이터 시각화
plt.figure(figsize=(10, 6))
plt.plot(df_ss_common.index, df_ss_common['Close'], label='SS Actual', color='blue')
plt.plot(df_prediction['Date'], df_prediction['Prediction'], label='Prediction', color='green', marker='o')

plt.xlabel('Date')
plt.ylabel('Price')
plt.title('SS Actual Prices vs. Predictions')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

print(len(df_ss_common.index))
print(len(df_ss_common['Close'].values))
print(len(df_prediction['Prediction'].values))

df_prediction_filtered = df_prediction[df_prediction['Date'].isin(df_ss_common.index)]

df_result = pd.DataFrame({
    'Date': df_ss_common.index,
    'Actual': df_ss_common['Close'].values,
    'Predicted': df_prediction_filtered['Prediction'].values
})

print(len(df_ss_common.index))
print(len(df_ss_common['Close'].values))
print(len(df_prediction['Prediction'].values))

# 공통된 인덱스 필터링
df_prediction_filtered = df_prediction[df_prediction['Date'].isin(df_ss_common.index)]
df_prediction_filtered = df_prediction_filtered.set_index('Date').reindex(df_ss_common.index).dropna()

print(len(df_ss_common.index))
print(len(df_prediction_filtered['Prediction'].values))

df_result = pd.DataFrame({
    'Date': df_ss_common.index,
    'Actual': df_ss_common['Close'].values,
    'Predicted': df_prediction_filtered['Prediction'].values
})

# 공통된 인덱스 필터링 및 재정렬
df_prediction_filtered = df_prediction[df_prediction['Date'].isin(df_ss_common.index)]
df_prediction_filtered = df_prediction_filtered.set_index('Date').reindex(df_ss_common.index).dropna()

print(len(df_ss_common.index))  # 확인
print(len(df_prediction_filtered['Prediction'].values))  # 확인

# 결과 데이터프레임 생성
df_result = pd.DataFrame({
    'Date': df_ss_common.index,
    'Actual': df_ss_common['Close'].values,
    'Predicted': df_prediction_filtered['Prediction'].values
})

# len(df_prediction), len(df_ss_common)

import pandas as pd
import numpy as np

# 날짜 인덱스 변환
df_ss_common.index = pd.to_datetime(df_ss_common.index)
df_prediction_filtered.index = pd.to_datetime(df_prediction_filtered.index)

# 결과 데이터프레임 생성
df_result = pd.DataFrame({
    'Date': df_ss_common.index,
    'Actual': df_ss_common['Close'].values,
    'Predicted': df_prediction_filtered['Prediction'].values
})

# Previous 열 생성 및 결측치 처리
df_result['Previous'] = df_result['Actual'].shift(1).fillna(0).astype(int)

# Predicted 값이 배열일 경우에 대한 처리
if isinstance(df_result['Predicted'].iloc[0], np.ndarray):
    df_result['Predicted'] = df_result['Predicted'].apply(lambda x: int(x[0]))
else:
    df_result['Predicted'] = df_result['Predicted'].astype(int)

# 차이 계산
df_result['Difference'] = df_result['Actual'] - df_result['Previous']
df_result['Difference'] = df_result['Difference'].fillna(0).apply(lambda x: int(x))

# Guess 및 Evaluate 열 생성
df_result['Guess'] = ''
df_result['Evaluate'] = ''

# 조건 적용 함수 정의
def apply_conditions(row):
    if row['Predicted'] > row['Previous']:
        row['Guess'] = 'Up'
        row['Evaluate'] = 'Good' if row['Difference'] >= 0 else 'Bad'
    elif row['Predicted'] == row['Previous']:
        row['Guess'] = '-'
        row['Evaluate'] = 'Good' if row['Difference'] == 0 else 'Bad'
    else:
        row['Guess'] = 'Down'
        row['Evaluate'] = 'Good' if row['Difference'] < 0 else 'Bad'
    return row

# Apply 함수 적용
df_result = df_result.apply(apply_conditions, axis=1)

# 첫 번째 행 제거 (필요한 경우)
df_result = df_result.drop(df_result.index[0])

# 결과 출력
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# 최종 결과 확인
print(df_result.tail(30))

# 정확도 계산
total = df_result.shape[0]
correct = df_result['Evaluate'].str.count("Good").sum()
accuracy = correct / total
print(f"{accuracy*100:.3f}%")

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# df_result

total = df_result.shape[0]
correct = df_result['Evaluate'].str.count("Good").sum()
accuracy = correct/total

print(f"{accuracy*100:.3f}%")

df_result.tail(30)