##PEPE TERRITORIAL
# Cargar librerias
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
from io import BytesIO
import openpyxl  # pip install openpyxl


st.set_page_config(layout="wide")
st.title("PEPE Territorial") 
#Menu lateral
from streamlit_option_menu import option_menu

menu = option_menu(
    None,
    ["Main","Ingresos","Gastos","Coyuntura","Treemap","Presupuesto actual","Descarga de datos"],
    icons=[
        "house",
        "cash-coin",
        "credit-card",
        "graph-up",
        "diagram-3",
        "clipboard-data",
        "download"
    ],
    orientation="horizontal",
    default_index=0
)
#Que el menu cambie segun la selección
#Inicio
if menu=="Main":
    st.header("Main")

#Ingresos
elif  menu=="Ingresos":
    st.header("Ingresos")
    tab1, tab2,tab3=st.tabs(["General","Departamental","Municipal"])
    with tab1:
        #################GENERAL################################################
        ##Gráfica del historico
        st.subheader("Histórico general")
        st.caption("Cifras en miles de millones de pesos")
        df=pd.read_parquet("data/ing.parquet")
        ## las graficas se vean una al lado de la otra
        col1, col2=st.columns(2)
        ##agrupe los datos  por año para hacer la grafica 
        with col1:
          agrupamiento_año=df.groupby("Año")["TotalRecaudo"].sum().reset_index()
          agrupamiento_año["Total_mm"]=agrupamiento_año["TotalRecaudo"]/1_000_000_000
          fig=px.line(agrupamiento_año,x="Año",y="Total_mm", markers=True)
          fig.update_yaxes(title=None)
          st.plotly_chart(fig)
          ##############################################################################

        with col2:
           ##Barras apiladas con Nueva clasificación
           agrupar_barras_api=df.groupby(["Año","clas_gen"])["TotalRecaudo"].sum().reset_index()
           agrupar_barras_api["Total_año"]=agrupar_barras_api.groupby("Año")["TotalRecaudo"].transform("sum")
           agrupar_barras_api["Porcentaje"]=agrupar_barras_api["TotalRecaudo"]/agrupar_barras_api["Total_año"]*100
           ##Gráfica de barras apiladas
           fig_barras=px.bar(
               agrupar_barras_api,
               x=("Año"),
               y=("Porcentaje"),
               color=("clas_gen"),
               barmode="stack"
           )
           fig_barras.update_yaxes(title=None)
           fig_barras.update_layout(legend_title=None)
           fig_barras.update_xaxes(tickmode="linear",dtick=2)
           fig_barras.update_layout(
               legend=dict(
                   orientation="h",
                   yanchor="top",
                   y=-0.2,
                   xanchor="left",
                   x=0
               )
           )
           st.plotly_chart(fig_barras,use_container_width=True)
        #################################FUERA COL1 Y COL2###########################
        ## Gráfica de area apilada con Clasificación General
        ## agrupamos las variables
        df["clasificacion_limpia"]="Otros"
        df.loc[df["clasificacion_ofpuj"].str.contains("TRANSFER",case=False,na=False),"clasificacion_limpia"]="Transferencias"
        df.loc[df["clasificacion_ofpuj"].str.contains("IMPUEST|TRIBUT",case=False,na=False),"clasificacion_limpia"]="Impuestos"
        df.loc[df["clasificacion_ofpuj"].str.contains("MULTA|SANCION",case=False,na=False),"clasificacion_limpia"]="Multas y sanciones"
        df.loc[df["clasificacion_ofpuj"].str.contains("CONTRIBU",case=False,na=False),"clasificacion_limpia"]="Contribuciones"
        df.loc[df["clasificacion_ofpuj"].str.contains("CAPITAL",case=False,na=False),"clasificacion_limpia"]="Recursos de capital"
        ## Gráfica de barras apiladas del ingreso clasificación normalita
        area_df=df.groupby(["Año","clasificacion_limpia"])["TotalRecaudo"].sum().reset_index()
        area_df["Total_anual_area1"]=area_df.groupby("Año")["TotalRecaudo"].transform("sum")###
        area_df["Porcentaje_area1"]= area_df["TotalRecaudo"]/area_df["Total_anual_area1"]###
        ##Gráfica area apilada
        fig_area_api=px.area(
            area_df,
            x="Año",
            y="Porcentaje_area1",
            color="clasificacion_limpia"
         )
        fig_area_api.update_yaxes(title=None)
        fig_area_api.update_yaxes(tickformat=".0%")
        fig_area_api.update_xaxes(
            tickmode="array",
            tickvals=[2012, 2014, 2016, 2018, 2020, 2022, 2024],
            ticktext=["2012", "2014", "2016", "2018", "2020", "2022", "2024"],
            range=[2011.8, 2024.8]
        )
        fig_area_api.update_layout(legend_title=None)
        fig_area_api.update_layout(
            legend_title=None,
            legend=dict(
                 orientation="h",
                 yanchor="top",
                 y=-0.2,
                 xanchor="left",
                 x=0
               )
                  
           )
        st.plotly_chart(fig_area_api,use_container_width=True)

        #########################################################################
        ###############################SGP_GENERAL##############################
        st.subheader("Sistema General de Participaciones (SGP)")
        BASE_DIR = Path(__file__).resolve().parent
        RUTA_SGP = BASE_DIR / "data" / "datos_sgp_pib_ic.parquet"
        df_sgp = pd.read_parquet(RUTA_SGP)
       ###listo ya cargada la primera base hagamos la primera grafica
       ## como hay muchas categorias me quedare con col1 la principal
        col1, col2=st.columns(2)
        ###############################COL1_sgp###############################################
        with col1:
        ####Gráfico de Linea SGP
            sgp_total = (
            df_sgp.groupby("Año", as_index=False)["valor_constante_25"].sum()
            )
            sgp_total["valor_mm"] = sgp_total["valor_constante_25"] / 1_000_000_000
            sgp_total = sgp_total[
             (sgp_total["Año"] >= 2012) & (sgp_total["Año"] <= 2024)
            ]
            fig_sgp_2 = px.line(
                 sgp_total,
                 x="Año",
                 y="valor_mm",
                 markers=True
                )
            fig_sgp_2.update_yaxes(title=None)
            fig_sgp_2.update_yaxes(title=None, tickformat=",.0f")
            st.plotly_chart(fig_sgp_2, use_container_width=True)
        #######################COL2_sgp##########################################################
        with col2:
            ##grafico barras apiladas
            ## solo renombre
            df_sgp["clasificacion_sgp"] = df_sgp["nivel_1"]
            df_sgp["clasificacion_sgp"] = df_sgp["clasificacion_sgp"].replace({
            "Agua Potable": "Agua y saneamiento básico",
            "Propósito General": "Inversiones con propósito general"
            })
            ##filtro los años que estoy teniendo en cuenta
            df_sgp_filtrado = df_sgp[(df_sgp["Año"] >= 2012) & (df_sgp["Año"] <= 2024)
            ].copy()
            ## agrupo lo que me interesa
            barra_sgp = (
            df_sgp_filtrado.groupby(["Año", "clasificacion_sgp"], as_index=False)["valor_constante_25"].sum()
            )
            #columna total
            barra_sgp["total_año"] = barra_sgp.groupby("Año")["valor_constante_25"].transform("sum")
            #columna porcentaje
            barra_sgp["porcentaje"] = (
            barra_sgp["valor_constante_25"] / barra_sgp["total_año"]
            ) * 100
            ## genera un orden para cada año
            orden = [
                "Educación",
                "Salud",
                "Agua y saneamiento básico",
                "Inversiones con propósito general",
                "Asignaciones especiales"
                ]

            df_sgp_filtrado["clasificacion_sgp"] = df_sgp_filtrado["clasificacion_sgp"].where(
            df_sgp_filtrado["clasificacion_sgp"].isin(orden),
             "Otros"
            )#####estudiar bien

            orden.append("Otros")
            ## ordena segun los años 
            barra_sgp = barra_sgp.sort_values(["Año", "clasificacion_sgp"])
            ##Gráfica barras apiladas
            fig_barra_sgp = px.bar(
                barra_sgp,
                x="Año",
                y="porcentaje",
                color="clasificacion_sgp",
                barmode="stack"
            )
            fig_barra_sgp.update_yaxes(title=None)
            fig_barra_sgp.update_layout(legend_title=None)
            fig_barra_sgp.update_xaxes(tickmode="linear",dtick=2)
            fig_barra_sgp.update_layout(
               legend=dict(
                   orientation="h",
                   yanchor="top",
                   y=-0.2,
                   xanchor="left",
                   x=0
               )
            )
            st.plotly_chart(fig_barra_sgp, use_container_width=True)
       
         #############FUERA COL1 Y COL2 SGP##############################################
         #crear la variable
        df_sgp["clasificacion_sgp_2"] = df_sgp["nivel_2"]##trabajar sin dañar 
        ##mi filtro año
        df_sgp_filtrado = df_sgp[(df_sgp["Año"] >= 2012) & (df_sgp["Año"] <= 2024)
        ].copy()
        ##Agrupar los datos que necesito
        area_sgp = df_sgp_filtrado.groupby(["Año", "clasificacion_sgp_2"], as_index=False)["valor_constante_25"].sum()
        ##calculamos el total para los porcentajes
        area_sgp["total_año"] = area_sgp.groupby("Año")["valor_constante_25"].transform("sum")
        ##Calcular porcentajes
        area_sgp["porcentaje"] = (
        area_sgp["valor_constante_25"] / area_sgp["total_año"]* 100
        )
        area_sgp = area_sgp.sort_values(["Año", "clasificacion_sgp_2"])
        fig_area_sgp = px.area(
            area_sgp,
             x="Año",
             y="porcentaje",
             color="clasificacion_sgp_2"
             )

        
        fig_area_sgp.update_yaxes(title=None)
        fig_area_sgp.update_xaxes(
            tickmode="array",
            tickvals=[2012, 2014, 2016, 2018, 2020, 2022, 2024],
            ticktext=["2012", "2014", "2016", "2018", "2020", "2022", "2024"],
            range=[2011.8, 2024.8]
        )
        fig_area_sgp.update_layout(legend_title=None)
        fig_area_sgp.update_layout(
            legend_title=None,
            legend=dict(
                 orientation="h",
                 yanchor="top",
                 y=-0.2,
                 xanchor="left",
                 x=0
               )
                  
           )
        st.plotly_chart(fig_area_sgp,use_container_width=True)

        ###############################################################################################
        ##Treemap 
        ##titulo
        st.subheader("Asignación del SGP por categoría")
        ##Primero el filtro de año
        año_sgp = st.slider(
         "Seleccione el año",
            min_value=2012,
            max_value=2024,
            value=2012,
            step=1,
            key="slider_treemap_sgp"
        )
        ##hacemos filtro para años necesitamos
        ##que el año seleccionado sea igual al del SGP
        df_sgp_año = df_sgp[df_sgp["Año"] == año_sgp].copy()
        ##cambiar los nombres a unos mas apropiados
        df_sgp_año["categoria_sgp"] = df_sgp_año["nivel_1"].replace({
        "Agua Potable": "Agua y saneamiento básico",
        "Propósito General": "Inversiones con propósito general"
        })
        ###genere la profundidad con nivel_2
        df_sgp_año["subcategoria_sgp"] = df_sgp_año["nivel_2"].fillna("Sin detalle")
        ##agrupe las columnas que me interesan
        treemap_sgp = (df_sgp_año.groupby( ["categoria_sgp", "subcategoria_sgp"],as_index=False)["valor_constante_25"].sum())
        treemap_sgp["valor_mm"] = treemap_sgp["valor_constante_25"] / 1_000_000_000
        ##Gráfica
        treemap_fig_sgp = px.treemap(
            treemap_sgp,
            path=["categoria_sgp", "subcategoria_sgp"],
            values="valor_mm"
        )
        ##estetica
        treemap_fig_sgp.update_layout(margin=dict(t=40, l=10, r=10, b=10))##visual
        treemap_fig_sgp.update_traces(textinfo="label+percent entry")#muestra texto y porcentaje
        treemap_fig_sgp.update_traces(
            textfont=dict(
            size=16,
            color="white"
         )
         )#letra
        treemap_fig_sgp.update_traces(
            marker=dict(
            line=dict(width=4, color="white")
        )
        )##bordes
        st.plotly_chart(
        treemap_fig_sgp,use_container_width=True,key="treemap_sgp_general")    
        #########################################################################
        ##Nuevo gráfico de linea SGP/PIB SGP/IC 
        #titulo 
        col1, col2=st.columns(2)
        with col1:
            ###Con pib
            st.subheader("Evolución anual del valor del SGP sobre el PIB")
            sgp_pib = (
            df_sgp.groupby("Año", as_index=False)["valor_sgp_pib"].sum()
            )
            # Filtrar años
            sgp_pib = sgp_pib[
            (sgp_pib["Año"] >= 2012) & (sgp_pib["Año"] <= 2024)
            ]

            # Gráfica
            fig_sgp_pib = px.line(
                sgp_pib,
                x="Año",
                y="valor_sgp_pib",
                markers=True
             )
            fig_sgp_pib.update_yaxes(title=None)
            st.plotly_chart(fig_sgp_pib, use_container_width=True)
        with col2:
             st.subheader("Evolución anual del valor del SGP sobre el ingresos corrientes")
             #Grafica con Ingresos corrientes
             sgp_ic = (
            df_sgp.groupby("Año", as_index=False)["valor_sgp_ingresos_corrientes"].sum()
            )

            # Filtrar años
             sgp_ic = sgp_ic[
            (sgp_ic["Año"] >= 2012) & (sgp_ic["Año"] <= 2024)
            ]

            # Gráfica
             fig_sgp_ic = px.line(
            sgp_ic,
                 x="Año",
                 y="valor_sgp_ingresos_corrientes",
                 markers=True,
             )

             fig_sgp_ic.update_yaxes(title=None)

             st.plotly_chart(fig_sgp_ic, use_container_width=True)
        
        
            ########################DEPARTAMENTAL#########################################
    with tab2:
        departamentos=sorted(df["Departamento"].dropna().unique())
        seleccionar_depto=st.selectbox("Seleccione un Departamento",departamentos)
        st.caption("Cifras en miles de millones de pesos")
        col1,col2=st.columns(2)
        with col1:
           ##Gráfica general con filtro
           depto_filtrado=df[df["Departamento"]==seleccionar_depto]
           agrupar_depto=depto_filtrado.groupby("Año")["TotalRecaudo"].sum().reset_index()
           agrupar_depto["Total_mm"]= agrupar_depto["TotalRecaudo"]/1_000_000_000
           agrupar_depto = agrupar_depto.sort_values("Año")###cambio_deptos
           fig_gen_depto=px.line(
               agrupar_depto,
               x="Año",
               y="Total_mm",
               markers=True

            )
           fig_gen_depto.update_yaxes(title=None)
           fig_gen_depto.update_xaxes(tickmode="linear",dtick=2)########
           st.plotly_chart(fig_gen_depto)
           
           ######################################################################
        with col2:
            agrupar_depto_barrasapi=depto_filtrado.groupby(["Año","clasificacion_limpia"])["TotalRecaudo"].sum().reset_index()
            agrupar_depto_barrasapi["Total_año_dep"]=agrupar_depto_barrasapi.groupby("Año")["TotalRecaudo"].transform("sum")
            agrupar_depto_barrasapi["Porcentaje_dpto"]= agrupar_depto_barrasapi["TotalRecaudo"]/ agrupar_depto_barrasapi["Total_año_dep"]*100
            agrupar_depto_barrasapi = agrupar_depto_barrasapi.groupby("Año").filter(
              lambda x: x["Porcentaje_dpto"].sum() > 0####no deja ver cosas que esten en 0
)
            agrupar_depto_barrasapi= agrupar_depto_barrasapi.sort_values("Año")#############################ordeno mis años
            años_dep = sorted(agrupar_depto_barrasapi["Año"].unique())##################################ordeno mis ejes del grafico
            fig_dep_depto=px.bar(
                agrupar_depto_barrasapi,
                x="Año",
                y="Porcentaje_dpto",
                color="clasificacion_limpia",
                barmode="stack"

         )
            fig_dep_depto.update_yaxes(title=None)
            fig_dep_depto.update_xaxes(
                 type="category",
                 categoryorder="array",
                 categoryarray=años_dep
                 )#################################### 
            fig_dep_depto.update_layout(legend_title=None)
            fig_dep_depto.update_layout(
               legend=dict(
                   orientation="h",
                   yanchor="top",
                   y=-0.15,
                   xanchor="left",
                   x=0
               )
            )
            st.plotly_chart(fig_dep_depto)
     ######################################FUERA COL1 Y COL2###################################################       
     ##Gráfica area 
        area_dep=depto_filtrado.groupby(["Año","clas_gen"])["TotalRecaudo"].sum().reset_index()
        area_dep["Total_area2"]=area_dep.groupby("Año")["TotalRecaudo"].transform("sum")
        area_dep["Porcentaje_area2"]=area_dep["TotalRecaudo"]/area_dep["Total_area2"]
        fig_are_dep=px.area(
            area_dep,
            x="Año",
            y="Porcentaje_area2",
            color="clas_gen"
        )
        fig_are_dep.update_yaxes(title=None)
        fig_are_dep.update_yaxes(tickformat=".0%")
        fig_are_dep.update_xaxes(
        tickmode="array",
        tickvals=[2012, 2014, 2016, 2018, 2020, 2022, 2024],
        ticktext=["2012", "2014", "2016", "2018", "2020", "2022", "2024"],
        range=[2011.8, 2024.8]
        )
        fig_are_dep.update_layout(legend_title=None)
        fig_are_dep.update_layout(
           legend_title=None,
           legend=dict(
               orientation="h",
               yanchor="top",
                y=-0.2,
                xanchor="left",
                x=0
            )
                  
           )
        st.plotly_chart(fig_are_dep,use_container_width=True)
        #########################SGP DEPARTAMENTAL#########################################
        ##################################################################################
        #selector de año
        st.subheader("Sistema General de Participaciones (SGP)")###
        año_sgp_dep=st.slider(
            "Seleccione el año",
            int(depto_filtrado["Año"].min()),
            int(depto_filtrado["Año"].max()),
            int(depto_filtrado["Año"].min()),
            key="slider_sgp_depto"
        )
        fil_año_depto=depto_filtrado[depto_filtrado["Año"]==año_sgp_dep].copy()
        df_sgp_depto=fil_año_depto[
            (
        fil_año_depto["clasificacion_ofpuj"].astype(str).str.strip().str.upper()
        =="SISTEMA GENERAL DE PARTICIPACIONES"
        )
        |
        (
             fil_año_depto["col_5"].astype(str).str.upper().str.contains(
                 "PARTICIPACIONES", na=False
             )
        )
        ].copy()

        def clasificar_cate_sgp_dep(valor):
            valor=str(valor).strip().upper()
            if "EDUCACION" in valor or "EDUCACIÓN" in valor:
                 return "Educación"
            elif "SALUD" in valor:
                 return "Salud"
            elif "AGUA" in valor or "SANEAMIENTO" in valor:
                return "Agua y saneamiento básico"
            elif "PROPOSITO GENERAL" in valor or "PROPÓSITO GENERAL" in valor:
                 return "Inversiones con propósito general"
            elif "ASIGNACIONES ESPECIALES" in valor:
                return "Asignaciones especiales"
            else:
                return "Otras"
        ##esto junta toda la jerarquia de la base
        df_sgp_depto["texto_sgp"] = (
            df_sgp_depto["col_5"].astype(str) + " " +
            df_sgp_depto["col_6"].astype(str) + " " +
            df_sgp_depto["col_7"].astype(str) + " " +
            df_sgp_depto["col_8"].astype(str) + " " +
            df_sgp_depto["col_9"].astype(str) + " " +
            df_sgp_depto["col_10"].astype(str)
        )
        df_sgp_depto["categoria_sgp_dep"]= df_sgp_depto["texto_sgp"].apply( clasificar_cate_sgp_dep)
        df_sgp_depto=df_sgp_depto[df_sgp_depto["categoria_sgp_dep"]!= "Otras"].copy()
        ###agrupar recaudo por clasificacion
        fig_treemap_sgp_dep=px.treemap(
            df_sgp_depto,
             path=["categoria_sgp_dep","col_7"],
             values="TotalRecaudo",
        )
        #Estilo

        fig_treemap_sgp_dep.update_layout(
             margin=dict(t=40, l=10, r=10, b=10)
         )
        ##muestra porcentajes
        fig_treemap_sgp_dep.update_traces(
            textinfo="label+percent entry",
        )
        ##Texto mas estetico
        fig_treemap_sgp_dep.update_traces(
            textfont=dict(
                size=16,
                color="white"
            )
        )
        ## por ultimo un lindo borde jejejeej
        fig_treemap_sgp_dep.update_traces(
           marker=dict(
               line=dict(width=4,color="white")
           )  
        )
        st.plotly_chart(
            fig_treemap_sgp_dep,
            use_container_width=True,
             key="treemap_sgp_general_dep"
             )

        ###################################################################################################  
        ##########################MUNICIPAL##############################################################
    with tab3:
        ##Filtro de departamento
        departamentos_mun=sorted(df["Departamento"].dropna().unique())
        seleccionar_depto_mun=st.selectbox("Selecciona un Departamento", departamentos_mun ,key="mun_depto")
        df_municipios_base=df[
            (df["Departamento"]==seleccionar_depto_mun)&
            (df["Tipo de Entidad"]=="Municipio")&
            (df["Entidad"] != "Boyacá")##force a boyaca a irse jejeje
        ]
        municipios_lista=sorted(df_municipios_base["Entidad"].dropna().unique())
        ##Filtro Municipio
        seleccionar_municipio=st.selectbox("Selecciona un Municipio", municipios_lista,key="mun_entidad")
        ##data ya filtrada
        df_filtrado_m_d=df_municipios_base[df_municipios_base["Entidad"]==seleccionar_municipio]
        st.write("Cifras en miles de millones de pesos")
        col1, col2 = st.columns(2)
        with col1: 
            ##Gráfica general
            agrupar_municipios_l= df_filtrado_m_d.groupby("Año")["TotalRecaudo"].sum().reset_index()
            agrupar_municipios_l["Total_mm"]= agrupar_municipios_l["TotalRecaudo"]/1_000_000_000
            agrupar_municipios_l= agrupar_municipios_l.sort_values("Año")
            fig_gen_mun=px.line(
                agrupar_municipios_l,
                x="Año",
                y="Total_mm",
                markers=True
            )
            fig_gen_mun.update_yaxes(title=None)
            st.plotly_chart(fig_gen_mun)
            #############################################################################
        with col2:
            ##Gráfica de barras apiladas
            agrupar_mun_barrasapi=df_filtrado_m_d.groupby(["Año","clasificacion_limpia"])["TotalRecaudo"].sum().reset_index()
            agrupar_mun_barrasapi["Total_año_mun"]= agrupar_mun_barrasapi.groupby("Año")["TotalRecaudo"].transform("sum")
            agrupar_mun_barrasapi["Porcentaje_mun"]=agrupar_mun_barrasapi["TotalRecaudo"]/agrupar_mun_barrasapi["Total_año_mun"]*100
            agrupar_mun_barrasapi = agrupar_mun_barrasapi.groupby("Año").filter(
               lambda x: x["Porcentaje_mun"].sum() > 0
              )############# no deja ver años que esten en 0
            agrupar_mun_barrasapi=agrupar_mun_barrasapi.sort_values("Año")
            años_mun = sorted(agrupar_mun_barrasapi["Año"].unique())### mis años que si existen
            fig_mun_barras=px.bar(
                agrupar_mun_barrasapi,
                x="Año",
                y="Porcentaje_mun",
                color="clasificacion_limpia",
                barmode="stack"
            )
            fig_mun_barras.update_yaxes(title=None)
            fig_mun_barras.update_xaxes(
                 type="category",
                 categoryorder="array",
                 categoryarray=años_mun
                 )#################################### 
            fig_mun_barras.update_layout(legend_title=None)
            fig_mun_barras.update_layout(
               legend=dict(
                   orientation="h",
                   yanchor="top",
                   y=-0.15,
                   xanchor="left",
                   x=0
               )
            )
            st.plotly_chart( fig_mun_barras)
        #####################################FUERA COL1 Y COL 2###################################
          #Gráfica de area
        area_api_mun= df_filtrado_m_d.groupby(["Año","clas_gen"])["TotalRecaudo"].sum().reset_index()
        area_api_mun["Total_area3"]=area_api_mun.groupby("Año")["TotalRecaudo"].transform("sum")
        area_api_mun["Porcentaje_mun"]=area_api_mun["TotalRecaudo"]/ area_api_mun["Total_area3"]
        area_api_mun=area_api_mun.sort_values("Año")
        fig_area_api_mun=px.area(
            area_api_mun,
            x="Año",
            y="Porcentaje_mun",
            color="clas_gen"

        )
        fig_area_api_mun.update_yaxes(title=None)
        fig_area_api_mun.update_yaxes(tickformat=".0%")
        fig_area_api_mun.update_xaxes(
            tickmode="array",
            tickvals=[2012, 2014, 2016, 2018, 2020, 2022, 2024],
            ticktext=["2012", "2014", "2016", "2018", "2020", "2022", "2024"],
            range=[2011.8, 2024.8]
        )
        fig_area_api_mun.update_layout(legend_title=None)
        fig_area_api_mun.update_layout(
           legend_title=None,
           legend=dict(
               orientation="h",
               yanchor="top",
               y=-0.2,
               xanchor="left",
               x=0
            )
                  
           )
        st.plotly_chart( fig_area_api_mun,use_container_width=True)    
        ############################SGP MUNICIPAL##################################
        #############################################################################
        ##Filtro de año
        año_sgp_mun=st.slider(
            "Seleccione el año",
            int(df_filtrado_m_d["Año"].min()),
            int(df_filtrado_m_d["Año"].max()),
            int(df_filtrado_m_d["Año"].max()),
            key="slider_sgp_municipal"
        )
        fil_año_mun=df_filtrado_m_d[df_filtrado_m_d["Año"]==año_sgp_mun].copy()
        df_sgp_mun=fil_año_mun[
            (
            fil_año_mun["clasificacion_ofpuj"].astype(str).str.strip().str.upper()
             == "SISTEMA GENERAL DE PARTICIPACIONES"
            )
            |
            (
            fil_año_mun["col_5"].astype(str).str.upper().str.contains(
             "PARTICIPACIONES", na=False)
            )
        ].copy()

        def clasificar_categoriaa_sgp_mun (valor):
            valor=str(valor).strip().upper()
            if "EDUCACION" in valor or "EDUCACIÓN" in valor:
                return "Educación"
            elif "SALUD" in valor:
                return "Salud"
            elif "AGUA" in valor or "SANEAMIENTO" in valor:
                return "Agua y saneamiento básico"
            elif "PROPOSITO GENERAL" in valor or "PROPÓSITO GENERAL" in valor:
                return "Inversiones con propósito general"
            elif "ASIGNACIONES ESPECIALES" in valor:
                 return "Asignaciones especiales"
            else:
                return "Otras"
        ##juntamos col de la base
        df_sgp_mun["texto_sgp_m"] = (
        df_sgp_mun["col_5"].astype(str) + " " +
        df_sgp_mun["col_6"].astype(str) + " " +
        df_sgp_mun["col_7"].astype(str) + " " +
        df_sgp_mun["col_8"].astype(str) + " " +
        df_sgp_mun["col_9"].astype(str) + " " +
        df_sgp_mun["col_10"].astype(str)
         )
        #######le aplica la clasificación a la información que unimos

        df_sgp_mun["categoria_sgp_mun"]=df_sgp_mun["texto_sgp_m"].apply(clasificar_categoriaa_sgp_mun)
        df_sgp_mun= df_sgp_mun[ df_sgp_mun["categoria_sgp_mun"]!="Otras"].copy()
        ##Gráfico
        treemap_fig_sgp_mun=px.treemap(
            df_sgp_mun,
            path=["categoria_sgp_mun","col_7"],
            values="TotalRecaudo",
            color="categoria_sgp_mun"
        )
            #Estilo

        treemap_fig_sgp_mun.update_layout(
            margin=dict(t=40, l=10, r=10, b=10)
        )
        ##muestra porcentajes
        treemap_fig_sgp_mun.update_traces(
            textinfo="label+percent entry",
        )
        ##Texto mas estetico
        treemap_fig_sgp_mun.update_traces(
            textfont=dict(
                size=16,
                color="white"
            )
        )
        ## por ultimo un lindo borde jejejeej
        treemap_fig_sgp_mun.update_traces(
           marker=dict(
               line=dict(width=4,color="white")
           )  
        )
        st.plotly_chart(
             treemap_fig_sgp_mun,
            use_container_width=True,
             key="treemap_sgp_mun"
             )

            
