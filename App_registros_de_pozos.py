# Librerias a importar
import streamlit as st 
import pandas as pd 
import lasio
import altair as alt
import matplotlib.pyplot as plt
from PIL import Image
from io import StringIO
#Nombre de la aplicación
st.title("Registro de pozos")
# Archivos a importar
archivo_las = lasio.read("Archivos_las\LGAE-040.las")
df = archivo_las.df()
inicio = Image.open("Inicio.jpg")
# Menú de la aplicación
menu = st.sidebar.radio("Seleccione una opcion del aplicativo", ("🏠 Inicio","📈 Análisis rápido", "📊 Evaluacion de zonas de pago"))
#Opciones de menu
if menu == "🏠 Inicio":
    st.image(inicio)
    st.write("""
        # Descripción del aplicativo
        El objetivo de este aplicativo es realizar un analisis breve de la información del registro de pozo
        y poder visualizar la data y graficarla, ademas incluir un **algoritmo para el análisis de zonas de pago**
        en base a las teorias y fórmulas bibliográficas

        Previamente se debe tener conocimientos generales para interpretar registros de pozos
        - La experiencia en campo
        - Conocimientos de programacion

        Dos aspectos que permitiran mejorar continuamente este aplicativo, pero el objetivo es dar  herramienta en este primer modulo

        """)


    st.write(""" 


        instrucciones

        1-

        2-

        
        3






        """)
if menu == "📈 Análisis rápido":
    cargar_data = st.selectbox("Escoja un método",("Data demo","Cargar archivo LAS"), index = 1)
    if cargar_data == "Data demo":
        st.header("Data Frame")
        st.write(df)
        st.header("Lectura del registro")
        profundidad_min = df.index.values[0]
        profundidad_max = df.index.values[-1]
        st.write("Este registro fue medido desde una profundidad de :", profundidad_min , "[ft]")
        st.write("Este registro fue medido hasta una profundidad de :", profundidad_max , "[ft]" ) 
        st.title("Limpieza y selección de datos ")
        selected_columns = ['NPHI','RHOB','GR']
        df_shorter = df[selected_columns]
        df_clean = df_shorter.dropna(subset=['NPHI','RHOB','GR'],axis=0, how='any')
        st.header("DataFrame sin valores nulos")
        st.write(df_clean)
        st.header("Grafico Data Frame Clean")
        f, ax = plt.subplots(nrows=1, ncols=3, figsize=(12,8) )
        logs = ['NPHI','RHOB','GR']
        colors = ['green','blue','red']
        for i,log,color in zip(range(3),logs,colors):
            ax[i].plot(df_clean[log], df_clean.index, color=color)
            ax[i].invert_yaxis()
        for i,log,color in zip(range(3),logs,colors):
            ax[i].set_xlabel(log)
            ax[0].set_ylabel("Depth(ft)")
            ax[i].grid()
        st.pyplot(f)
        
    if cargar_data == "Cargar archivo LAS":
        archivo_cargado = st.file_uploader("Cargar archivo LAS" , key=None)
        
        if archivo_cargado is None:
            st.write("Suba un archivo con extencion .las")

        if archivo_cargado is not None:
            bytes_data = archivo_cargado.read()
            str_io = StringIO(bytes_data.decode('Windows-1252'))
            las_file = lasio.read(str_io)
            df_upload = las_file.df()
            df_upload['DEPTH'] = df_upload.index
            st.header("Data Frame")
            st.write(df_upload)
            st.header("Lectura del registro")
            profundidad_min = df_upload.index.values[0]
            profundidad_max = df_upload.index.values[-1]
            st.write("Este registro fue medido desde una profundidad de :", profundidad_min , "[ft]")
            st.write("Este registro fue medido hasta una profundidad de :", profundidad_max , "[ft]" ) 
            st.header("Limpieza y selección de datos ")
            selected_columns = ['NPHI','RHOB','GR']
            df_shorter = df_upload[selected_columns]
            df_clean = df_shorter.dropna(subset=['NPHI','RHOB','GR'],axis=0, how='any')
            st.header("DataFrame sin valores nulos")
            st.write(df_clean)
            f, ax = plt.subplots(nrows=1, ncols=3, figsize=(12,8) )
            logs = ['NPHI','RHOB','GR']
            colors = ['green','blue','red']
            for i,log,color in zip(range(3),logs,colors):
                ax[i].plot(df_clean[log], df_clean.index, color=color)
                ax[i].invert_yaxis()
            for i,log,color in zip(range(3),logs,colors):
                ax[i].set_xlabel(log)
                ax[0].set_ylabel("Depth(ft)")
                ax[i].grid()
            st.pyplot(f)


