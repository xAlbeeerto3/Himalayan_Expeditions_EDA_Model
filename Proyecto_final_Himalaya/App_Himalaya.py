#---LIBRERÍAS EMPLEADAS---#
import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import plotly_express as px
import streamlit as st
import plotly as pt
from streamlit_folium import st_folium
import folium
from streamlit_folium import folium_static
from streamlit_option_menu import option_menu
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
import requests
import json

#---DISEÑO BÁSICO---#

# Nombre e icono de la web
st.set_page_config(page_title="Expedición al Himalaya",
        layout="wide",
        page_icon="⛰️")

# Eliminamos la barra superior
st.markdown(
    """
    <style>
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0);
    }
    </style>
    """,
    unsafe_allow_html=True)

# Estilos para el sidebar y contenido principal
st.markdown(
    f"""
    <style>
    .sidebar-content {{
        background-color: #008080 !important;
        padding: 10px !important;
        border: 1px solid #008080 !important;
        border-radius: 5px !important;
    }}
    </style>
    """,
    unsafe_allow_html=True)

# Sidebar para el menú principal
logos_expediciones = (r'Imagenes\logos_expediciones.png')
st.sidebar.image(logos_expediciones, width=250)
st.sidebar.header('Opciones', divider='rainbow')
st.sidebar.markdown(
    """
    <style>
    .sidebar-content {
        background-color: #000033 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Curiosidades para el sidebar
st.sidebar.markdown("## ⭐Curiosidades del Himalaya:⭐")
st.sidebar.markdown("⛰️ Himalaya sigue creciendo 2cm al año.")
st.sidebar.markdown("📆 Solo tiene 65 millones de años.")
st.sidebar.markdown("⛵ Ríos que nacen: Indo, Ganges y Yangtsé.")
st.sidebar.markdown("💀 A partir de 7.500m es Zona de Muerte.")


#---LECTURA---#
expeditions = pd.read_csv('himalayan_expeditions_copy.csv')
members = pd.read_csv('members_copy.csv')
peaks = pd.read_csv('peaks_copy.csv')
peaks_original = pd.read_csv('peaks.csv')
expeditions_original = pd.read_csv('expeditions.csv')

#---MENU PRINCIPAL---#
menu_principal = option_menu(None, ['📌 Introducción', "📈 Análisis Exploratorio", "🚧 Power BI", "🌐 Modelo", "🏆 Conclusión"], orientation="horizontal",
                             styles={"container": {"background-color": "#000033", "border-radius": "50px"},})

#---INTRODUCCION---#
if menu_principal == '📌 Introducción':
    
    url_imagen_fondo_introduccion = "https://static.vecteezy.com/system/resources/thumbnails/006/132/608/original/himalaya-mountain-with-star-in-night-time-video.jpg"

    def add_bg_from_url(url_imagen_fondo_dataframe):
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url({url_imagen_fondo_dataframe});
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
                </style>
                """,
                unsafe_allow_html=True)

    add_bg_from_url(url_imagen_fondo_introduccion)
    
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 70px; margin: 0; text-shadow: 6px 6px 6px #000000;'>🧭 Expedición al Himalaya: ¿Cuándo se hizo tan viral? 💬</h1></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 20px; font-size: 25px; background-color: rgba(255, 255, 255, 0.5); color: #ffffff; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Desde tiempos inmemoriales, el Himalaya ha fascinado a aventureros y exploradores, pero ¿cuándo se convirtió en un fenómeno global? A traves del siguiente análisis basado en un estudio de las expediciones, picos y sus miembros en el Himalaya desde 1905 hasta 2019. Responderemos a preguntas cómo: ¿Cuál fue la primera expedición en llegar a la cima del Everest?,  ¿Cual es el pico mas letal? o ¿Que promedio de miembros son necesarios para llevar a cabo una expedicion?, todo ello, con el objetivo de a traves de un modelo predictivo que veremos mas adelante, tratar de conocer la probabilidad de fallecer en una expedicion.</b><br>
        </div>
        """, unsafe_allow_html=True)
    
    
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 40px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Breve historia ⏳</h1></div>", unsafe_allow_html=True)
    colgif2, colnepal2 = st.columns(2)
    colgif1, colnepal1 = st.columns(2)
    
    with colgif1:
        gif_himalaya = ('https://i.pinimg.com/originals/2e/f9/70/2ef9703c4a2711fbb0df642b1ae67294.gif')
        st.image(gif_himalaya,width=1040)
    
    with colnepal1:
        nepalfoto1 = ('https://static.viajesanepal.com/uploads/2020/08/Escalar-un-pico-de-trekking-en-Nepal.jpg')
        st.image(nepalfoto1,width=1030)
        
    st.markdown("""<div style="margin-bottom: 40px;"></div>""", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 20px; font-size: 25px; background-color: rgba(255, 255, 255, 0.5); color: #ffffff; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>El Himalaya o Morada de la Nieve, es la cadena montañosa más alta del mundo y se extiende a lo largo de: India, Nepal, Bután, Birmania, China y Pakistán. Alberga las cumbres más altas del planeta, incluido el Everest, que con sus 8.848 metros sobre el nivel del mar, es el pico más alto de la Tierra. Las expediciones al Himalaya tienen una rica y fascinante historia que se remonta a siglos atrás. Las primeras exploraciones fueron realizadas por lugareños, como los sherpas y otros habitantes de las regiones montañosas, que conocían bien las rutas y peligros de la zona. Sin embargo, fue en el siglo XX cuando las expediciones occidentales comenzaron a explorar estas alturas en busca de aventura y descubrimiento.</b><br>
        </div>
        """, unsafe_allow_html=True)
    
    
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 40px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Nepal: El Corazón del Himalaya ⛰️</h1></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 20px; font-size: 25px; background-color: rgba(255, 255, 255, 0.5); color: #ffffff; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Nepal es conocido como el país de las montañas y es el epicentro de la mayoría de las expediciones al Himalaya. De hecho, no solo es hogar del Everest, sino también de otros siete de los catorce picos de más de 8.000 metros de altura.</b><br>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""<div style="margin-bottom: 60px;"></div>""", unsafe_allow_html=True)
    
    colnepal1, colgif2 = st.columns(2)
    
    with colnepal1:
        nepalfoto1 = ('https://static.viajesanepal.com/uploads/2020/08/Escalar-un-pico-de-trekking-en-Nepal.jpg')
        st.image(nepalfoto1,width=1030)
    
    with colgif2:
        gif_expedicion = ('https://i.pinimg.com/originals/d3/9a/a4/d39aa4a407af7f6f480bf4661ef6f63f.gif')
        st.image(gif_expedicion,width=1021)
    
    st.markdown("""<div style="margin-bottom: 60px;"></div>""", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 20px; font-size: 25px; background-color: rgba(255, 255, 255, 0.5); color: #ffffff; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>El gobierno nepali nos ha solicitado un analisis exhaustivo de los datos recogidos por las expediciones desde 1905 a 2019, para entender el impacto demografico y medioambiental que estan suponiendo para el pais y las montañas sagradas de las que se compone.</b><br>
        </div>
        """, unsafe_allow_html=True)

#---ANALISIS EXPLORATORIO---# 
#-EXPEDICION EDA-#
if menu_principal == '📈 Análisis Exploratorio':
    sidebar = st.sidebar.radio('Selecciona una opción:', ['Expedicion','Pico', 'Miembro'])
    
    if sidebar == 'Expedicion':
        
        url_imagen_fondo_eda = "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/0d/00/c7/64/himalayan-hikers-expedition.jpg?w=1200&h=1200&s=1"

        def add_bg_from_url(url_imagen_fondo_eda):
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url({url_imagen_fondo_eda});
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
                </style>
                """,
                unsafe_allow_html=True)

        add_bg_from_url(url_imagen_fondo_eda)
        
        st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 70px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Expediciones 🗺️</h1></div>", unsafe_allow_html=True)

        #---PREGUNTA PRIMERA---#
        st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 40px; margin: 0; text-shadow: 6px 6px 6px #000000;'>¿Cuál fue la primera expedición en llegar a la cima del Everest?</h1></div>", unsafe_allow_html=True)
        
        imagen7 = (r'Imagenes\imagen7.jpg')
        st.image(imagen7,use_column_width=True, width=600)
        
        imagen_consulta = (r'Imagenes\consulta.PNG')
        st.image(imagen_consulta,use_column_width=True)
        
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; font-size: 25px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>El 29 de mayo de 1953 son escaladores, Tenzing Norgay y  Edmund Hillary de 39 y 34 años respectivamente, lograban subir a la cima del mundo, el monte Everest de 8848 metros. </b><br>
        </div>
        """, unsafe_allow_html=True)

        #---PREGUNTA SEGUNDA---#
        st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 40px; margin: 0; text-shadow: 6px 6px 6px #000000;'>¿Cuál es la mejor estación del año para hacer una expedición? ¿Cuál es el pico con mayor expediciones en la temporada de otoño?</h1></div>", unsafe_allow_html=True)
        
        col3, col7 = st.columns(2)
        with col3:
            imagen_amadablam = (r'Imagenes\imagen3.png')
            st.image(imagen_amadablam,width=10, use_column_width=True)
        
        with col7:
            imagen3 = (r'Imagenes\grafica_picos_otoño.png')
            st.image(imagen3, width=1000)
        
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; font-size: 25px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>La mejor época para viajar a Nepal es desde octubre hasta febrero y en segundo lugar , de marzo a mayo. Estos períodos ofrecen la mejor temporada de trekking del Nepal. El pico Ama Dablam con 6812 m de altitud. Preferido por los escaladores pues el hielo que se desprende del glaciar, típicamente va hacia la izquierda, lejos del campamento. Los mejores meses son abril.mayo y septiembre-octubre.</b><br>
        </div>
        """, unsafe_allow_html=True)
        

        #---PREGUNTA TERCERA---#
            
        st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 40px; margin: 0; text-shadow: 6px 6px 6px #000000;'>¿Por qué hay ciertas expediciones que nunca terminaron?</h1></div>", unsafe_allow_html=True)
        col5, col6 = st.columns(2)
        with col5:
            imagen5 = (r'Imagenes\5_razones_abandono.png')
            st.image(imagen5,width=1070)
        with col6:
            imagen6 = (r'Imagenes\mal_tiempo.jpg')
            st.image(imagen6,width=1120) 
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; font-size: 25px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Diversos motivos son los que causan que una expedición  decida no continuar con la conquista de la cima. Los tres mas importantes son : 
            Mal tiempo, tormentas y fuertes vientos,   
            malas condiciones como , avalanchas o nieve profunda,   
            enfermedades, congelación de miembros y males de altura.  </b><br>
        </div>
        """, unsafe_allow_html=True)

        #---PREGUNTA CUARTA---#
        st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 40px; margin: 0; text-shadow: 6px 6px 6px #000000;'>¿Cuántas expediciones subieron con oxígeno?</h1></div>", unsafe_allow_html=True)
        col5, col6 = st.columns(2)
        with col5:
            imagen2 = (r'Imagenes\imagen2.png')
            st.image(imagen2,width=1000)
        
        with col6:
            imagen_oxigeno = (r'Imagenes\oxigeno.jpg')
            st.image(imagen_oxigeno,width=1200)
    
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; font-size: 25px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Subieron 2912 expediciones subieron con oxígeno, lo que quiere decir, como vemos en el gráfico que muchas más expediciones decidieron no utilizar bombonas de oxígeno para sus ascensiones.</b><br>
        </div>
        """, unsafe_allow_html=True)
    
        
        #---PREGUNTA QUINTA---#
        st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 40px; margin: 0; text-shadow: 6px 6px 6px #000000;'>¿Cuáles son las 50 expediciones con más miembros?</h1></div>", unsafe_allow_html=True)
        miembros_expediciones = (r'Imagenes\50miembros_expediciones.PNG')
        st.image(miembros_expediciones,use_column_width=True)
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; font-size: 25px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Las expediciones con más miembros son las siguientes: en 1988, la del Everest con 99 miembros; seguida por la de 2008, también al Everest, con 76 miembros; y finalmente, en 1987, la del pico Yalung Kang con 62 miembros.</b><br>
        </div>
        """, unsafe_allow_html=True)
        
        
    #-PICO EDA-#
    if sidebar == 'Pico':
        
        url_imagen_fondo_eda = "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/0d/00/c7/64/himalayan-hikers-expedition.jpg?w=1200&h=1200&s=1"

        def add_bg_from_url(url_imagen_fondo_eda):
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url({url_imagen_fondo_eda});
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
                </style>
                """,
                unsafe_allow_html=True)

        add_bg_from_url(url_imagen_fondo_eda)
        
        st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 70px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Picos ⛰️</h1></div>", unsafe_allow_html=True)
        
    #---PREGUNTA PRIMERA---#
        st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 40px; margin: 0; text-shadow: 6px 6px 6px #000000;'>¿Cuáles son los 8000 de la cordillera del Himalaya?</h1></div>", unsafe_allow_html=True)
    
        col1, col2 = st.columns(2)
    
        with col1:
    
            st.image('Imagenes/ochomil.png', caption= 'Fig3.Gráfico con los picos mayores de 8 mil metros')
    
        with col2:
    
                picos_8000 = {
                "Everest": [27.9881, 86.9250],
                "Kangchenjunga": [27.7025, 88.1475],
                "Lhotse": [27.9617, 86.9330],
                "Yalung Kang": [27.665, 88.120],
                "Makalu": [27.8897, 87.0883],
                "Kangchenjunga South": [27.6498, 88.1478],
                "Kangchenjunga Central": [27.6745, 88.144],
                "Lhotse Middle": [27.962, 86.930],
                "Lhotse Shar": [27.960, 86.940],
                "Cho Oyu": [28.0944, 86.6608],
                "Dhaulagiri I": [28.6967, 83.4875],
                "Manaslu": [28.5497, 84.5597],
                "Annapurna I": [28.5961, 83.8203],
                "Yalung Kang West": [27.7000, 88.1333], 
                "Annapurna I Middle": [28.5961, 83.8203],  
                "Annapurna I East": [28.5961, 83.8203],
                }
    
                mapa_himalaya = folium.Map(location=[28.22885, 85.37665], zoom_start=6.5, width=1200, height=560)
    
                for pico, coordenadas in picos_8000.items():
                    folium.Marker(
                        location=coordenadas,
                        popup=pico,
                        icon=folium.Icon(color='blue', icon='info-sign')
                    ).add_to(mapa_himalaya)
    
                st_folium(mapa_himalaya, width=1200, height=560)
    
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; font-size: 25px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Estos son los picos mas deseados por los alpinistas de todos los tiempos, en el  Himalaya no solo hay que sobrepasen la mítica altitud de 8000 metros sino que por debajo tenemos multitud de montañas por explorar, con vertientes vírgenes esperando ser pisadas.</b><br>
        </div>
        """, unsafe_allow_html=True)
        
        ##---PREGUNTA SEGUNDA---#
    
        st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 40px; margin: 0; text-shadow: 6px 6px 6px #000000;'>¿Hay más picos escalados que sin escalar?</h1></div>", unsafe_allow_html=True)
    
        col9, col10 = st.columns(2)
        with col9:
            climbed_vs_unclimbed = (r'Imagenes\grafico_climbed_unclimbed.png')
            st.image(climbed_vs_unclimbed,width=800)
            
        with col10:
            cima = (r'Imagenes\cima.jpg')
            st.image(cima,width=1060)
        
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; font-size: 25px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>En la actualidad, sigue hay mas escalados que sin escalar. Varios picos son los que todavía no han sido escalados, dada su  dificultad, por tragedias o incluso motivos religiosos,  destacando el monte Machhapurhre, un pico declarado en 1957 como monte sagrado por ser la morada del dios Shiba. Desde entonces no han sido permitidas las ascensiones.</b><br>
        </div>
        """, unsafe_allow_html=True)
    
    
        #---PREGUNTA TERCERA---#    
        st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 40px; margin: 0; text-shadow: 6px 6px 6px #000000;'>¿Cuáles son las nacionalidades con más primeras ascensiones? ¿Cuál fue el primer país en intentar llegar a la cumbre del Everest sin éxito?</h1></div>", unsafe_allow_html=True)
        colpaises1, colpaises2 = st.columns(2)
        with colpaises1:
            primeras_ascensiones = (r'Imagenes\japon_nepal_primeras.jpg')
            st.image(primeras_ascensiones, width=1000)
        
        with colpaises2:
            st.markdown("""<div style="margin-bottom: 200px;"></div>""", unsafe_allow_html=True)     
            st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; font-size: 25px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Las primeras naciones con mayor numero de primeras ascensiones son: Nepal y Japon. Los primeros en ascender sin exito el Everest fueron británicos, en la primavera de 1921, una primera ascensión de exploración y reconocimiento como principales objetivos. En aquella época Nepal estaba totalmente cerrado a los extranjeros por los que debían ganarse el permiso del Dalai Lama para realizar cualquier tipo de ascenso.</b><br>
        </div>
        """, unsafe_allow_html=True)
    
    
        #---PREGUNTA CUARTA---#
    
        st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 40px; margin: 0; text-shadow: 6px 6px 6px #000000;'>¿Cuál es el pico mas letal?</h1></div>", unsafe_allow_html=True)
        col12, col13 = st.columns(2)
        with col12:
            imagen_letal = (r'Imagenes\picos_letales.png')
            st.image(imagen_letal,width=1070)
    
        with col13:
            coordenadas_picos_mas_letales = {
            "Everest": [27.9881, 86.9250],
            "Annapurna I": [28.5961, 83.8203],
            "Manaslu": [28.5497, 84.5597],
            "Lhotse": [27.9617, 86.9330],
            "Ama Dablam": [27.8616, 86.8615]
            }
    
            letal_himalaya = folium.Map(location=[28.22885, 85.37665], zoom_start=6.5, width=900, height=450)
    
            for pico, coordenadas in coordenadas_picos_mas_letales.items():
                folium.Marker(
                    location=coordenadas,
                    popup=pico,
                    icon=folium.Icon(color='blue', icon='info-sign')
                ).add_to(letal_himalaya)
    
            st_folium(letal_himalaya, width=900, height=450)
    
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; font-size: 25px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>El monte Everest con sus más de 300 fallecidos por accidente se encuentra en la primera posición de este letal ranking.</b><br>
        </div>
        """, unsafe_allow_html=True)
        
        #-MIEMBRO EDA-#
    if sidebar == 'Miembro':
        
        url_imagen_fondo_eda = "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/0d/00/c7/64/himalayan-hikers-expedition.jpg?w=1200&h=1200&s=1"

        def add_bg_from_url(url_imagen_fondo_eda):
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url({url_imagen_fondo_eda});
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
                </style>
                """,
                unsafe_allow_html=True)

        add_bg_from_url(url_imagen_fondo_eda)
        
        st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 70px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Miembros 🧗</h1></div>", unsafe_allow_html=True)
        
    #---PREGUNTA PRIMERA---#
        st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 40px; margin: 0; text-shadow: 6px 6px 6px #000000;'>¿Cuál ha sido el suceso más grave en la cordillera del Himalaya por españoles?</h1></div>", unsafe_allow_html=True)
        imagen6 = (r'Imagenes\imagen6.PNG')
        st.image(imagen6,use_column_width=True)
        
        españoles_fallecidos = (r'Imagenes\5españoles_fallecidos.PNG')
        st.image(españoles_fallecidos,use_column_width=True)
        
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; font-size: 25px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>El 16 de octubre de 2001, cinco escaladores, los navarros Aritz Artieda, Javier Arkauz y César Nieto y los guipuzcoanos Beñat Arrue e Iñaki Ayerza, murieron al se aplastados por un alud en el monte Pumori(7161 metros) en Nepal</b><br>
        </div>
        """, unsafe_allow_html=True)
        
    #---PREGUNTA SEGUNDA---#
        st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 40px; margin: 0; text-shadow: 6px 6px 6px #000000;'>¿Cuántos miembros de las expediciones fueron afectados a lo largo de los años?</h1></div>", unsafe_allow_html=True)
        
        miembros_fallecidos = (r'Imagenes\miembros_afectados.png')
        st.image(miembros_fallecidos,use_column_width=True)
            
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; font-size: 25px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>A partir de 1983, el número de heridos superó al número de fallecidos en expediciones, lo que significa que las medidas de seguridad han ido evolucionando y por tanto las expediciones son mas seguras.</b><br>
        </div>
        """, unsafe_allow_html=True)
        
    #---PREGUNTA TERCERA---#
        st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 40px; margin: 0; text-shadow: 6px 6px 6px #000000;'>¿Qué roles son más habituales en una expedicion?</h1></div>", unsafe_allow_html=True)
        
        col18, col19 = st.columns(2)
        with col18:
            imagen5 = (r'Imagenes\roles_expediciones.png')
            st.image(imagen5,width=1000)
        
        with col19:
            st.markdown("""<div style="margin-bottom: 300px;"></div>""", unsafe_allow_html=True)  
            st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; font-size: 25px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Los roles más habituales son: Escaladores, Sherpas, líder de la expedición, Sirdar(líder sherpas) y médico de la expedición entre otros.</b><br>
        </div>
        """, unsafe_allow_html=True)
        
    #---PREGUNTA CUARTA---#
        st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 40px; margin: 0; text-shadow: 6px 6px 6px #000000;'>De los alpinistas del Himalaya, ¿Cuántos escalaron solos y cuantos acompañados?</h1></div>", unsafe_allow_html=True)
        
        solos_fallecidos = members[(members['solo']=='Yes') & (members['died']=='Yes')].value_counts().sum()
        acompañados_fallecidos = members[(members['solo']=='No') & (members['died']=='Yes')].value_counts().sum()
        total_miembros = members.value_counts().sum()
        porcentaje_miembros_solos = (solos_fallecidos/total_miembros)*100
        porcentaje_miembros_solos.round(4)
        porcentaje_miembros_acompañados = (acompañados_fallecidos/total_miembros)*100
        porcentaje_miembros_acompañados.round(4)
        
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; font-size: 25px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Un total de 121 personas subieron solas y 76398 subieron acompañadas y como dato peculiar, de los que subieron solos fallecieron 5  y de los que subieron acompañados fallecieron un total de 1101 personas.</b><br>
        </div>
        """, unsafe_allow_html=True)
        
    #---PREGUNTA QUINTA---#
        st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 40px; margin: 0; text-shadow: 6px 6px 6px #000000;'>¿Cuántas mujeres realizaron expediciones? ¿Cuál fue la primera en subir a Everest?</h1></div>", unsafe_allow_html=True)
        
        col20, col21 = st.columns(2)
        with col20:
            st.markdown("""<div style="margin-bottom: 200px;"></div>""", unsafe_allow_html=True)
            primera_mujer = members[(members['sex']=='F') & (members['success']=='Yes') & (members['year']==1975) & (members['peak_name']=='Everest')].iloc[:-1]
            primera_mujer
        
        with col21:
            primera_mujer_everest = (r'Imagenes\primera_mujer_everest.PNG')
            st.image(primera_mujer_everest,width=1000)        
        st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 10px; font-size: 25px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>El numero de mujeres que hicieron cima fue 2306. Junko Tabei, la primera mujer en coronar el Everest, demostró que una mujer podía alcanzar las mismas metas que un hombre, algo inconcebible en la sociedad de su tiempo. El 6 de mayo de 1975, todos los estereotipos quedaron pulverizados cuando Tabei coronó el monte Everest acompañada del Sherpa Angustias Tsering.</b><br>
        </div>
        """, unsafe_allow_html=True)
        
        
    #---POWER BI---#