#Gastos    
elif  menu=="Gastos":
    st.header("Gastos")

# =============================================================================
# COYUNTURA  — reemplazo de la sección elif menu == "Coyuntura"
# =============================================================================

elif menu == "Coyuntura":
    st.header("Coyuntura - Ejecución Presupuestal Territorial")

    DATOS_LISTOS = False  # ← cambiar a True cuando el CIFFIT actualice

    if not DATOS_LISTOS:
        st.info(" Esperando actualización del CIFFIT.")
    else:

        tab_ing, tab_gas = st.tabs(["Ingresos 2025", "Gastos 2025"])

        # =========================================================================
        # HELPERS COMPARTIDOS
        # =========================================================================
        def fmt_cop(n):
            if n >= 1e12: return f"${n/1e12:.2f} B"
            if n >= 1e9:  return f"${n/1e9:.1f} MM"
            return f"${n/1e6:.0f} M"

        def tarjeta_metrica(label, valor_cop, color_valor):
            return f"""
            <div style="background:#F1EFE8; border-radius:12px; padding:14px 18px;
                        margin-bottom:10px; border-left:4px solid {color_valor};">
                <div style="font-size:11px; font-weight:600; color:#888780;
                            letter-spacing:.06em; text-transform:uppercase;
                            margin-bottom:4px;">{label}</div>
                <div style="font-size:22px; font-weight:600; color:{color_valor};
                            font-family:'Inter',sans-serif;">{valor_cop}</div>
            </div>
            """

        # Paleta de colores por clasificación e impuesto
        COLOR_CLAS = {
            "Recursos propios":    "#185FA5",
            "Transferencias":      "#0F6E56",
            "Recursos de capital": "#BA7517",
        }
        COLOR_IMP = {
            "Estampillas":                          "#534AB7",
            "Sobretasa a la gasolina":              "#0F6E56",
            "Impuesto predial unificado":           "#185FA5",
            "Impuesto de industria y comercio":     "#BA7517",
        }

        # -------------------------------------------------------------------------
        # Función reutilizable: gauge limpio sin fondo blanco
        # -------------------------------------------------------------------------
        def make_gauge(value, title_text, subtitle="", color="#185FA5",
                    height=280, font_size=52, show_threshold=False, threshold_val=58.3):
            steps  = [
                {"range": [0,  40], "color": "#FCEBEB"},
                {"range": [40, 70], "color": "#FAEEDA"},
                {"range": [70,100], "color": "#EAF3DE"},
            ]
            gauge_cfg = {
                "axis":        {"range": [0, 100], "tickwidth": 1,
                                "tickcolor": "#888780", "tickfont": {"size": 11}, "dtick": 20},
                "bar":         {"color": color, "thickness": 0.28},
                "bgcolor":     "rgba(0,0,0,0)",   # fondo interno transparente
                "borderwidth": 0,
                "steps":       steps,
            }
            if show_threshold:
                gauge_cfg["threshold"] = {
                    "line": {"color": "#D85A30", "width": 3},
                    "thickness": 0.85,
                    "value": threshold_val,
                }
            full_title = (
                f"{title_text}<br>"
                f"<span style='font-size:13px;color:#888780'>{subtitle}</span>"
                if subtitle else title_text
            )
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=value,
                number={"suffix": "%", "font": {"size": font_size, "color": "#1a1a2e",
                                                "family": "Inter, sans-serif"}},
                gauge=gauge_cfg,
                title={"text": full_title,
                    "font": {"size": 17, "color": "#1a1a2e", "family": "Inter, sans-serif"}},
            ))
            fig.update_layout(
                height=height,
                margin=dict(t=60, b=10, l=20, r=20),
                paper_bgcolor="rgba(0,0,0,0)",   # ← sin fondo blanco
                plot_bgcolor ="rgba(0,0,0,0)",
                font_family="Inter, sans-serif",
            )
            return fig

        # =========================================================================
        # TAB INGRESOS 2025
        # =========================================================================
        with tab_ing:

            # ----- Carga de datos ------------------------------------------------
            base_dir  = Path(__file__).parent
            ejec_path = base_dir / "eje_ing_clean25.xlsx"
            prog_path = base_dir / "pro_ing_clean25.xlsx"

            @st.cache_data
            def cargar_ingresos():
                df_e = pd.read_excel(ejec_path)
                df_p = pd.read_excel(prog_path)
                for df in [df_e, df_p]:
                    df["Entidad"]         = df["Entidad"].astype(str).str.strip()
                    df["Tipo de Entidad"] = df["Tipo de Entidad"].astype(str).str.strip()
                    df["Departamento"]    = df["Departamento"].astype(str).str.strip()
                return df_e, df_p

            df_ejec, df_prog = cargar_ingresos()

            # ----- Consolidado por entidad ---------------------------------------
            group_cols = ["Entidad", "Tipo de Entidad", "Departamento"]

            ejec_agg = (df_ejec.groupby(group_cols, as_index=False)["Total Recaudo"]
                            .sum().rename(columns={"Total Recaudo": "Total_Ejecutado"}))
            prog_agg = (df_prog.groupby(group_cols, as_index=False)["Presupuesto Definitivo"]
                            .sum().rename(columns={"Presupuesto Definitivo": "Total_Programado"}))

            tabla = pd.merge(prog_agg, ejec_agg, on=group_cols, how="left")
            tabla["Total_Ejecutado"]   = tabla["Total_Ejecutado"].fillna(0)
            tabla["Tasa_Ejecución (%)"]= ((tabla["Total_Ejecutado"] / tabla["Total_Programado"]) * 100).round(2).fillna(0)

            # ----- Consolidado por clas_gen2 (clasificación) --------------------
            det_cols = group_cols + ["clas_gen2"]
            ejec_det = (df_ejec.groupby(det_cols, as_index=False)["Total Recaudo"]
                            .sum().rename(columns={"Total Recaudo": "Total_Ejecutado"}))
            prog_det = (df_prog.groupby(det_cols, as_index=False)["Presupuesto Definitivo"]
                            .sum().rename(columns={"Presupuesto Definitivo": "Total_Programado"}))
            detalle  = pd.merge(prog_det, ejec_det, on=det_cols, how="left")
            detalle["Total_Ejecutado"]    = detalle["Total_Ejecutado"].fillna(0)
            detalle["Tasa_Ejecución (%)"] = ((detalle["Total_Ejecutado"] / detalle["Total_Programado"]) * 100).round(2).fillna(0)

            # ----- Consolidado por clas_ofpuj (impuestos) -----------------------
            ofp_cols = group_cols + ["clas_ofpuj"]
            ejec_ofp = (df_ejec.groupby(ofp_cols, as_index=False)["Total Recaudo"]
                            .sum().rename(columns={"Total Recaudo": "Total_Ejecutado"}))
            prog_ofp = (df_prog.groupby(ofp_cols, as_index=False)["Presupuesto Definitivo"]
                            .sum().rename(columns={"Presupuesto Definitivo": "Total_Programado"}))
            ofpuj    = pd.merge(prog_ofp, ejec_ofp, on=ofp_cols, how="left")
            ofpuj["Total_Ejecutado"]    = ofpuj["Total_Ejecutado"].fillna(0)
            ofpuj["Tasa_Ejecución (%)"] = ((ofpuj["Total_Ejecutado"] / ofpuj["Total_Programado"]) * 100).round(2).fillna(0)

            # ----- Totales generales --------------------------------------------
            def tasas(df_sub):
                p = df_sub["Total_Programado"].sum()
                e = df_sub["Total_Ejecutado"].sum()
                t = round(e / p * 100, 2) if p > 0 else 0
                return p, e, t

            p_gen,  e_gen,  t_gen  = tasas(tabla)
            p_dep,  e_dep,  t_dep  = tasas(tabla[tabla["Tipo de Entidad"] == "Departamento"])
            p_mun,  e_mun,  t_mun  = tasas(tabla[tabla["Tipo de Entidad"] == "Municipio"])

            # =====================================================================
            # PESTAÑAS INGRESOS
            # =====================================================================
            tab1, tab2, tab3 = st.tabs(["General", "Departamental", "Municipal"])

            # ------------------------------------------------------------------
            # TAB 1 – GENERAL
            # ------------------------------------------------------------------
            with tab1:
                st.subheader("Ejecución Acumulada General")
                col1, col2, col3 = st.columns(3)

                for col, tasa, prog, ejec, titulo in [
                    (col1, t_gen,  p_gen,  e_gen,  "Nacional"),
                    (col2, t_dep,  p_dep,  e_dep,  "Departamentos"),
                    (col3, t_mun,  p_mun,  e_mun,  "Municipios"),
                ]:
                    with col:
                        st.plotly_chart(
                            make_gauge(tasa, titulo, show_threshold=True),
                            use_container_width=True,
                            config={"displayModeBar": False},
                        )
                        st.caption(f"**Ejecutado / Programado:** {fmt_cop(ejec)} / {fmt_cop(prog)}")
                        st.divider()
                        if tasa > 100:
                            st.metric("Sobreejecución", f"+{tasa-100:.1f}%",
                                    f"+{fmt_cop(ejec-prog)}", delta_color="normal")
                        else:
                            st.metric("Falta por ejecutar", f"{100-tasa:.1f}%",
                                    f"{fmt_cop(prog-ejec)} restantes", delta_color="inverse")

            # ------------------------------------------------------------------
            # TAB 2 – DEPARTAMENTAL
            # ------------------------------------------------------------------
            with tab2:
                st.subheader("Nivel Departamental")
                df_dep = tabla[tabla["Tipo de Entidad"] == "Departamento"].copy()

                if df_dep.empty:
                    st.info("No hay datos departamentales disponibles.")
                else:
                    entidad_sel = st.selectbox(
                        "Selecciona Departamento",
                        sorted(df_dep["Entidad"].unique()),
                        key="ing_dep_sel",
                    )
                    row    = df_dep[df_dep["Entidad"] == entidad_sel].iloc[0]
                    tasa   = row["Tasa_Ejecución (%)"]
                    prog   = row["Total_Programado"]
                    ejec   = row["Total_Ejecutado"]

                    # — Gauge principal + métricas —
                    col_gauge, col_metrics = st.columns([1.4, 1])
                    with col_gauge:
                        st.plotly_chart(
                            make_gauge(tasa, "Tasa de ejecución total",
                                    subtitle=f"Acumulado 2025 · {entidad_sel}",
                                    show_threshold=True),
                            use_container_width=True,
                            config={"displayModeBar": False},
                        )
                        st.caption("**Ejecutado / Programado**")

                    with col_metrics:
                        st.markdown(tarjeta_metrica("Programado",  fmt_cop(prog),        "#185FA5"), unsafe_allow_html=True)
                        st.markdown(tarjeta_metrica("Ejecutado",   fmt_cop(ejec),        "#1D9E75"), unsafe_allow_html=True)
                        st.markdown(tarjeta_metrica("Rezago",      fmt_cop(prog - ejec), "#D85A30"), unsafe_allow_html=True)

                    st.divider()

                    # — Zona 2: Clasificación | Impuesto —
                    col_clas, col_imp = st.columns(2)

                    # ── Clasificación clas_gen2 (gauge individual) ──────────────
                    with col_clas:
                        st.markdown("### Ejecución por Clasificación")
                        opciones_clas = ["Recursos propios", "Transferencias", "Recursos de capital"]
                        clas_sel = st.selectbox(
                            "Selecciona una clasificación",
                            opciones_clas,
                            key="ing_clas_dep",
                        )
                        df_c = detalle[
                            (detalle["Entidad"] == entidad_sel) &
                            (detalle["clas_gen2"] == clas_sel)
                        ]
                        if not df_c.empty:
                            p_c = df_c["Total_Programado"].sum()
                            e_c = df_c["Total_Ejecutado"].sum()
                            t_c = round(e_c / p_c * 100, 2) if p_c > 0 else 0
                            color_c = COLOR_CLAS.get(clas_sel, "#185FA5")
                            st.plotly_chart(
                                make_gauge(t_c, clas_sel, color=color_c, height=240, font_size=40),
                                use_container_width=True,
                                config={"displayModeBar": False},
                            )
                            st.caption(f"Ejecutado: **{fmt_cop(e_c)}** / Programado: **{fmt_cop(p_c)}**")
                        else:
                            st.info(f"Sin datos para {clas_sel}.")

                    # ── Impuesto principal (gauge individual) ──────────────────
                    with col_imp:
                        st.markdown("### Impuestos Principales")
                        opciones_imp_dep = ["Estampillas", "Sobretasa a la gasolina"]
                        imp_sel = st.selectbox(
                            "Selecciona un impuesto",
                            opciones_imp_dep,
                            key="ing_imp_dep",
                        )
                        mask   = ofpuj["clas_ofpuj"].str.contains(imp_sel, case=False, na=False)
                        df_imp = ofpuj[(ofpuj["Entidad"] == entidad_sel) & mask]
                        if not df_imp.empty:
                            p_i = df_imp["Total_Programado"].sum()
                            e_i = df_imp["Total_Ejecutado"].sum()
                            t_i = round(e_i / p_i * 100, 2) if p_i > 0 else 0
                            color_i = COLOR_IMP.get(imp_sel, "#185FA5")
                            st.plotly_chart(
                                make_gauge(t_i, imp_sel, color=color_i, height=240, font_size=40),
                                use_container_width=True,
                                config={"displayModeBar": False},
                            )
                            st.caption(f"Ejecutado: **{fmt_cop(e_i)}** / Programado: **{fmt_cop(p_i)}**")
                        else:
                            st.info(f"Sin datos para {imp_sel}.")

                    st.divider()
                    with st.expander("Ver tabla de detalle completa"):
                        st.dataframe(tabla[tabla["Entidad"] == entidad_sel], use_container_width=True)

            # ------------------------------------------------------------------
            # TAB 3 – MUNICIPAL
            # ------------------------------------------------------------------
            with tab3:
                st.subheader("Nivel Municipal")
                df_mun_t = tabla[tabla["Tipo de Entidad"] == "Municipio"].copy()

                if df_mun_t.empty:
                    st.info("No hay datos municipales disponibles.")
                else:
                    deptos_mun = sorted(df_mun_t["Departamento"].unique())
                    depto_sel  = st.selectbox("Selecciona un Departamento", deptos_mun, key="ing_mun_depto_sel")
                    muns_lista = sorted(df_mun_t[df_mun_t["Departamento"] == depto_sel]["Entidad"].unique())
                    entidad_sel = st.selectbox("Selecciona un Municipio", muns_lista, key="ing_mun_sel")

                    row  = df_mun_t[df_mun_t["Entidad"] == entidad_sel].iloc[0]
                    tasa = row["Tasa_Ejecución (%)"]
                    prog = row["Total_Programado"]
                    ejec = row["Total_Ejecutado"]

                    # — Gauge principal + métricas —
                    col_gauge, col_metrics = st.columns([1.4, 1])
                    with col_gauge:
                        st.plotly_chart(
                            make_gauge(tasa, "Tasa de ejecución total",
                                    subtitle=f"Acumulado 2025 · {entidad_sel}",
                                    show_threshold=True),
                            use_container_width=True,
                            config={"displayModeBar": False},
                        )
                        st.caption("**Ejecutado / Programado**")

                    with col_metrics:
                        st.markdown(tarjeta_metrica("Programado",  fmt_cop(prog),        "#185FA5"), unsafe_allow_html=True)
                        st.markdown(tarjeta_metrica("Ejecutado",   fmt_cop(ejec),        "#1D9E75"), unsafe_allow_html=True)
                        st.markdown(tarjeta_metrica("Rezago",      fmt_cop(prog - ejec), "#D85A30"), unsafe_allow_html=True)

                    st.divider()

                    # — Zona 2: Clasificación | Impuesto —
                    col_clas, col_imp = st.columns(2)

                    # ── Clasificación clas_gen2 (gauge individual) ──────────────
                    with col_clas:
                        st.markdown("### Ejecución por Clasificación")
                        opciones_clas = ["Recursos propios", "Transferencias", "Recursos de capital"]
                        clas_sel = st.selectbox(
                            "Selecciona una clasificación",
                            opciones_clas,
                            key="ing_clas_mun",
                        )
                        df_c = detalle[
                            (detalle["Entidad"] == entidad_sel) &
                            (detalle["clas_gen2"] == clas_sel)
                        ]
                        if not df_c.empty:
                            p_c = df_c["Total_Programado"].sum()
                            e_c = df_c["Total_Ejecutado"].sum()
                            t_c = round(e_c / p_c * 100, 2) if p_c > 0 else 0
                            color_c = COLOR_CLAS.get(clas_sel, "#185FA5")
                            st.plotly_chart(
                                make_gauge(t_c, clas_sel, color=color_c, height=240, font_size=40),
                                use_container_width=True,
                                config={"displayModeBar": False},
                            )
                            st.caption(f"Ejecutado: **{fmt_cop(e_c)}** / Programado: **{fmt_cop(p_c)}**")
                        else:
                            st.info(f"Sin datos para {clas_sel}.")

                    # ── Impuesto principal (gauge individual) ──────────────────
                    with col_imp:
                        st.markdown("### Impuestos Principales")
                        opciones_imp_mun = [
                            "Impuesto predial unificado",
                            "Impuesto de industria y comercio",
                            "Sobretasa a la gasolina",
                            "Estampillas",
                        ]
                        imp_sel = st.selectbox(
                            "Selecciona un impuesto",
                            opciones_imp_mun,
                            key="ing_imp_mun",
                        )
                        # Máscara flexible según el impuesto
                        if "predial" in imp_sel.lower():
                            mask = ofpuj["clas_ofpuj"].str.contains("predial", case=False, na=False)
                        elif "industria" in imp_sel.lower() or "comercio" in imp_sel.lower():
                            mask = ofpuj["clas_ofpuj"].str.contains("industria|comercio|ICA", case=False, na=False)
                        else:
                            mask = ofpuj["clas_ofpuj"].str.contains(imp_sel, case=False, na=False)

                        df_imp = ofpuj[(ofpuj["Entidad"] == entidad_sel) & mask]
                        if not df_imp.empty:
                            p_i = df_imp["Total_Programado"].sum()
                            e_i = df_imp["Total_Ejecutado"].sum()
                            t_i = round(e_i / p_i * 100, 2) if p_i > 0 else 0
                            color_i = COLOR_IMP.get(imp_sel, "#185FA5")
                            st.plotly_chart(
                                make_gauge(t_i, imp_sel, color=color_i, height=240, font_size=40),
                                use_container_width=True,
                                config={"displayModeBar": False},
                            )
                            st.caption(f"Ejecutado: **{fmt_cop(e_i)}** / Programado: **{fmt_cop(p_i)}**")
                        else:
                            st.info(f"Sin datos para {imp_sel}.")

                    st.divider()
                    with st.expander("Ver tabla de detalle completa"):
                        st.dataframe(tabla[tabla["Entidad"] == entidad_sel], use_container_width=True)

        # =========================================================================
        # TAB GASTOS 2025
        # =========================================================================
        with tab_gas:
            st.header("Coyuntura de Gastos 2025")
        
            base_dir  = Path(__file__).parent
            ejec_path = base_dir / "eje_gast_clean25.xlsx"
            prog_path = base_dir / "pro_gast_clean25.xlsx"

            @st.cache_data
            def cargar_gastos():
                df_eg = pd.read_excel(ejec_path)
                df_pg = pd.read_excel(prog_path)
                for df in [df_eg, df_pg]:
                    df["Entidad"]         = df["Entidad"].astype(str).str.strip()
                    df["Tipo de Entidad"] = df["Tipo de Entidad"].astype(str).str.strip()
                    df["Departamento"]    = df["Departamento"].astype(str).str.strip()
                return df_eg, df_pg

            df_ejec_g, df_prog_g = cargar_gastos()

            group_cols = ["Entidad", "Tipo de Entidad", "Departamento"]
            ejec_agg_g = (df_ejec_g.groupby(group_cols, as_index=False)["Obligaciones"]
                                .sum().rename(columns={"Obligaciones": "Total_Ejecutado"}))
            prog_agg_g = (df_prog_g.groupby(group_cols, as_index=False)["Apropiación Definitiva"]
                                .sum().rename(columns={"Apropiación Definitiva": "Total_Programado"}))
            tabla_g = pd.merge(prog_agg_g, ejec_agg_g, on=group_cols, how="left")
            tabla_g["Total_Ejecutado"]    = tabla_g["Total_Ejecutado"].fillna(0)
            tabla_g["Tasa_Ejecución (%)"] = ((tabla_g["Total_Ejecutado"] / tabla_g["Total_Programado"]) * 100).round(2).fillna(0)

            p_gen_g, e_gen_g, t_gen_g = tasas(tabla_g)
            p_dep_g, e_dep_g, t_dep_g = tasas(tabla_g[tabla_g["Tipo de Entidad"] == "Departamento"])
            p_mun_g, e_mun_g, t_mun_g = tasas(tabla_g[tabla_g["Tipo de Entidad"] == "Municipio"])

            tab1g, tab2g, tab3g = st.tabs(["General", "Departamental", "Municipal"])

            # ------------------------------------------------------------------
            # GASTOS – TAB GENERAL
            # ------------------------------------------------------------------
            with tab1g:
                st.subheader("Ejecución Acumulada General de Gastos")
                col1, col2, col3 = st.columns(3)
                for col, tasa, prog, ejec, titulo in [
                    (col1, t_gen_g, p_gen_g, e_gen_g, "Nacional"),
                    (col2, t_dep_g, p_dep_g, e_dep_g, "Departamentos"),
                    (col3, t_mun_g, p_mun_g, e_mun_g, "Municipios"),
                ]:
                    with col:
                        st.plotly_chart(
                            make_gauge(tasa, titulo),
                            use_container_width=True,
                            config={"displayModeBar": False},
                        )
                        st.caption(f"**Obligaciones / Apropiación:** {fmt_cop(ejec)} / {fmt_cop(prog)}")

            # ------------------------------------------------------------------
            # GASTOS – TAB DEPARTAMENTAL
            # ------------------------------------------------------------------
            with tab2g:
                st.subheader("Nivel Departamental")
                df_dep_g = tabla_g[tabla_g["Tipo de Entidad"] == "Departamento"].copy()
                if not df_dep_g.empty:
                    entidad_sel = st.selectbox(
                        "Selecciona Departamento",
                        sorted(df_dep_g["Entidad"].unique()),
                        key="gasto_dep_sel",
                    )
                    row = df_dep_g[df_dep_g["Entidad"] == entidad_sel].iloc[0]
                    col_gauge, col_info = st.columns([1.4, 1])
                    with col_gauge:
                        st.plotly_chart(
                            make_gauge(row["Tasa_Ejecución (%)"],
                                    "Tasa de ejecución",
                                    subtitle=f"Acumulado 2025 · {entidad_sel}"),
                            use_container_width=True,
                            config={"displayModeBar": False},
                        )
                    with col_info:
                        st.markdown(tarjeta_metrica("Programado",           fmt_cop(row["Total_Programado"]),                     "#185FA5"), unsafe_allow_html=True)
                        st.markdown(tarjeta_metrica("Ejecutado (Obl.)",     fmt_cop(row["Total_Ejecutado"]),                      "#1D9E75"), unsafe_allow_html=True)
                        st.markdown(tarjeta_metrica("Por Ejecutar",         fmt_cop(row["Total_Programado"] - row["Total_Ejecutado"]), "#D85A30"), unsafe_allow_html=True)

            # ------------------------------------------------------------------
            # GASTOS – TAB MUNICIPAL
            # ------------------------------------------------------------------
            with tab3g:
                st.subheader("Nivel Municipal")
                df_mun_g = tabla_g[tabla_g["Tipo de Entidad"] == "Municipio"].copy()
                if not df_mun_g.empty:
                    depto_sel = st.selectbox(
                        "Selecciona Departamento",
                        sorted(df_mun_g["Departamento"].unique()),
                        key="gasto_mun_depto",
                    )
                    muns_g    = sorted(df_mun_g[df_mun_g["Departamento"] == depto_sel]["Entidad"].unique())
                    entidad_sel = st.selectbox("Selecciona Municipio", muns_g, key="gasto_mun_sel")
                    row = df_mun_g[df_mun_g["Entidad"] == entidad_sel].iloc[0]
                    col_gauge, col_info = st.columns([1.4, 1])
                    with col_gauge:
                        st.plotly_chart(
                            make_gauge(row["Tasa_Ejecución (%)"],
                                    "Tasa de ejecución",
                                    subtitle=f"Acumulado 2025 · {entidad_sel}"),
                            use_container_width=True,
                            config={"displayModeBar": False},
                        )
                    with col_info:
                        st.markdown(tarjeta_metrica("Programado",       fmt_cop(row["Total_Programado"]),                     "#185FA5"), unsafe_allow_html=True)
                        st.markdown(tarjeta_metrica("Ejecutado (Obl.)", fmt_cop(row["Total_Ejecutado"]),                      "#1D9E75"), unsafe_allow_html=True)
                        st.markdown(tarjeta_metrica("Por Ejecutar",     fmt_cop(row["Total_Programado"] - row["Total_Ejecutado"]), "#D85A30"), unsafe_allow_html=True)
        
    
