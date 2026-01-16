import re
import streamlit as st
import google.generativeai as g
from google.generativeai import types
from PIL import Image
from io import BytesIO

client=g.configure(api_key="AIzaSyAhKCXXHgbr8f9Ld0NPzLuF0jKnfESUz2A")
def is_prompt_safe(prompt: str)-> bool:import re
import streamlit as st
import google.generativeai as g
from google.generativeai import types
from PIL import Image
from io import BytesIO

client=g.configure(api_key="AIzaSyAhKCXXHgbr8f9Ld0NPzLuF0jKnfESUz2A")
def is_prompt_safe(prompt: str)-> bool:
    forbidden_keywords=[
        "violence","weapon","gun","blood","death","kill","hurt","harm","suicide","self-destruct","explosion","fire","terroism","explosive","bomb"
    ]
    pattern=re.compile("|".join(forbidden_keywords),re.IGNORECASE)
    return not bool(pattern.search(prompt))
def generate_response(prompt:str):
    if not is_prompt_safe(prompt):
        return None, "your prompt contains restricted keywords. please modify your prompt and try again."
    try:
        model="gemini-2.0-flash-preview-image-generation"
        contents=[types.Content(role="user",parts=[types.Part(text=prompt)])]
        generate_content_config=types.GenerateContentConfig(response_modalities=["IMAGE","TEXT"],
        response_mine_type="text/plain"
        )
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            generate_content_config=generate_content_config,
        ):
            if(
                chunk.candidates is None
                or chunk.candidates[0].content is None
                or chunk.candidates[0].content.parts is None
            ):
                continue
            if(chunk.candidates[0].content.parts[0].inline_data and
               chunk.candidates[0].content.parts[0].inline_data.data):
                inline_data=chunk.candidates[0].content.parts[0].inline_data
                data_buffer=inline_data.data
                image=Image, None
            elif chunk.text:
                continue
        return None, "no response generated"
    except Exception as e:
        return None, f" Error during image generation: {str(e)}"
def main():
    st.set_page_config(page_title="ai image geneartor",page_icon=":robot:")
    st.title("???? Safe AI Image Generator")
    st.info("Describe an image to genearte using Google Gemini 2.0 Flash. Make sure it's safe and respectful")
    with st.form(key="image_form"):
        prompt=st.text_area("image description", height=100,
                            placeholder="enter a detailed description of the image you want to generate")
        submit=st.form_submit_button("generating image")
        if submit:
            if not prompt.strip:
                st.warning("please enter a prompt")
            else:
                with st.spinner("generating image..."):
                    image,error=generate_response(prompt)
                    if error:
                        st.error(error)
                    elif image:
                        st.image(image,vaption="generated image",use_column_width=True)
                        st.session_state.generated_image=image
                    else:
                        st.error("no image generated")
        if hasattr(st.session_state,"generated_image")and st.session_state.generated_image:
            buf=BytesIO()
            st.session_state.generated_image.save(buf,format="PNG")
            byte_im=buf.getvalue()
            btn=st.download_button(
            label="download image",
            data=byte_im,
            file_name="generated_image.png",
            mime="image/png")
if __name__=="__main__":
    main()