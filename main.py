##PEPE TERRITORIAL
# Cargar librerias
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from streamlit_option_menu import option_menu
import plotly.graph_objects as go


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
# Coyuntura 
# =============================================================================

elif menu == "Coyuntura":
    st.header("Coyuntura - Ejecución de Ingresos 2025")
    
    # ====================== CARGA DE DATOS ======================
    base_dir = Path(__file__).parent
    ejec_path = base_dir / "eje_ing_clean25.xlsx"
    prog_path = base_dir / "pro_ing_clean25.xlsx"
    
    @st.cache_data
    def cargar_datos():
        df_ejec = pd.read_excel(ejec_path)
        df_prog = pd.read_excel(prog_path)
        return df_ejec, df_prog

    df_ejec, df_prog = cargar_datos()

    # Limpieza
    for df in [df_ejec, df_prog]:
        df['Entidad'] = df['Entidad'].astype(str).str.strip()
        df['Tipo de Entidad'] = df['Tipo de Entidad'].astype(str).str.strip()
        df['Departamento'] = df['Departamento'].astype(str).str.strip()

    # ====================== TOTAL POR ENTIDAD ======================
    group_cols = ['Entidad', 'Tipo de Entidad', 'Departamento']
    ejec_agg = (df_ejec.groupby(group_cols, as_index=False)['Total Recaudo'].sum().rename(columns={'Total Recaudo': 'Total_Ejecutado'}))
    prog_agg = (df_prog.groupby(group_cols, as_index=False)['Presupuesto Definitivo'].sum().rename(columns={'Presupuesto Definitivo': 'Total_Programado'}))
    tabla_consolidada = pd.merge(prog_agg, ejec_agg, on=group_cols, how='left')
    tabla_consolidada['Total_Ejecutado'] = tabla_consolidada['Total_Ejecutado'].fillna(0)
    tabla_consolidada['Tasa_Ejecución (%)'] = ((tabla_consolidada['Total_Ejecutado'] / tabla_consolidada['Total_Programado']) * 100).round(2).fillna(0)

    # ====================== TOTALES GENERALES ======================
    total_gen  = tabla_consolidada.agg({'Total_Programado': 'sum', 'Total_Ejecutado': 'sum'})
    total_dept = tabla_consolidada[tabla_consolidada['Tipo de Entidad'] == "Departamento"].agg({'Total_Programado': 'sum', 'Total_Ejecutado': 'sum'})
    total_mun  = tabla_consolidada[tabla_consolidada['Tipo de Entidad'] == "Municipio"].agg({'Total_Programado': 'sum', 'Total_Ejecutado': 'sum'})

    tasa_gen  = (total_gen['Total_Ejecutado'] / total_gen['Total_Programado'] * 100).round(2) if total_gen['Total_Programado'] > 0 else 0
    tasa_dept = (total_dept['Total_Ejecutado'] / total_dept['Total_Programado'] * 100).round(2) if total_dept['Total_Programado'] > 0 else 0
    tasa_mun  = (total_mun['Total_Ejecutado'] / total_mun['Total_Programado'] * 100).round(2) if total_mun['Total_Programado'] > 0 else 0

    # ====================== DETALLE CLAS_GEN2 ======================
    detailed_group = ['Entidad', 'Tipo de Entidad', 'Departamento', 'clas_gen2']
    ejec_detail = (df_ejec.groupby(detailed_group, as_index=False)['Total Recaudo'].sum().rename(columns={'Total Recaudo': 'Total_Ejecutado'}))
    prog_detail = (df_prog.groupby(detailed_group, as_index=False)['Presupuesto Definitivo'].sum().rename(columns={'Presupuesto Definitivo': 'Total_Programado'}))
    detail_consolidada = pd.merge(prog_detail, ejec_detail, on=detailed_group, how='left')
    detail_consolidada['Total_Ejecutado'] = detail_consolidada['Total_Ejecutado'].fillna(0)
    detail_consolidada['Tasa_Ejecución (%)'] = ((detail_consolidada['Total_Ejecutado'] / detail_consolidada['Total_Programado']) * 100).round(2).fillna(0)

    # ====================== DETALLE CLAS_OFPUJ (CORREGIDO) ======================
    ofpuj_group = ['Entidad', 'Tipo de Entidad', 'Departamento', 'clas_ofpuj']
    ejec_ofpuj = (df_ejec.groupby(ofpuj_group, as_index=False)['Total Recaudo'].sum().rename(columns={'Total Recaudo': 'Total_Ejecutado'}))
    prog_ofpuj = (df_prog.groupby(ofpuj_group, as_index=False)['Presupuesto Definitivo'].sum().rename(columns={'Presupuesto Definitivo': 'Total_Programado'}))
    ofpuj_consolidada = pd.merge(prog_ofpuj, ejec_ofpuj, on=ofpuj_group, how='left')
    ofpuj_consolidada['Total_Ejecutado'] = ofpuj_consolidada['Total_Ejecutado'].fillna(0)
    ofpuj_consolidada['Tasa_Ejecución (%)'] = ((ofpuj_consolidada['Total_Ejecutado'] / ofpuj_consolidada['Total_Programado']) * 100).round(2).fillna(0)

    # ====================== HELPERS ======================
    def fmt_cop(n):
        if n >= 1e12: return f"${n/1e12:.2f} B"
        if n >= 1e9: return f"${n/1e9:.1f} MM"
        return f"${n/1e6:.0f} M"

    def tarjeta_metrica(label, valor_cop, color_valor):
        return f"""
        <div style="background:#F1EFE8; border-radius:12px; padding:14px 18px; margin-bottom:10px; border-left:4px solid {color_valor};">
            <div style="font-size:11px; font-weight:600; color:#888780; letter-spacing:.06em; text-transform:uppercase; margin-bottom:4px;">{label}</div>
            <div style="font-size:22px; font-weight:600; color:{color_valor}; font-family:'Inter',sans-serif;">{valor_cop}</div>
        </div>
        """

    COLOR_CLAS = {"Recursos propios": "#185FA5", "Transferencias": "#0F6E56", "Recursos de capital": "#BA7517"}
    COLOR_POR_IMPUESTO = {
        "Estampillas": "#534AB7",
        "Sobretasa a la gasolina": "#0F6E56",
        "Impuesto predial unificado": "#185FA5",
        "Impuesto de industria y comercio": "#BA7517"
    }

    tab1, tab2, tab3 = st.tabs(["General", "Departamental", "Municipal"])