##treemap
elif menu == "Treemap":
           
    st.header("Treemap")

# =============================================================================
# PRESUPUESTO ACTUAL — reemplazo del bloque elif menu == "Presupuesto actual"
# =============================================================================

elif menu == "Presupuesto actual":
    st.header("Presupuesto actual 2025")

    # -------------------------------------------------------------------------
    # Carga de datos
    # -------------------------------------------------------------------------
    DATOS_LISTOS = False  # ← cambiar a True cuando el CIFFIT actualice

    if not DATOS_LISTOS:
        st.info(" Esperando actualización del CIFFIT.")
    else:
        base_dir  = Path(__file__).parent

        @st.cache_data
        def cargar_presupuesto():
            df_ing  = pd.read_excel(base_dir / "pro_ing_clean25.xlsx")
            df_gast = pd.read_excel(base_dir / "pro_gast_clean25.xlsx")

            for df in [df_ing, df_gast]:
                df["Entidad"]         = df["Entidad"].astype(str).str.strip()
                df["Tipo de Entidad"] = df["Tipo de Entidad"].astype(str).str.strip()
                df["Departamento"]    = df["Departamento"].astype(str).str.strip()

            return df_ing, df_gast

        df_ing, df_gast = cargar_presupuesto()

        # -------------------------------------------------------------------------
        # Helpers
        # -------------------------------------------------------------------------
        def fmt_cop(n):
            """Formato COP legible."""
            if n >= 1e12: return f"${n/1e12:.2f} B"
            if n >= 1e9:  return f"${n/1e9:.1f} MM"
            return f"${n/1e6:.0f} M"

        def limpiar_path(df, cols):
            """
            Para treemaps: propaga hacia adelante los valores de la jerarquía
            y descarta filas completamente vacías en la primera columna del path.
            """
            df = df.copy()
            df[cols[0]] = df[cols[0]].fillna("Sin clasificar")
            for i in range(1, len(cols)):
                df[cols[i]] = df[cols[i]].fillna(df[cols[i - 1]])
            return df

        def estilo_treemap(fig):
            """Estética uniforme para todos los treemaps."""
            fig.update_layout(margin=dict(t=30, l=10, r=10, b=10))
            fig.update_traces(
                textinfo="label+percent entry",
                textfont=dict(size=14, color="white"),
                marker=dict(line=dict(width=3, color="white")),
            )
            return fig

        def metrica_total(df, col_valor, label):
            total = df[col_valor].sum()
            st.metric(label, fmt_cop(total))

        # =========================================================================
        # TABS PRINCIPALES: Ingresos | Gastos
        # =========================================================================
        tab_ing_p, tab_gast_p = st.tabs([" Ingresos 2025", "Gastos 2025"])

        # =========================================================================
        # INGRESOS 2025
        # =========================================================================
        with tab_ing_p:
            st.subheader("Programación de Ingresos 2025")

            PATH_ING  = ["clas_ofpuj", "clas_gen1", "clas_gen2"]
            COL_VAL_I = "Presupuesto Definitivo"

            # Limpiar columnas de path
            df_ing_clean = limpiar_path(df_ing, PATH_ING)
            df_ing_clean["valor_mm"] = df_ing_clean[COL_VAL_I] / 1_000_000_000

            # Sub-tabs territoriales
            t_dep_i, t_mun_i = st.tabs(["Departamental", "Municipal"])

            # ------------------------------------------------------------------
            # INGRESOS – DEPARTAMENTAL
            # ------------------------------------------------------------------
            with t_dep_i:
                df_dep_i = df_ing_clean[
                    df_ing_clean["Tipo de Entidad"] == "Departamento"
                ].copy()

                deptos_i = sorted(df_dep_i["Departamento"].dropna().unique())
                depto_sel_i = st.selectbox(
                    "Selecciona un Departamento",
                    deptos_i,
                    key="pres_ing_depto"
                )

                df_fil_di = df_dep_i[df_dep_i["Departamento"] == depto_sel_i]

                if df_fil_di.empty:
                    st.warning("Sin datos para este departamento.")
                else:
                    metrica_total(df_fil_di, "valor_mm", f"Total Presupuesto · {depto_sel_i}")

                    fig_i_dep = px.treemap(
                        df_fil_di,
                        path=PATH_ING,
                        values="valor_mm",
                        title=f"Composición del presupuesto de ingresos — {depto_sel_i}",
                        color="clas_ofpuj",
                    )
                    st.plotly_chart(
                        estilo_treemap(fig_i_dep),
                        use_container_width=True,
                        key="treemap_pres_ing_dep"
                    )

            # ------------------------------------------------------------------
            # INGRESOS – MUNICIPAL
            # ------------------------------------------------------------------
            with t_mun_i:
                df_mun_i = df_ing_clean[
                    df_ing_clean["Tipo de Entidad"] == "Municipio"
                ].copy()

                deptos_mi = sorted(df_mun_i["Departamento"].dropna().unique())
                depto_sel_mi = st.selectbox(
                    "Selecciona un Departamento",
                    deptos_mi,
                    key="pres_ing_mun_depto"
                )

                muns_i = sorted(
                    df_mun_i[df_mun_i["Departamento"] == depto_sel_mi]["Entidad"]
                    .dropna().unique()
                )
                mun_sel_i = st.selectbox(
                    "Selecciona un Municipio",
                    muns_i,
                    key="pres_ing_mun_ent"
                )

                df_fil_mi = df_mun_i[df_mun_i["Entidad"] == mun_sel_i]

                if df_fil_mi.empty:
                    st.warning("Sin datos para este municipio.")
                else:
                    metrica_total(df_fil_mi, "valor_mm", f"Total Presupuesto · {mun_sel_i}")

                    fig_i_mun = px.treemap(
                        df_fil_mi,
                        path=PATH_ING,
                        values="valor_mm",
                        title=f"Composición del presupuesto de ingresos — {mun_sel_i}",
                        color="clas_ofpuj",
                    )
                    st.plotly_chart(
                        estilo_treemap(fig_i_mun),
                        use_container_width=True,
                        key="treemap_pres_ing_mun"
                    )

        # =========================================================================
        # GASTOS 2025
        # =========================================================================
        with tab_gast_p:
            st.subheader("Programación de Gastos 2025")

            # Definir columnas de profundidad disponibles en gastos
            # col_1 existe solo en gastos; se usa como raíz de la jerarquía
            COLS_GASTO_RAW = ["col_1", "col_2", "col_3", "col_4", "col_5", "col_6"]
            COL_VAL_G = "Apropiación Definitiva"

            # Detectar cuáles columnas de path realmente existen en el archivo
            PATH_GAST = [c for c in COLS_GASTO_RAW if c in df_gast.columns]

            df_gast_clean = limpiar_path(df_gast, PATH_GAST)
            df_gast_clean["valor_mm"] = df_gast_clean[COL_VAL_G] / 1_000_000_000

            # Sub-tabs territoriales
            t_dep_g, t_mun_g = st.tabs(["Departamental", "Municipal"])

            # ------------------------------------------------------------------
            # GASTOS – DEPARTAMENTAL
            # ------------------------------------------------------------------
            with t_dep_g:
                df_dep_g = df_gast_clean[
                    df_gast_clean["Tipo de Entidad"] == "Departamento"
                ].copy()

                deptos_g = sorted(df_dep_g["Departamento"].dropna().unique())
                depto_sel_g = st.selectbox(
                    "Selecciona un Departamento",
                    deptos_g,
                    key="pres_gast_depto"
                )

                df_fil_dg = df_dep_g[df_dep_g["Departamento"] == depto_sel_g]

                if df_fil_dg.empty:
                    st.warning("Sin datos para este departamento.")
                else:
                    metrica_total(df_fil_dg, "valor_mm", f"Total Apropiación · {depto_sel_g}")

                    fig_g_dep = px.treemap(
                        df_fil_dg,
                        path=PATH_GAST,
                        values="valor_mm",
                        title=f"Composición del presupuesto de gastos — {depto_sel_g}",
                        color="col_1",
                    )
                    st.plotly_chart(
                        estilo_treemap(fig_g_dep),
                        use_container_width=True,
                        key="treemap_pres_gast_dep"
                    )

            # ------------------------------------------------------------------
            # GASTOS – MUNICIPAL
            # ------------------------------------------------------------------
            with t_mun_g:
                df_mun_g = df_gast_clean[
                    df_gast_clean["Tipo de Entidad"] == "Municipio"
                ].copy()

                deptos_mg = sorted(df_mun_g["Departamento"].dropna().unique())
                depto_sel_mg = st.selectbox(
                    "Selecciona un Departamento",
                    deptos_mg,
                    key="pres_gast_mun_depto"
                )

                muns_g = sorted(
                    df_mun_g[df_mun_g["Departamento"] == depto_sel_mg]["Entidad"]
                    .dropna().unique()
                )
                mun_sel_g = st.selectbox(
                    "Selecciona un Municipio",
                    muns_g,
                    key="pres_gast_mun_ent"
                )

                df_fil_mg = df_mun_g[df_mun_g["Entidad"] == mun_sel_g]

                if df_fil_mg.empty:
                    st.warning("Sin datos para este municipio.")
                else:
                    metrica_total(df_fil_mg, "valor_mm", f"Total Apropiación · {mun_sel_g}")

                    fig_g_mun = px.treemap(
                        df_fil_mg,
                        path=PATH_GAST,
                        values="valor_mm",
                        title=f"Composición del presupuesto de gastos — {mun_sel_g}",
                        color="col_1",
                    )
                    st.plotly_chart(
                        estilo_treemap(fig_g_mun),
                        use_container_width=True,
                        key="treemap_pres_gast_mun"
                    )