if menu_principal == '🚧 Power BI':
    
    url_imagen_fondo_power_bi = "https://e00-elmundo.uecdn.es/assets/multimedia/imagenes/2024/05/24/17165405040305.jpg"

    def add_bg_from_url(url_imagen_fondo_power_bi):
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url({url_imagen_fondo_power_bi});
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
                </style>
                """,
                unsafe_allow_html=True)

    add_bg_from_url(url_imagen_fondo_power_bi)
        
    power_bi_html = '''<iframe title="Himalayan_Expedition" width="1920" height="1080" src="https://app.powerbi.com/view?r=eyJrIjoiMGIzZjY1MzMtZDdmZC00YTFiLTg0YjUtOWRlZjk5YWNkMDJiIiwidCI6IjhhZWJkZGI2LTM0MTgtNDNhMS1hMjU1LWI5NjQxODZlY2M2NCIsImMiOjl9" frameborder="0" allowFullScreen="true"></iframe>'''
    
    # Mostramos el iframe en Streamlit usando html
    st.components.v1.html(power_bi_html, width=1920, height=1080)
        
    #---MODELO---#

if menu_principal == '🌐 Modelo':
    
    url_imagen_fondo_introduccion = "https://static.vecteezy.com/system/resources/thumbnails/006/132/608/original/himalaya-mountain-with-star-in-night-time-video.jpg"

    def add_bg_from_url(url_imagen_fondo_dataframe):
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url({url_imagen_fondo_dataframe});
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
                </style>
                """,
                unsafe_allow_html=True)

    add_bg_from_url(url_imagen_fondo_introduccion)
    

    # Creamos una funcion para la prediccion
    def prediccion(input_data):
        url = 'https://machinelearningupgrade-dvmkp.eastus2.inference.ml.azure.com/score'
        api_key = '95TjJl1q2AAgec80MOkm7jhbgIMKiFJ8'

        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'himalayanexp6-1' }

        try:
            response = requests.post(url, json=input_data, headers=headers)
            if response.status_code == 200:
                result = response.json()
                st.write(result)
            else:
                st.error("Request failed with status code: {}".format(response.status_code))
                st.error(response.text)
        except Exception as e:
            st.error("Error making request: {}".format(str(e)))

    # Creamos el formulario
    def main():
        st.title('Modelo de predicción de mortalidad')

        peak_options = ['Everest', 'Annapurna II', 'Makalu', 'Ama Dablam', 'Cho Oyu', 'Manaslu', 'Lhotse', 'Kangchenjunga', 'Yalung Kang', 'Dhaulagiri I', 'Annapurna I Middle']
        season_options = ['Spring', 'Autumn', 'Summer', 'Winter']
        oxygen_options = ['Yes', 'No']

        peak_name = st.selectbox('Selecciona Pico:', peak_options)
        year = st.number_input('Introduce Año:', value=2019)
        season = st.selectbox('Selecciona Temporada:', season_options)
        members = st.number_input('Introduce numero de expedicionistas:', value=5)
        oxygen_used = st.selectbox('Oxigeno Usado:', oxygen_options)

        if st.button('Predict'):
            season_mapping = {'Spring': 0, 'Autumn': 1, 'Summer': 2, 'Winter': 3}
            oxygen_used_numeric = 1 if oxygen_used == 'Yes' else 0

            input_data = {
                "input_data": {
                    "columns": ['Column2', "year", "members", "oxygen_used", "season", 'peak_name'],
                    "index": [0],
                    "data": [[0, year, members, oxygen_used_numeric, season_mapping[season], peak_name]]
                }
            }

            prediccion(input_data)

    if __name__ == '__main__':
        main()

        
    #---CONCLUSION---#
