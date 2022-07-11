import serial
import streamlit as st
import plotly.graph_objects as go
import time
import numpy as np

arduino = serial.Serial(port='/dev/ttyACM1', baudrate=9600, parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS) #Change COM3 to whichever COM port your arduino is in

st.sidebar.title('Radar')
info_bar = st.empty()
info = st.empty()
radar_placeholder = st.empty()

r = [0]*180
theta = np.arange(0, 361, step=2)

def radar_gauge(rng1, rng2, pos, placeholder):
    fig = go.Figure()
    r[pos//2] = rng1
    r[((pos+180)%360)//2] = rng2

    fig.add_trace(go.Scatterpolar(
          r=r,
          theta=theta,
          line_color = 'cornflowerblue'
    ))

    r_needle = [0]*180
    r_needle[pos//2] = 1500
    r_needle[((pos+180)%360)//2] = 1500
    fig.add_trace(go.Scatterpolar(
          r=r_needle,
          theta=theta,
          line_color = 'firebrick'
    ))

    fig.update_layout(
      polar=dict(
        radialaxis=dict(
          visible=True,
          range=[0, 1500]
        ),
      ),
      showlegend=False
    )
    placeholder.write(fig)

if st.sidebar.button('Start reading data'):
    info_bar.info('Radar running')

    try:
        arduino.open()
    except:
        pass

    if st.sidebar.button('Stop reading data'):
        info_bar.warning('Radar stopped')
        try:
            arduino.close()
        except:
            pass

    while True:
        arduino.flushInput()
        arduino.flushOutput()
        arduino.flush()
        try:
            line = arduino.readline().decode().strip('\r\n').split('*')
            pos = int(line[0])
            rng1 = int(line[1])
            rng2 = int(line[2])
            print(f'Position: {pos}, range: {rng1}, {rng2}')
        except:
            pos = theta[0]
            rng1 = 0
            rng2 = 0
        # pos = arduino.readline().decode().strip('\r\n').split('*')[0]
        info.info(f'Position: **{pos}**°, Ranges: **{rng1}** mm, **{rng2}** mm')
        radar_gauge(rng1, rng2, pos, radar_placeholder)
        time.sleep(0.05)

try:
    arduino.close()
except:
    pass