#Descargas
elif menu == "Descarga de datos":
    st.header("Descarga de datos")

    base_dir = Path(__file__).parent

    @st.cache_data
    def convertir_xlsx(ruta_parquet):
        df = pd.read_parquet(ruta_parquet)
        buffer = BytesIO()
        df.to_excel(buffer, index=False, engine="openpyxl")
        buffer.seek(0)
        return buffer.getvalue()

    datasets = [
        {
            "titulo":   "Ingresos territoriales",
            "archivo":  base_dir / "data" / "ingresos_ipc_pop.parquet",
            "nombre":   "ingresos_ipc_pop.xlsx",
            "boton":    "Descargar datos completos (xlsx)",
        },
        {
            "titulo":   "Gastos territoriales",
            "archivo":  base_dir / "data" / "ejecucion_deflactada_mun.parquet",
            "nombre":   "ejecucion_deflactada_mun.xlsx",
            "boton":    "Descargar datos completos (xlsx)",
        },
        {
            "titulo":   "Sistema General de Participaciones (SGP)",
            "archivo":  base_dir / "data" / "datos_sgp_pib_ic.parquet",
            "nombre":   "datos_sgp_pib_ic.xlsx",
            "boton":    "Descargar datos completos (xlsx)",
        },
    ]

    for ds in datasets:
        st.subheader(ds["titulo"])
        if ds["archivo"].exists():
            datos_xlsx = convertir_xlsx(ds["archivo"])
            st.download_button(
                label=ds["boton"],
                data=datos_xlsx,
                file_name=ds["nombre"],
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=ds["nombre"],
            )
        else:
            st.warning(f"Archivo no disponible: {ds['archivo'].name}")
        st.divider()