if menu_principal == '🏆 Conclusión':
    
    url_imagen_fondo_conclusion = ("https://imagenes.20minutos.es/files/image_1920_1080/uploads/imagenes/2023/08/11/europapress-5032695-himalaya.jpeg")

    def add_bg_from_url(url_imagen_fondo_conclusion):
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url({url_imagen_fondo_conclusion});
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
                </style>
                """,
                unsafe_allow_html=True)

    add_bg_from_url(url_imagen_fondo_conclusion)
    
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 70px; margin: 0; text-shadow: 6px 6px 6px #000000;'>La comercialización de las expediciones al Himalaya 💱</h1></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 20px; font-size: 25px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Después de analizar detalladamente los datos a lo largo de nuestro estudio, se ha evidenciado que escalar los ochomiles del Himalaya, y en concreto el Everest, se ha convertido en un negocio lucrativo. Muchas expediciones 'comerciales' no tienen en cuenta el nivel de experiencia de los escaladores, llevando a personas poco preparadas hasta la cima sin evaluar posibles consecuencias. Como mencionamos anteriormente, las temporadas de escalada son breves, limitando los días al año la posibilidad de ascender a la cima, cuando las condiciones meteorológicas son favorables y no hay vientos fuertes y tormentas.</b><br>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 40px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Masificacion y sus consecuencias medioambientales ♻️</h1></div>", unsafe_allow_html=True)
    
    personas_everest_gif = (r'Imagenes\videoagif.gif')
    basura_en_everest = (r'Imagenes\basura_en_everest.jpg')
    
    colconclusion3, colconclusion4 = st.columns(2)
    with colconclusion3:
        st.image(personas_everest_gif,width=1010)
    
    with colconclusion4:
        st.image(basura_en_everest,width=1000)
        
    st.markdown("""<div style="margin-bottom: 30px;"></div>""", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 20px; font-size: 25px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>El 22 de mayo de 2019 se hicieron virales estas imágenes como el día más concurrido de la historia del Everest: más de 200 personas pasaron por la cima. Por ello, el gobierno nepalí ha introducido normas para evitar muertes no accidentales y reducir los graves efectos medioambientales, obligando a ir con un sherpa o guía nativo, presentar certificados médicos y demostrar que han escalado antes un pico de 6500 metros (como mínimo). Alrededor de 800 personas escalan cada año la montaña más alta del mundo, incluyendo sherpas. Estas expediciones dejan a su paso botellas de oxígeno vacías, latas de comida y residuos humanos que se han ido acumulando durante décadas. De hecho, en 2019 se llevó a cabo una campaña de recogida que recuperó más de 10 toneladas de residuos y 4 cadáveres abandonados en la montaña. La presencia de cadáveres en los picos del Himalaya presenta un debate ético, moral y cultural. Por un lado, moverlos supondría un riesgo para los rescatistas y alpinistas, y por otro, el daño a la calidad del agua y el suelo por ser un entorno de descomposición lenta.</b><br>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 40px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Conclusion final 🏁</h1></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: left; border: 1px solid #000000; padding: 20px; font-size: 25px; background-color: rgba(255, 255, 255, 0.5); color: #000000; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5); border-radius: 10px;">
            <b>Este estudio nos ha permitido entender que, además de ser una aventura y proeza deportiva hacer expediciones a los picos más altos del mundo, también es un negocio. Mientras la cordillera del Himalaya siga siendo un símbolo de desafío, también será un lugar de problemas éticos, medioambientales y comerciales que deben ser gestionados por los gobiernos de los países involucrados para preservar su respeto sagrado.</b><br>
        </div>
        """, unsafe_allow_html=True)
    
    gif_formacion_himalaya = ('https://j.gifs.com/yg1oRe.gif')
    logo_nepal = ('https://www.shutterstock.com/shutterstock/videos/1069631479/thumb/1.jpg?ip=x480')
    
    st.markdown("""<div style="margin-bottom: 30px;"></div>""", unsafe_allow_html=True)
    
    colconclusion5, colconclusion6 = st.columns(2)
    
    with colconclusion5:
        st.image(gif_formacion_himalaya,width=1000)
    
    with colconclusion6:
        st.image(logo_nepal,width=1000)