if menu == "📊 Evaluacion de zonas de pago":
    st.header("Lectura del registro")
    profundidad_min = df.index.values[0]
    profundidad_max = df.index.values[-1]
    st.write("Este registro fue medido desde una profundidad de :", profundidad_min , "[ft]")
    st.write("Este registro fue medido hasta una profundidad de :", profundidad_max , "[ft]" ) 
    st.header("Limpieza y selección de datos ")
    selected_columns = ['NPHI','RHOB','GR']
    df_shorter = df[selected_columns]
    df_clean = df_shorter.dropna(subset=['NPHI','RHOB','GR'],axis=0, how='any')
    df_clean


    f, ax = plt.subplots(nrows=1, ncols=2, figsize=(12,8) )
    logs = ['NPHI','RHOB']
    colors = ['green','blue']
    for i,log,color in zip(range(2),logs,colors):
        ax[i].plot(df_clean[log], df_clean.index, color=color)
        ax[i].invert_yaxis()
    for i,log,color in zip(range(3),logs,colors):
        ax[i].set_xlabel(log)
        ax[0].set_ylabel("Depth(ft)")
        ax[i].grid()
    st.pyplot(f)

    st.title("Evaluación del Registro")

    limite_superior = st.slider("Seleccione el limte superior de la formacion a analizar", int(profundidad_min) , int(profundidad_max) )
    limite_inferior = st.slider("Seleccione el limte inferior de la formacion a analizar", int(profundidad_min) , int(profundidad_max)  )
    df_limites=df[limite_superior:limite_inferior]
    
    st.header("Data Frame de la zona a evaluar")

    st.write(df_limites)
    seleccionar_columnas = ['NPHI','DT','RHOB','GR','SP','RT']
    st.header("Registros necesarios para la evaluación")
    df_filtrado = df_limites[seleccionar_columnas ]
    st.write(df_filtrado)

    f_filtrado, ax = plt.subplots(nrows=1, ncols=6, figsize=(16,10))
    logs = ['NPHI','DT','RHOB','GR','SP','RT']
    colors = ['green','orange','blue','red','black','brown']
    for i,log,color in zip(range(6),logs,colors):
        ax[i].plot(df_filtrado[log], df_filtrado.index, color=color)
        ax[i].invert_yaxis()
        
    for i,log,color in zip(range(6),logs,colors):
        ax[i].set_xlabel(log)
        ax[0].set_ylabel("Depth(ft)")
        ax[i].grid()
    st.pyplot(f_filtrado)


    st.header("Parametros para evaluacion")
    st.header("Analisis del GR")
    valor_minimo = df_filtrado["GR"].min()
    valor_maximo = df_filtrado["GR"].max()
    st.write("El valor minimo del GR:",valor_minimo)
    st.write("El valor maximo del GR:",valor_maximo)

    
    #Calculos Indice de Gamma Ray
    df_filtrado["IGR"]=(df_filtrado.GR-valor_minimo)/(valor_maximo-valor_minimo)
    #Calculo Vsh
    df_filtrado["Vsh"]=0.33*(2**(2*df_filtrado.IGR)-1)
    #Calculo Sonico
    

    delta_matriz=55.5
    delta_fluido=189
    st.write("Δmatriz:",delta_matriz)
    st.write("Δfluido:",delta_fluido)

    df_filtrado["PSonico"]=(df_filtrado.DT-delta_matriz)/(delta_fluido-delta_matriz)
    
    #Calculo densidad
    densidad_matriz=2.65
    densidad_fluido=1
    st.write("Densidad de la matriz:", densidad_matriz)
    st.write("Densidad del fluido:", densidad_fluido)

    df_filtrado["Pdensidad"]=(densidad_matriz-df_filtrado.RHOB)/(densidad_matriz-densidad_fluido)
    

    #Calculo porosidad total 
    df_filtrado["PT"]=((df_filtrado.NPHI+df_filtrado.Pdensidad)/2)
    
    #Calculo de gradiente de temperatura 
    Tf=200
    Pm=10370
    Ts=60
    st.write("Temperatura de la formacion:",Tf)
    st.write("Temperatura de superficie:",Tf)
    st.write("Presion del lodo:",Pm)

    df_filtrado["Gt"]=(Tf-Ts)*100/Pm


    #Calculo de temperatura de formacion  
    df_filtrado["TF"]=(Ts+df_filtrado.Gt*(df_filtrado.index/100))


    #Calculo de la resistividad de lodo en formacion 
    Rms=1.17
    Tm=60
    st.write("Resistividad del lodo de formacion:",Rms)
    st.write("Temperatura del lodo:",Pm)

    df_filtrado["Rmf"]=1.17*((Tm+6.77)/(df_filtrado.TF+6.77))


    #Calculos SP
    valor_minimosp = df_filtrado["SP"].min()
    st.write("El valor minimo del SP:",valor_minimosp)

    #Calculo de resistividad de agua equivalente
    df_filtrado["k"]=61.3+0.133*df_filtrado.TF


    df_filtrado["Rwe"]=df_filtrado.Rmf/(10**(valor_minimosp/-df_filtrado.k))

    #Calculo Rw
    Rw=0.11 #60 ºF
    st.write("Resistividad del agua:",Rw)
    df_filtrado['Rwf']=Rw*((Ts+6.77)/(df_filtrado.TF+6.77))

    st.title("Tabla para determinar conductividad")
    imagen1= Image.open("Conductividad.jpg")
    st.image(imagen1)

    #Calculo del factor de formacion 
    df_filtrado['F']=1.13/(df_filtrado.PT**1.73)


    #Calculo de Ro #(Resitividad de formacion)
    df_filtrado['Ro']=df_filtrado.F*df_filtrado.Rwf


    #Calculo de Sw
    df_filtrado['Sw']=(df_filtrado.Ro/df_filtrado.RT)**0.5


    #Calculo de So
    df_filtrado['So']=1-df_filtrado.Sw


    #Calculo de Rwa
    df_filtrado['Rwa']=df_filtrado.RT/df_filtrado.F


    #Calculo de Rwa/Rwf
    df_filtrado['Rwa/Rwf']=df_filtrado.Rwa/df_filtrado.Rwf


    bins = (0.0, 3.0, 1000.0)
    grupos_nombres = ['No pago','Pago']
    df_filtrado['Zonas de pago'] = pd.cut(df_filtrado['Rwa/Rwf'], bins=bins, labels = grupos_nombres)
    df_filtrado['Zonas de pago'].unique()

    st.header("Data Frame Resultante")
    st.write(df_filtrado.astype('object'))

    #Grafico_Zonas de pago 
    Grafico=alt.Chart(df_filtrado.astype('object')).mark_bar().encode(
        x="Zonas de pago",
        y="count()",
        tooltip=['Zonas de pago',"count()"]).interactive().properties(width=400, height = 300)
    st.altair_chart(Grafico)

    
    df_filtrado.reset_index(level=0 , inplace =True)

    st.write(df_filtrado.astype('object'))
    df_clean = df_filtrado.dropna(subset=['Rwa/Rwf'],axis=0, how='any')
    st.write(df_clean.astype('object'))
    Grafico2 = alt.Chart(df_clean.astype('object')).mark_line().encode(
        y="Rwa/Rwf",
        x= "DEPTH"

        ).properties(width=400, height = 300)

    

    st.altair_chart(Grafico2)