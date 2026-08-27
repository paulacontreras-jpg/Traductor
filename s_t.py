import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob

from gtts import gTTS
from googletrans import Translator


# ---------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ---------------------------------------------------

st.set_page_config(
    page_title="Traductor",
    page_icon="💛",
    layout="centered"
)


# ---------------------------------------------------
# DECORACIÓN AMARILLA
# ---------------------------------------------------

st.markdown("""
<style>

    /* Fondo general */
    .stApp {
        background-color: #FFF9D6;
    }

    /* Título */
    h1 {
        color: #D4A900;
        text-align: center;
        font-weight: bold;
    }

    h2, h3 {
        color: #B8860B;
    }

    /* Texto */
    p {
        color: #4A4200;
    }

    /* Botones */
    .stButton > button {
        background-color: #FFD83D;
        color: #4A3B00;
        border: 2px solid #E5B900;
        border-radius: 12px;
        font-weight: bold;
        padding: 10px 25px;
    }

    .stButton > button:hover {
        background-color: #FFC400;
        color: white;
        border-color: #D4A000;
    }

    /* Selectbox */
    div[data-baseweb="select"] > div {
        border: 2px solid #FFD83D;
        border-radius: 10px;
        background-color: #FFFDF0;
    }

    /* Checkbox */
    .stCheckbox {
        color: #6B5700;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFF0A8;
    }

    /* Línea decorativa */
    .decoracion {
        text-align: center;
        font-size: 25px;
        color: #E5B900;
        margin: 5px;
    }

    /* Caja de información */
    .info-box {
        background-color: #FFF3A6;
        padding: 15px;
        border-radius: 15px;
        border: 2px solid #FFD83D;
        text-align: center;
        color: #5C4B00;
        margin-bottom: 20px;
    }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# TÍTULO
# ---------------------------------------------------

st.markdown(
    '<div class="decoracion">✦ ✦ ✦ 💛 ✦ ✦ ✦</div>',
    unsafe_allow_html=True
)

st.title("TRADUCTOR")

st.subheader("Escucho lo que quieres traducir.")

st.markdown("""
<div class="info-box">
🎤 Presiona el botón, habla y deja que el traductor haga el resto.
<br>
🌎 Traduce tu mensaje a diferentes idiomas.
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# IMAGEN
# ---------------------------------------------------

image = Image.open('gatos.jfif')

st.image(image, width=300)


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.subheader("💛 Traductor")

    st.write(
        "Presiona el botón. Cuando escuches la señal, "
        "habla lo que quieres traducir y luego selecciona "
        "la configuración de lenguaje que necesites."
    )

    st.markdown("🌎 **Idiomas disponibles:**")

    st.write("🇪🇸 Español")
    st.write("🇬🇧 Inglés")
    st.write("🇧🇩 Bengali")
    st.write("🇰🇷 Coreano")
    st.write("🇨🇳 Mandarín")
    st.write("🇯🇵 Japonés")
    st.write("🇫🇷 Francés")
    st.write("🇩🇪 Alemán")


# ---------------------------------------------------
# BOTÓN DE VOZ
# ---------------------------------------------------

st.write("### 🎤 Toca el botón y habla lo que quieres traducir")

stt_button = Button(
    label="💛 Escuchar 🎤",
    width=300,
    height=50
)

stt_button.js_on_event(
    "button_click",
    CustomJS(code="""
        var recognition = new webkitSpeechRecognition();

        recognition.continuous = false;
        recognition.interimResults = true;

        recognition.lang = 'es-ES';

        recognition.onresult = function (e) {

            var value = "";

            for (
                var i = e.resultIndex;
                i < e.results.length;
                ++i
            ) {

                if (e.results[i].isFinal) {
                    value += e.results[i][0].transcript;
                }

            }

            if (value != "") {

                document.dispatchEvent(
                    new CustomEvent(
                        "GET_TEXT",
                        {detail: value}
                    )
                );

            }

        }

        recognition.onend = function() {
            console.log("Reconocimiento detenido");
        }

        recognition.start();
    """)
)


# ---------------------------------------------------
# RECIBIR TEXTO
# ---------------------------------------------------

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)


# ---------------------------------------------------
# TRADUCCIÓN
# ---------------------------------------------------

