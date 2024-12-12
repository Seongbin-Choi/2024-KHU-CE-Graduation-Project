# 2024-KHU-CE-Graduation-Project
2024년 경희대학교 컴퓨터공학과 졸업프로젝트

요약 : 본 연구는 LSTM(Long Short-Term Memory)을 활용하여 환율 및 코스피 종합지수를 반영한 데이터 통합 모델을 통해 주가 예측의 정확도 개선 방안을 제안한다. 기존 연구는 단일 주가 데이터만을 학습하여 외부 요인의 영향을 반영하지 못하는 한계가 있었다. 
   본 연구에서는 코스피 지수와 환율(USD/KRW)을 추가 데이터로 통합하여 삼성전자의 주가 변동성을 예측하고, LSTM과 GRU(Gated Recurrent Unit) 모델의 성능을 비교 분석하였다. 
   연구 결과, 데이터 통합 스케일링 모델이 가장 높은 정확도를 기록하며 외부 요인의 중요성을 입증하였다. 이를 통해 주가 예측 모델의 실효성을 높이고, 금융 시장에서의 활용 가능성을 확대하는 데 기여하고자 한다.

1. LSTM 모델 구성

![image](https://github.com/user-attachments/assets/a892e2da-776a-4c2e-8290-d27477ad9125)

1.1. 환율 제거 옵션: KOSPI 종합지수와 삼성전자 주가 데이터만을 사용하여 예측을 수행하였다. 환율 데이터를 제외하여 외부 요인 없이 주가 데이터만으로 예측했을 때의 성능을 확인하였다.

1.2. 환율 포함 옵션: 환율(USD/KRW) 데이터를 포함하여 모델을 학습하였으며, 환율 변동이 주가 예측에 미치는 영향을 분석하였다. 환율 포함 여부에 따른 성능 차이를 비교하였다.


   ![image](https://github.com/user-attachments/assets/2556eb1c-c96f-41cd-a67a-a6062853b652)

1.3. GRU 모델 옵션: LSTM 대신 GRU(Gated Recurrent Unit) 모델을 사용하여 동일한 데이터로 주가 예측을 수행하였으며, LSTM과 GRU 모델 간의 성능 차이를 비교하였다.

1.4. 코스피와 환율 결합 인덱스 옵션: KOSPI 지수와 환율 데이터를 결합하여 하나의 설명 변수로 입력 데이터에 포함하였다. 이를 통해 결합된 변수의 효과가 개별 변수 사용 대비 주가 예측 성능에 미치는 영향을 평가하였다.

2. 모델 성능 평가
- 예측 결과 분석: 본 연구에서는 학습된 LSTM 및 GRU 모델을 사용하여 삼성전자 주가 예측 결과를 도출하고, 다양한 옵션별로 예측 성능을 비교하였다. 성능 평가는 RMSE(Root Mean Squared Error), MAE(Mean Absolute Error) 등의 회귀 모델 성능 지표와 함께 정확도(Accuracy)를 사용하였다.

   ![image](https://github.com/user-attachments/assets/2995a91d-3dec-406f-9d2a-1c11a98f8310)
- 환율 제거 vs. 환율 포함: 환율을 제거하여 KOSPI와 삼성전자 주가 데이터만을 사용하여 예측한 경우, 정확도는 45.963%로 나타났다. 이는 외부 경제 요인(환율)을 반영하지 못했기 때문에 성능이 저하된 결과이다. 환율 데이터를 포함하여 학습한 경우, 정확도는 46.835%로 나타나 환율 제거 모델보다 성능이 향상되었다. 이는 환율이 삼성전자와 같은 대형 기업 주가 변동에 중요한 영향을 미친다는 점을 시사한다.

   ![image](https://github.com/user-attachments/assets/5f7fad2e-5912-4ae5-a053-26781f7d5014)
- LSTM vs. GRU 모델: LSTM(Long Short-Term Memory) 모델과 GRU(Gated Recurrent Unit) 모델의 성능을 비교한 결과, GRU 모델은 정확도가 49.689%로 나타나 효율성과 성능 면에서 긍정적인 결과를 보였으나, LSTM 모델의 정확도(50%)에는 미치지 못했다. LSTM은 복잡한 시계열 데이터의 학습에 강점을 보여 최종 모델로 선택되었다.

- (accuracy를 향상한 데이터 통합 모델 그래프 업로드 예정)
- 데이터 통합 스케일링 모델: 본 연구에서 제안한 데이터 통합 스케일링 모델은 KOSPI, 환율 데이터를 통합한 후 정규화하여 외부 요인의 상호작용을 효과적으로 반영하였다. 이를 통해 정확도는 50%로 기존 모든 옵션 중 가장 높은 성능을 기록하였다. 데이터 통합 스케일링 과정은 각 변수 간 상관관계를 강화하고, 예측 정확도를 더욱 향상시킬 수 있음을 입증하였다.

3. 결론

 본 연구는 주가 예측의 정확도를 향상시키기 위해 LSTM(Long Short-Term Memory) 모델에 KOSPI 종합지수와 환율(USD/KRW)을 결합한 데이터를 적용하고, 다양한 실험 옵션을 통해 모델 성능을 비교하였다. 기존 연구들이 단일 주가 데이터에 의존했던 한계를 넘어, 외부 경제적 요인을 반영한 다변량 시계열 데이터 분석을 도입하여 보다 정교한 예측 결과를 도출하고자 하였다.
 연구 결과, 데이터 통합 스케일링 모델이 50%의 정확도를 기록하며 가장 높은 성능을 보였고, 최종 모델로 선정되었다. 이 모델은 KOSPI 지수와 환율 데이터를 정규화 및 결합하여 외부 요인의 상호작용을 효과적으로 반영하였으며, 기존 모델 대비 예측 정밀도를 크게 향상시켰다. 반면, 환율 데이터를 포함하지 않은 모델은 45.96%의 낮은 정확도를 기록하여, 외부 경제적 요인의 배제가 예측 성능을 제한한다는 점을 명확히 보여주었다.

 또한, LSTM과 GRU(Gated Recurrent Unit) 모델을 비교한 결과, GRU 모델이 간결한 구조로 학습 효율성을 제공했지만, 복잡한 시계열 데이터를 처리하는 데 있어 LSTM 모델이 더 우수한 성능을 나타냈다. 특히, 환율과 KOSPI 지수를 단일 변수로 결합한 옵션은 개별 변수의 상호작용을 정교하게 반영하는 데이터 통합 스케일링 접근법에 비해 낮은 성능을 보여, 변수 간 상호작용을 반영한 분석 기법의 중요성을 확인할 수 있었다.

 본 연구는 단일 주가 데이터에 의존하던 기존 모델과 비교하여 외부 경제 요인을 추가함으로써 예측 정확도를 개선할 수 있음을 입증하였다. 이로써 주가 예측 모델의 실효성을 높이는 데 기여하며, 금융 시장의 복잡성을 더 정교하게 반영할 수 있는 분석 도구를 제시하였다. 특히, KOSPI와 환율 데이터를 포함한 다변량 시계열 분석이 주가 변동성을 더 잘 예측할 수 있는 기반을 제공함을 보여주었다.

 추가적으로, 본 연구는 데이터 통합 과정에서의 스케일링 기법이 예측 정확도 향상에 미친 영향을 상세히 분석하였으며, 이를 통해 다양한 데이터 세트를 통합적으로 처리하여 학습시킬 경우 모델의 성능이 크게 개선될 수 있음을 실증적으로 확인하였다. 이러한 접근은 주가 예측뿐만 아니라 다른 시계열 데이터 분석에도 적용 가능한 범용성을 가지며, 경제적 요인의 복합성을 반영하는 데 중요한 기여를 한다.