# ====================== TAB GENERAL ======================
    with tab1:
        st.subheader("Ejecución Acumulada General")
        col1, col2, col3 = st.columns(3)

        # Total General
        with col1:
            tasa = tasa_gen
            prog = total_gen['Total_Programado']
            ejec = total_gen['Total_Ejecutado']
            st.metric("**Total General**", f"{tasa:.1f}%", f"{fmt_cop(ejec)} / {fmt_cop(prog)}")
            fig_gen = go.Figure(go.Indicator(
                mode="gauge+number",
                value=tasa,
                number={"suffix": "%", "font": {"size": 52, "color": "#1a1a2e"}},
                gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#185FA5", "thickness": 0.28},
                       "steps": [{"range": [0, 40], "color": "#FCEBEB"}, {"range": [40, 70], "color": "#FAEEDA"}, {"range": [70, 100], "color": "#EAF3DE"}]},
                title={"text": "Nacional"}
            ))
            st.plotly_chart(fig_gen, use_container_width=True, config={"displayModeBar": False})
            st.caption("**Ejecutado / Programado**")
            st.divider()


            # Diferencia solicitada
            if tasa > 100:
                sob = tasa - 100
                mon = ejec - prog
                st.metric("**Sobreejecución**", f"+{sob:.1f}%", f"+{fmt_cop(mon)}", delta_color="normal")
            else:
                falta = 100 - tasa
                mon_falta = prog - ejec
                st.metric("**Falta por ejecutar**", f"{falta:.1f}%", f"{fmt_cop(mon_falta)} restantes", delta_color="inverse")

        # Departamentos
        with col2:
            tasa = tasa_dept
            prog = total_dept['Total_Programado']
            ejec = total_dept['Total_Ejecutado']
            st.metric("**Departamentos**", f"{tasa:.1f}%", f"{fmt_cop(ejec)} / {fmt_cop(prog)}")
            fig_dep = go.Figure(go.Indicator(
                mode="gauge+number",
                value=tasa,
                number={"suffix": "%", "font": {"size": 52, "color": "#1a1a2e"}},
                gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#185FA5", "thickness": 0.28},
                       "steps": [{"range": [0, 40], "color": "#FCEBEB"}, {"range": [40, 70], "color": "#FAEEDA"}, {"range": [70, 100], "color": "#EAF3DE"}]},
                title={"text": "Todos los Departamentos"}
            ))
            st.plotly_chart(fig_dep, use_container_width=True, config={"displayModeBar": False})
            st.caption("**Ejecutado / Programado**")
            st.divider()


            if tasa > 100:
                sob = tasa - 100
                mon = ejec - prog
                st.metric("**Sobreejecución**", f"+{sob:.1f}%", f"+{fmt_cop(mon)}", delta_color="normal")
            else:
                falta = 100 - tasa
                mon_falta = prog - ejec
                st.metric("**Falta por ejecutar**", f"{falta:.1f}%", f"{fmt_cop(mon_falta)} restantes", delta_color="inverse")

        # Municipios
        with col3:
            tasa = tasa_mun
            prog = total_mun['Total_Programado']
            ejec = total_mun['Total_Ejecutado']
            st.metric("**Municipios**", f"{tasa:.1f}%", f"{fmt_cop(ejec)} / {fmt_cop(prog)}")
            fig_mun = go.Figure(go.Indicator(
                mode="gauge+number",
                value=tasa,
                number={"suffix": "%", "font": {"size": 52, "color": "#1a1a2e"}},
                gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#185FA5", "thickness": 0.28},
                       "steps": [{"range": [0, 40], "color": "#FCEBEB"}, {"range": [40, 70], "color": "#FAEEDA"}, {"range": [70, 100], "color": "#EAF3DE"}]},
                title={"text": "Todos los Municipios"}
            ))
            st.plotly_chart(fig_mun, use_container_width=True, config={"displayModeBar": False})
            st.caption("**Ejecutado / Programado**")
            st.divider()


            if tasa > 100:
                sob = tasa - 100
                mon = ejec - prog
                st.metric("**Sobreejecución**", f"+{sob:.1f}%", f"+{fmt_cop(mon)}", delta_color="normal")
            else:
                falta = 100 - tasa
                mon_falta = prog - ejec
                st.metric("**Falta por ejecutar**", f"{falta:.1f}%", f"{fmt_cop(mon_falta)} restantes", delta_color="inverse")

    # ====================== TAB DEPARTAMENTAL ======================
    with tab2:
        st.subheader("Nivel Departamental")
        df_dep = tabla_consolidada[tabla_consolidada['Tipo de Entidad'] == "Departamento"].copy()
        if not df_dep.empty:
            entidad_sel = st.selectbox("Selecciona Departamento", sorted(df_dep['Entidad'].unique()), key="dep_sel")
            df_e = df_dep[df_dep['Entidad'] == entidad_sel].iloc[0]
            tasa = df_e['Tasa_Ejecución (%)']
            prog = df_e['Total_Programado']
            ejec = df_e['Total_Ejecutado']

            # ZONA 1
            col_gauge, col_metrics = st.columns([1.4, 1])
            with col_gauge:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=tasa,
                    number={"suffix": "%", "font": {"size": 52, "color": "#1a1a2e", "family": "Inter, sans-serif"}},
                    gauge={"axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#888780", "tickfont": {"size": 11}, "dtick": 20},
                           "bar": {"color": "#185FA5", "thickness": 0.28},
                           "bgcolor": "white", "borderwidth": 0,
                           "steps": [{"range": [0, 40], "color": "#FCEBEB"}, {"range": [40, 70], "color": "#FAEEDA"}, {"range": [70, 100], "color": "#EAF3DE"}],
                           "threshold": {"line": {"color": "#D85A30", "width": 3}, "thickness": 0.85, "value": 58.3}},
                    title={"text": f"Tasa de ejecución total<br><span style='font-size:13px;color:#888780'>Acumulado 2025 · {entidad_sel}</span>", "font": {"size": 17, "color": "#1a1a2e", "family": "Inter, sans-serif"}}
                ))
                fig.update_layout(height=280, margin=dict(t=60, b=10, l=20, r=20), paper_bgcolor="white", font_family="Inter, sans-serif")
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

                st.caption("**Ejecutado / Programado**")

            with col_metrics:
                st.markdown(tarjeta_metrica("Programado", fmt_cop(prog), "#185FA5"), unsafe_allow_html=True)
                st.markdown(tarjeta_metrica("Ejecutado", fmt_cop(ejec), "#1D9E75"), unsafe_allow_html=True)
                st.markdown(tarjeta_metrica("Rezago", fmt_cop(prog - ejec), "#D85A30"), unsafe_allow_html=True)

            st.divider()

            # ZONA 2
            col_clas, col_imp = st.columns([1, 1])
            with col_clas:
                st.markdown("### Ejecución por Clasificación (clas_gen2)")
                opciones_clas = ['Recursos propios', 'Transferencias', 'Recursos de capital']
                seleccion_clas = st.multiselect("Selecciona qué clasificaciones mostrar", opciones_clas, default=opciones_clas, key="clas_dep")
                for clas in seleccion_clas:
                    df_clas = detail_consolidada[(detail_consolidada['Entidad'] == entidad_sel) & (detail_consolidada['clas_gen2'] == clas)].copy()
                    if not df_clas.empty:
                        prog_clas = df_clas['Total_Programado'].sum()
                        ejec_clas = df_clas['Total_Ejecutado'].sum()
                        tasa_clas = (ejec_clas / prog_clas * 100).round(2) if prog_clas > 0 else 0
                        st.markdown(f"**{clas}** — {tasa_clas:.1f}%")
                        st.progress(min(tasa_clas / 100, 1.0))
                        st.caption(f"Ejecutado: {fmt_cop(ejec_clas)} / {fmt_cop(prog_clas)}")
                        st.markdown("---")

            with col_imp:
                st.markdown("### Impuestos Principales")
                opciones_imp_dep = ["Estampillas", "Sobretasa a la gasolina"]
                seleccion_imp = st.multiselect("Selecciona qué impuestos mostrar", opciones_imp_dep, default=opciones_imp_dep, key="imp_dep")
                cols_imp = st.columns(len(seleccion_imp))
                for i, imp in enumerate(seleccion_imp):
                    mask = ofpuj_consolidada['clas_ofpuj'].str.contains(imp, case=False, na=False)
                    df_imp = ofpuj_consolidada[(ofpuj_consolidada['Entidad'] == entidad_sel) & mask].copy()
                    if not df_imp.empty:
                        prog_imp = df_imp['Total_Programado'].sum()
                        ejec_imp = df_imp['Total_Ejecutado'].sum()
                        tasa_imp = (ejec_imp / prog_imp * 100).round(2) if prog_imp > 0 else 0
                        with cols_imp[i]:
                            fig_mini = go.Figure(go.Indicator(
                                mode="gauge+number",
                                value=tasa_imp,
                                number={"suffix": "%", "font": {"size": 28, "color": "#1a1a2e"}},
                                gauge={"axis": {"range": [0, 100], "visible": False}, "bar": {"color": COLOR_POR_IMPUESTO.get(imp, "#185FA5"), "thickness": 0.3}, "bgcolor": "#F1EFE8", "borderwidth": 0},
                                title={"text": imp, "font": {"size": 13, "color": "#5F5E5A"}}
                            ))
                            fig_mini.update_layout(height=180, margin=dict(t=40, b=20, l=10, r=10), paper_bgcolor="white")
                            st.plotly_chart(fig_mini, use_container_width=True, config={"displayModeBar": False})
                            st.caption(f"{fmt_cop(ejec_imp)} / {fmt_cop(prog_imp)}")

            st.divider()

            with st.expander("Ver tabla de detalle completa"):
                st.dataframe(tabla_consolidada[tabla_consolidada['Entidad'] == entidad_sel], use_container_width=True)

    # ====================== TAB MUNICIPAL ======================
    with tab3:
        st.subheader("Nivel Municipal")
        df_mun = tabla_consolidada[tabla_consolidada['Tipo de Entidad'] == "Municipio"].copy()
        if not df_mun.empty:
            departamentos = sorted(df_mun['Departamento'].unique())
            depto_sel = st.selectbox("Selecciona un Departamento", departamentos, key="mun_depto_sel")
            municipios_filtrados = sorted(df_mun[df_mun['Departamento'] == depto_sel]['Entidad'].unique())
            entidad_sel = st.selectbox("Selecciona un Municipio", municipios_filtrados, key="mun_sel")
            df_e = df_mun[df_mun['Entidad'] == entidad_sel].iloc[0]
            tasa = df_e['Tasa_Ejecución (%)']
            prog = df_e['Total_Programado']
            ejec = df_e['Total_Ejecutado']

            # ZONA 1
            col_gauge, col_metrics = st.columns([1.4, 1])
            with col_gauge:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=tasa,
                    number={"suffix": "%", "font": {"size": 52, "color": "#1a1a2e", "family": "Inter, sans-serif"}},
                    gauge={"axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#888780", "tickfont": {"size": 11}, "dtick": 20},
                           "bar": {"color": "#185FA5", "thickness": 0.28},
                           "bgcolor": "white", "borderwidth": 0,
                           "steps": [{"range": [0, 40], "color": "#FCEBEB"}, {"range": [40, 70], "color": "#FAEEDA"}, {"range": [70, 100], "color": "#EAF3DE"}],
                           "threshold": {"line": {"color": "#D85A30", "width": 3}, "thickness": 0.85, "value": 58.3}},
                    title={"text": f"Tasa de ejecución total<br><span style='font-size:13px;color:#888780'>Acumulado 2025 · {entidad_sel}</span>", "font": {"size": 17, "color": "#1a1a2e", "family": "Inter, sans-serif"}}
                ))
                fig.update_layout(height=280, margin=dict(t=60, b=10, l=20, r=20), paper_bgcolor="white", font_family="Inter, sans-serif")
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

            with col_metrics:
                st.markdown(tarjeta_metrica("Programado", fmt_cop(prog), "#185FA5"), unsafe_allow_html=True)
                st.markdown(tarjeta_metrica("Ejecutado", fmt_cop(ejec), "#1D9E75"), unsafe_allow_html=True)
                st.markdown(tarjeta_metrica("Rezago", fmt_cop(prog - ejec), "#D85A30"), unsafe_allow_html=True)
                st.caption("**Ejecutado / Programado**")


            st.divider()

            # ZONA 2
            col_clas, col_imp = st.columns([1, 1])
            with col_clas:
                st.markdown("### Ejecución por Clasificación (clas_gen2)")
                opciones_clas = ['Recursos propios', 'Transferencias', 'Recursos de capital']
                seleccion_clas = st.multiselect("Selecciona qué clasificaciones mostrar", opciones_clas, default=opciones_clas, key="clas_mun")
                for clas in seleccion_clas:
                    df_clas = detail_consolidada[(detail_consolidada['Entidad'] == entidad_sel) & (detail_consolidada['clas_gen2'] == clas)].copy()
                    if not df_clas.empty:
                        prog_clas = df_clas['Total_Programado'].sum()
                        ejec_clas = df_clas['Total_Ejecutado'].sum()
                        tasa_clas = (ejec_clas / prog_clas * 100).round(2) if prog_clas > 0 else 0
                        st.markdown(f"**{clas}** — {tasa_clas:.1f}%")
                        st.progress(min(tasa_clas / 100, 1.0))
                        st.caption(f"Ejecutado: {fmt_cop(ejec_clas)} / {fmt_cop(prog_clas)}")
                        st.markdown("---")

            with col_imp:
                st.markdown("### Impuestos Principales")
                opciones_imp_mun = ["Impuesto predial unificado", "Impuesto de industria y comercio", "Sobretasa a la gasolina", "Estampillas"]
                seleccion_imp = st.multiselect("Selecciona qué impuestos mostrar", opciones_imp_mun, default=opciones_imp_mun, key="imp_mun")
                cols_imp = st.columns(len(seleccion_imp))
                for i, imp in enumerate(seleccion_imp):
                    if "predial" in imp.lower():
                        mask = ofpuj_consolidada['clas_ofpuj'].str.contains("predial", case=False, na=False)
                    elif "industria" in imp.lower() or "comercio" in imp.lower():
                        mask = ofpuj_consolidada['clas_ofpuj'].str.contains("industria|comercio|ICA", case=False, na=False)
                    else:
                        mask = ofpuj_consolidada['clas_ofpuj'].str.contains(imp, case=False, na=False)
                    df_imp = ofpuj_consolidada[(ofpuj_consolidada['Entidad'] == entidad_sel) & mask].copy()
                    if not df_imp.empty:
                        prog_imp = df_imp['Total_Programado'].sum()
                        ejec_imp = df_imp['Total_Ejecutado'].sum()
                        tasa_imp = (ejec_imp / prog_imp * 100).round(2) if prog_imp > 0 else 0
                        with cols_imp[i]:
                            fig_mini = go.Figure(go.Indicator(
                                mode="gauge+number",
                                value=tasa_imp,
                                number={"suffix": "%", "font": {"size": 28, "color": "#1a1a2e"}},
                                gauge={"axis": {"range": [0, 100], "visible": False}, "bar": {"color": COLOR_POR_IMPUESTO.get(imp, "#185FA5"), "thickness": 0.3}, "bgcolor": "#F1EFE8", "borderwidth": 0},
                                title={"text": imp, "font": {"size": 13, "color": "#5F5E5A"}}
                            ))
                            fig_mini.update_layout(height=180, margin=dict(t=40, b=5, l=10, r=10), paper_bgcolor="white")
                            st.plotly_chart(fig_mini, use_container_width=True, config={"displayModeBar": False})
                            st.caption(f"{fmt_cop(ejec_imp)} / {fmt_cop(prog_imp)}")

            st.divider()

            with st.expander("Ver tabla de detalle completa"):
                st.dataframe(tabla_consolidada[tabla_consolidada['Entidad'] == entidad_sel], use_container_width=True)


 ##treemap
elif menu == "Treemap":
           
    st.header("Treemap")

#Presupuesto
elif  menu=="Presupuesto actual":
    st.header("Presupuesto actual")

#Descargas
elif  menu=="Descarga datos":
    st.header("Descarga datos")