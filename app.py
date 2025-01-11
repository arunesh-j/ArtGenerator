import streamlit as st
from openai import OpenAI
import requests
from io import BytesIO
from PIL import Image

# Set page config
st.set_page_config(
    page_title="Mandala Art Generator",
    page_icon="🎨",
    layout="centered"
) 

def generate_prompt(inspiration_word):
    """Generate a detailed prompt for DALL-E based on the inspiration word."""
    return f"Create a detailed, symmetrical black and white mandala pattern inspired by the concept of '{inspiration_word}'. The mandala should be intricate and detailed with geometric patterns. Style: monochromatic, zen-like, meditation art. The background must be pure white, with black lines and patterns forming the mandala design. The mandala should be clearly visible against the clean white background. No color, only black lines on white background."

def generate_mandala(prompt, api_key):
    """Generate mandala image using DALL-E 3."""
    try:
        client = OpenAI(api_key=api_key)
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None

def get_image_download_link(img_url, filename="mandala.png"):
    """Generate a download link for the image."""
    try:
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        
        # Ensure white background by creating a new white image and pasting the mandala
        white_bg = Image.new("RGB", img.size, "WHITE")
        if img.mode == 'RGBA':
            white_bg.paste(img, mask=img.split()[3])  # Use alpha channel as mask
        else:
            white_bg.paste(img)
        
        # Save to buffer
        buf = BytesIO()
        white_bg.save(buf, format="PNG")
        byte_im = buf.getvalue()
        return byte_im
    except Exception as e:
        st.error(f"Error preparing download: {str(e)}")
        return None

# Main app interface
def main():
    st.title("✨ Mandala Art Generator")
    st.write("Enter your OpenAI API key and an inspiration word to create a unique black and white mandala pattern.")

    # Input section
    with st.form("mandala_form"):
        # API Key input with password masking
        api_key = st.text_input(
            "Enter your OpenAI API Key:",
            type="password",
            help="Your API key will not be stored and will be used only for this session"
        )
        
        inspiration = st.text_input(
            "Enter your inspiration word:",
            placeholder="e.g., peace, nature, harmony"
        )
        
        generate_button = st.form_submit_button("Generate Mandala")

    if generate_button:
        if not api_key:
            st.error("Please enter your OpenAI API key")
        elif not inspiration:
            st.error("Please enter an inspiration word")
        else:
            with st.spinner("Creating your mandala... 🎨"):
                # Generate and display the mandala
                prompt = generate_prompt(inspiration)
                image_url = generate_mandala(prompt, api_key)
                
                if image_url:
                    st.image(image_url, caption=f"Mandala inspired by '{inspiration}'")
                    
                    # Prepare download button
                    image_data = get_image_download_link(image_url)
                    if image_data:
                        st.download_button(
                            label="Download Mandala",
                            data=image_data,
                            file_name=f"mandala_{inspiration}.png",
                            mime="image/png"
                        )
                        
                    st.success("Your mandala is ready! You can download it using the button above.")

    # Add app instructions and API key information
    with st.expander("How to use"):
        st.write("""
        1. Enter your OpenAI API key (get it from https://platform.openai.com/api-keys)
        2. Enter a single word that inspires you
        3. Click 'Generate Mandala' to create your unique art
        4. Wait a few seconds for the AI to generate your mandala
        5. Download your mandala using the download button
        6. Try different words to create various patterns!
        
        Note: Your API key is not stored and is only used for the current session.
        """)

if __name__ == "__main__":
    main()