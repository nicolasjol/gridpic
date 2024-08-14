import streamlit as st
from PIL import Image, UnidentifiedImageError
import os

def create_printable_grid(input_img, output_path, input_size_inches, output_size_inches, dpi=600):
    # Convert sizes to pixels
    input_size_pixels = (int(input_size_inches[0] * dpi), int(input_size_inches[1] * dpi))
    output_size_pixels = (int(output_size_inches[0] * dpi), int(output_size_inches[1] * dpi))

    img = input_img.resize(input_size_pixels, Image.ANTIALIAS)
    img_width, img_height = img.size

    output_img = Image.new("RGB", output_size_pixels, "white")

    tiles_x = output_size_pixels[0] // img_width
    tiles_y = output_size_pixels[1] // img_height

    remaining_space_x = (output_size_pixels[0] - (tiles_x * img_width)) // 2
    remaining_space_y = (output_size_pixels[1] - (tiles_y * img_height)) // 2

    for row in range(tiles_y):
        for col in range(tiles_x):
            x = remaining_space_x + col * img_width
            y = remaining_space_y + row * img_height
            output_img.paste(img, (x, y))

    output_img.save(output_path)

def main():
    st.title("Image Grid Generator")
    
    st.write("Upload an image and specify the sizes to create a printable grid.")
    
    input_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if input_file:
        try:
            img = Image.open(input_file)
            st.image(img, caption="Uploaded Image", use_column_width=True)

            st.write("### Specify Image and Output Sizes")
            input_width = st.text_input("Input Width (in inches):", "")
            input_height = st.text_input("Input Height (in inches):", "")
            output_width = st.text_input("Output Width (in inches):", "4")
            output_height = st.text_input("Output Height (in inches):", "6")

            if st.button("Generate Grid"):
                try:
                    output_width = float(output_width)
                    output_height = float(output_height)

                    if input_width and input_height:
                        input_size_inches = (float(input_width), float(input_height))
                    else:
                        img_width, img_height = img.size
                        input_size_inches = (img_width / 600, img_height / 600)

                    output_path = "output.jpg"
                    create_printable_grid(img, output_path, input_size_inches, (output_width, output_height))

                    st.success("Grid generated successfully!")
                    st.image(output_path, caption="Generated Image", use_column_width=True)
                    with open(output_path, "rb") as file:
                        btn = st.download_button(
                            label="Download Image",
                            data=file,
                            file_name="output.jpg",
                            mime="image/jpeg"
                        )
                except ValueError:
                    st.error("Please enter valid numerical values for sizes.")

        except UnidentifiedImageError:
            st.error("The uploaded file is not a valid image. Please upload a valid image file.")

if __name__ == "__main__":
    main()

