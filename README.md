# Inglés ¡YA! — versión WEB

Conversión de la aplicación de escritorio Tkinter a Streamlit.

## Incluye
- Niveles A1 a C1-C2.
- 10 unidades por nivel, lecciones A/B/C/D.
- Vocabulario, pronunciación, gramática, diálogo, lectura, ejercicios, práctica oral, evaluación y tareas.
- Audio neural inglés estadounidense con Edge TTS.
- Grabación desde el navegador con `st.audio_input` y reconocimiento de voz.
- Corrector de respuestas.
- Navegación anterior/siguiente.
- Interfaz responsive para PC, tablet y celular.

## Probar en tu PC
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publicar en Streamlit Community Cloud
1. Crea un repositorio de GitHub.
2. Sube todos los archivos de esta carpeta conservando `.streamlit/` y `assets/`.
3. En Streamlit Community Cloud selecciona el repositorio.
4. Main file: `app.py`.
5. Deploy.

## Importante sobre progreso y usuarios
Esta primera conversión conserva el progreso durante la sesión del navegador. Para alumnos reales y progreso permanente por usuario conviene conectar el login existente de Inglés ¡YA! a Supabase y guardar allí el avance. Eso evita que dos alumnos compartan el mismo progreso.


## Complete curriculum build
This build includes lesson-specific CEFR-scaled vocabulary, pronunciation, grammar guidance, dialogue, reading, exercises, speaking prompts, evaluation and homework for all 320 lessons.