if result:

    if "GET_TEXT" in result:

        st.markdown("### 📝 Texto detectado")

        st.write(result.get("GET_TEXT"))

    try:
        os.mkdir("temp")
    except:
        pass

    st.title("💛 Texto a Audio")

    translator = Translator()

    text = str(result.get("GET_TEXT"))


    # ---------------------------------------------------
    # IDIOMA DE ENTRADA
    # ---------------------------------------------------

    in_lang = st.selectbox(
        "🌎 Selecciona el lenguaje de entrada",

        (
            "Inglés",
            "Español",
            "Bengali",
            "Coreano",
            "Mandarín",
            "Japonés",
            "Francés",
            "Alemán"
        )
    )


    if in_lang == "Inglés":
        input_language = "en"

    elif in_lang == "Español":
        input_language = "es"

    elif in_lang == "Bengali":
        input_language = "bn"

    elif in_lang == "Coreano":
        input_language = "ko"

    elif in_lang == "Mandarín":
        input_language = "zh-cn"

    elif in_lang == "Japonés":
        input_language = "ja"

    elif in_lang == "Francés":
        input_language = "fr"

    elif in_lang == "Alemán":
        input_language = "de"


    # ---------------------------------------------------
    # IDIOMA DE SALIDA
    # ---------------------------------------------------

    out_lang = st.selectbox(
        "🌎 Selecciona el lenguaje de salida",

        (
            "Inglés",
            "Español",
            "Bengali",
            "Coreano",
            "Mandarín",
            "Japonés",
            "Francés",
            "Alemán"
        )
    )


    if out_lang == "Inglés":
        output_language = "en"

    elif out_lang == "Español":
        output_language = "es"

    elif out_lang == "Bengali":
        output_language = "bn"

    elif out_lang == "Coreano":
        output_language = "ko"

    elif out_lang == "Mandarín":
        output_language = "zh-cn"

    elif out_lang == "Japonés":
        output_language = "ja"

    elif out_lang == "Francés":
        output_language = "fr"

    elif out_lang == "Alemán":
        output_language = "de"


    # ---------------------------------------------------
    # ACENTO
    # ---------------------------------------------------

    english_accent = st.selectbox(
        "🎙️ Selecciona el acento",

        (
            "Defecto",
            "Español",
            "Reino Unido",
            "Estados Unidos",
            "Canada",
            "Australia",
            "Irlanda",
            "Sudáfrica",
        ),
    )


    if english_accent == "Defecto":
        tld = "com"

    elif english_accent == "Español":
        tld = "com.mx"

    elif english_accent == "Reino Unido":
        tld = "co.uk"

    elif english_accent == "Estados Unidos":
        tld = "com"

    elif english_accent == "Canada":
        tld = "ca"

    elif english_accent == "Australia":
        tld = "com.au"

    elif english_accent == "Irlanda":
        tld = "ie"

    elif english_accent == "Sudáfrica":
        tld = "co.za"


    # ---------------------------------------------------
    # FUNCIÓN TEXTO A VOZ
    # ---------------------------------------------------

    def text_to_speech(
        input_language,
        output_language,
        text,
        tld
    ):

        translation = translator.translate(
            text,
            src=input_language,
            dest=output_language
        )

        trans_text = translation.text

        tts = gTTS(
            trans_text,
            lang=output_language,
            tld=tld,
            slow=False
        )

        try:
            my_file_name = text[0:20]

        except:
            my_file_name = "audio"

        # Evitar caracteres problemáticos en el nombre
        my_file_name = "".join(
            c for c in my_file_name
            if c.isalnum() or c in (" ", "_", "-")
        )

        if my_file_name == "":
            my_file_name = "audio"

        tts.save(
            f"temp/{my_file_name}.mp3"
        )

        return my_file_name, trans_text


    # ---------------------------------------------------
    # MOSTRAR TEXTO
    # ---------------------------------------------------

    display_output_text = st.checkbox(
        "📝 Mostrar el texto traducido"
    )


    # ---------------------------------------------------
    # CONVERTIR
    # ---------------------------------------------------

    if st.button("💛 CONVERTIR"):

        result, output_text = text_to_speech(
            input_language,
            output_language,
            text,
            tld
        )

        audio_file = open(
            f"temp/{result}.mp3",
            "rb"
        )

        audio_bytes = audio_file.read()

        st.markdown(
            "## 🔊 Tu audio:"
        )

        st.audio(
            audio_bytes,
            format="audio/mp3",
            start_time=0
        )


        if display_output_text:

            st.markdown(
                "## 📝 Texto de salida:"
            )

            st.write(
                output_text
            )


# ---------------------------------------------------
# ELIMINAR ARCHIVOS ANTIGUOS
# ---------------------------------------------------

def remove_files(n):

    mp3_files = glob.glob(
        "temp/*mp3"
    )

    if len(mp3_files) != 0:

        now = time.time()

        n_days = n * 86400

        for f in mp3_files:

            if os.stat(f).st_mtime < now - n_days:

                os.remove(f)

                print(
                    "Deleted ",
                    f
                )


remove_files(7)


# ---------------------------------------------------
# DECORACIÓN FINAL
# ---------------------------------------------------

st.markdown(
    '<div class="decoracion">💛 ✦ 🌎 ✦ 🎤 ✦ 💛</div>',
    unsafe_allow_html=True
)


        
    



        
    


