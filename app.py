import streamlit as st
import pandas as pd
import joblib

# Título do formulário
st.title("Predição de Sobrevida")

st.write(
    "Preencha os campos abaixo com os valores correspondentes às variáveis utilizadas no modelo preditivo."
)

#Criando listas
cid = pd.read_csv("cids.csv")
cid_list = cid['Codigo'].tolist()

status_options = ["Nenhuma das anteriores(Verde)", "Outras situações que requerem atend. com urgência intermediária - (Amarelo)", 
                  "Suspeita/Confirmação de NF - (Amarelo)", "Dor Intensa (> 7 em 10) - (Amarelo)", "Sala de Emergência - (Vermelho)", 
                  "Suspeita de SCM - (Amarelo)",
                  "Sepse - (Amarelo)","Dessaturação - (Amarelo)", "Hemorragia com potencial risco de vida - (Amarelo)", 
                  "Sinais de choque - (Vermelho)", 
                  "Fase Final de Vida - (Amarelo)", "Outras situações que requerem atend. Prioritário - (Vermelho)", "IRA - (Amarelo)", 
                  "Desconforto Respiratório - (Vermelho)", "Distúrbio Hidroeletrolítico com risco de instabilidade - (Amarelo)",
                  "Rebaixamento do Nível de Consciência - (Vermelho)", "Suspeita de SCA - (Vermelho)", "Sangramento Ativo Ameaçador à Vida - (Vermelho)",
                  "Suspeita de Síndrome de Lise Tumoral - (Vermelho)"]

priority_options = ["Verde", "Amarelo", "Vermelho"]

tendency_options = ["Estável", "Instável", "Melhorando"]

 
 
# Criando o formulário
with st.form(key="input_form"):

    # Seção 1: Informações Pessoais
    st.subheader("Informações Pessoais")
    age = st.number_input("Idade", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Sexo", options=["Masculino", "Feminino"])

    st.markdown("---")  # Linha de separação

    # Seção 2: Sinais Vitais
    st.subheader("Sinais Vitais")
    mbp = st.number_input("Pressão Arterial", min_value=0.0, step=0.1)
    hr = st.number_input("Frequência Cardíaca", min_value=0.0, step=0.1)
    os = st.number_input("Saturação de Oxigênio", min_value=0.0, step=0.1)

    st.markdown("---")  # Linha de separação

    # Seção 3: Antropometria
    st.subheader("Antropometria")
    missing_bmi = st.checkbox("Ausência de Antropometria")
    height = st.number_input("Altura", min_value=0.0, step=0.1)
    weight = st.number_input("Peso Estimado", min_value=0.0, step=0.1)
    bmi = st.number_input("Índice de Massa Corporal", min_value=0.0, step=0.1)

    st.markdown("---")  # Linha de separação

    # Seção 4: Diagnóstico e Status
    st.subheader("Diagnóstico e Status")
    icd = st.selectbox("CID", options=cid_list)
    status_original = st.selectbox("Status Original", options=status_options)
    status_priority = st.selectbox("Prioridade", options=priority_options)

    st.markdown("---")  # Linha de separação

    # Seção 5: Histórico Clínico
    st.subheader("Histórico Clínico")
    ti = st.number_input("Tempo entre Última Consulta e PS", min_value=0.0, step=0.1)
    tdr = st.selectbox("Internação Recente", options=["Não", "Sim"])
    tendency = st.selectbox("Tendência", options=tendency_options)

    st.markdown("---")  # Linha de separação

    # Seção 6: Escore Funcional
    st.subheader("Escore Funcional")
    missing_ecog = st.checkbox("Ausência de ECOG")
    ecog = st.number_input("ECOG", min_value=0.0, max_value=4.0, step=0.1)

    st.markdown("---")  # Linha de separação

    # Botão de envio
    submit_button = st.form_submit_button(label="Enviar")

# Exibir os dados submetidos
if submit_button:
    st.success("Dados enviados com sucesso!")
    st.write("Valores inseridos:")
    st.write({
        "Idade": age,
        "Sexo": gender,
        "Pressão Arterial": mbp,
        "Frequência Cardíaca": hr,
        "Saturação de Oxigênio": os,
        "Altura": height,
        "Peso Estimado": weight,
        "Índice de Massa Corporal": bmi,
        "Ausência de Antropometria": missing_bmi,
        "CID": icd,
        "Status Original": status_original,
        "Prioridade do Status": status_priority,
        "Tempo entre Última Consulta e PS": ti,
        "Internação Recente": tdr,
        "Tendência": tendency,
        "ECOG": ecog,
        "Ausência de ECOG": missing_ecog,
    })

if submit_button:
    # Criar DataFrame a partir dos inputs do usuário
    df_input = pd.DataFrame({
        "age": [age],
        "gender": [gender],  
        "mbp": [mbp],
        "hr": [hr],
        "os": [os],
        "height": [height],
        "weight": [weight],
        "bmi": [bmi],
        "icd": icd,  
        "status_original": [status_original],  
        "status_priority": [status_priority],  
        "ti": [ti],  
        "tdr": [tdr],  
        "tendency": [tendency],  
        "ecog": [ecog],  
        "missing_ecog": [missing_ecog]
    })

if submit_button:

    #Print:
    #st.subheader("📊 Dados inseridos pelo usuário")
    #st.dataframe(df_input)

    #Encoding CID
    try:
        encoding_maps = joblib.load("encoding_maps.joblib")
        encoding_maps_cid = encoding_maps["ICD"]
        st.write("✅ Preparando dados para predição...")
        df_input["icd_processed"] = df_input["icd"].str.split(" - ").str[0].str.lower()
        df_input["icd_encoded"] = df_input["icd_processed"].map(encoding_maps_cid).fillna(0.34162670016104163)
    except Exception as e:
        st.write("❌ Erro preparar dados para predição...")

    #Encoding Status_Original
    try:
        encoding_maps_status = encoding_maps["Status_Original"]
        st.write("✅ Preparando dados para predição...")
        st.write("📌 Mapping de CIDs:", encoding_maps_status)
        df_input["status_original_encoded"] = df_input["status_original"].map(encoding_maps_status).fillna(0.31209494163715695)
        st.write("Dados com Status codificado:", df_input["status_original_encoded"])
    except Exception as e:
        st.write("❌ Erro preparar dados para predição...")

    #Encoding Status_Ordinal

    #Encoding Sexo

    #Encoding TDR

    #Encoding Tendência

    #Encoding missing_ecog

    #Encoding missing_ecog

    #Scaling

    #Aplicando predição

    #Mostrando predição


