# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 15:58:18 2026

@author: BusRmutt
"""

import pickle
from streamlit_option_menu import option_menu
import streamlit as st

used_car_model = pickle.load(open('Used_cars_model.sav','rb'))
riding_model = pickle.load(open('RidingMowers_model.sav','rb'))
bmi_model = pickle.load(open('bmi_model.sav','rb'))


fuel_map = {
    'Diesel': 0,
    'Electric': 1,
    'Petrol': 2
}

engine_map = {
    '800': 0,
    '1000': 1,
    '1200': 2,
   '1500': 3,
    '1800': 4,
    '2000': 5,
    '2500': 6,
    '3000': 7,
    '4000': 8,
    '5000': 9
}

brand_map = {
    'BMW': 0,
    'Chevrolet': 1,
    'Ford': 2,
    'Honda': 3,
    'Hyundai': 4,
    'Kia': 5,
    'Nissan': 6,
    'Tesla': 7,
    'Toyota': 8,
    'Volkswagen': 9
}

transmission_map = {
    'Automatic': 0,
    'Manual': 1
}
with st.sidebar:
    selected = option_menu('Prediction',
                           ['Ridingmower','Used_cars','BMI'])

if selected== 'Ridingmower':
    st.title('Riding Mower Classification')
    
    Income = st.text_input('Income')
    LotSize = st.text_input('LotSize')
    Riding_prediction = ''
    if st.button('Predict'):
        Riding_prediction = riding_model.predict([[
            float(Income),
            float(LotSize)
            ]])
        if Riding_prediction[0]==1:
            Riding_prediction = 'Owner'
        else:
            Riding_prediction = 'Non Owner'
    st.success(Riding_prediction)
    
if selected == 'Used_cars':
    st.title('ประเมินราคารถมือ 2')
    make_year = st.text_input('ปีที่ผลิต')
    mileage_kmpl = st.text_input('กินน้ำมันกี่ KM/L')
    engine_cc = st.selectbox('ขนาดเครื่องยนต์ (CC)', engine_map)
    fuel_type = st.selectbox('ประเภทน้ำมัน', fuel_map)
    owner_count = st.text_input('จำนวนเจ้าของเดิม')
    brand = st.selectbox('ยี่ห้อรถ', brand_map)
    transmission = st.selectbox('ประเภทเกียร์', transmission_map)
    accidents_reported = st.text_input('จำนวนอุบัติเหตุที่เคยเกิด')
    Price_predict = ''
    if st.button('Predict'):
        Price_predict = used_car_model.predict([[
            float(make_year),
            float(mileage_kmpl),
            engine_map[engine_cc],
            fuel_map[fuel_type],
            float(owner_count),
            brand_map[brand],
            transmission_map[transmission],
            float(accidents_reported)
            ]])
        Price_predict = round(Price_predict[0],2)

    st.success(Price_predict)

import streamlit as st

# สมมติว่าตัวแปร selected และ bmi_model ถูกกำหนดไว้แล้วก่อนหน้านี้
if selected == 'BMI':
    st.title('BMI Classification')
    
    # 1. รับค่าเพศเป็นข้อความ แล้วค่อยแปลงเป็นตัวเลขเบื้องหลัง
    # หมายเหตุ: ลองเช็คดูนะครับว่าตอนเทรนโมเดลคุณให้ Male=0 หรือ Male=1 โค้ดนี้สมมติให้ Male=0 ครับ
    gender_input = st.selectbox('Gender', ['Male', 'Female'])
    gender_val = 0 if gender_input == 'Male' else 1 
    
    # 2. รับค่าส่วนสูง (ซม.) และน้ำหนัก (กก.)
    height = st.number_input('Height (cm)', min_value=0)
    weight = st.number_input('Weight (kg)', min_value=0.0, format="%.1f")
    
    # ดิกชันนารีสำหรับแปลผลลัพธ์ Index
    bmi_categories = {
        0: "Extremely Weak (ผอมมาก)",
        1: "Weak (ผอม)",
        2: "Normal (เกณฑ์ปกติ)",
        3: "Overweight (น้ำหนักเกิน)",
        4: "Obesity (โรคอ้วน)",
        5: "Extreme Obesity (โรคอ้วนขั้นรุนแรง)"
    }
    
    if st.button('Predict'):
        if height > 0 and weight > 0:
            try:
                # ส่งค่าไปให้โมเดลทำนาย (เพศ, ส่วนสูง, น้ำหนัก)
                prediction = bmi_model.predict([[
                    float(gender_val),
                    float(height),
                    float(weight)
                ]])
                
                # ดึงค่า Index ออกมา และแปลงเป็นจำนวนเต็ม (integer)
                index_result = int(prediction[0])
                
                # ดึงข้อความแปลผลจากดิกชันนารี
                category_text = bmi_categories.get(index_result, "ไม่ทราบค่าการแปลผล")
                
                # แสดงผลลัพธ์แบบสวยงาม
                st.success(f'ดัชนีผลลัพธ์ (Index): {index_result}')
                st.info(f'**ผลการประเมิน:** {category_text}')
                
            except Exception as e:
                st.error(f'เกิดข้อผิดพลาดในการประมวลผล: {e}')
        else:
            st.warning('กรุณากรอกส่วนสูงและน้ำหนักให้มากกว่า 0')
       


