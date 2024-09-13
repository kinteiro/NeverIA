import streamlit as st
import base64
from PIL import Image
# from datetime import datetime
from OpenAiPromptAPI_GPT4_Vision import text_output


# Variable global para almacenar el base64 de la imagen
img_b64 = None

def main():
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image("Images/NeverIA.jpeg")
    st.title("Vamos a hacer recetas con lo que tengas por la nevera! ") 
    img_file = st.file_uploader("Haz una foto o adjunta una imagen con los ingredientes de tu nevera", type=['png', 'jpg', 'jpeg'])

    global img_b64  

    if img_file is not None:
        img = Image.open(img_file)
        st.image(img, caption='Imagen cargada!', use_column_width=True)
        img_b64 = base64.b64encode(img_file.getvalue()).decode()

    if st.button("Analizar Imagen") and img_b64 is not None:
        with st.spinner('Vamos a ver qué tiene tu nevera...'):
            text = text_output(img_b64)
        st.markdown(text)

if __name__ == "__main__":
    main()
