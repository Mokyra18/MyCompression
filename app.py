import streamlit as st
import os
from pydub import AudioSegment
from PIL import Image
from moviepy.editor import VideoFileClip
import io
import tempfile

#Image.ANTIALIAS = Image.LANCZOS

def compress_audio_algorithm1(input_file):
    # Implementasi algoritma kompresi lossless pertama (misalnya, FLAC)
    audio = AudioSegment.from_file(input_file)
    output_buffer = io.BytesIO()
    audio.export(output_buffer, format='flac')
    return output_buffer.getvalue()

def compress_audio_algorithm2(input_file):
    # Konversi audio ke format WAV (tanpa kompresi tambahan)
    audio = AudioSegment.from_file(input_file)
    output_buffer = io.BytesIO()
    audio.export(output_buffer, format='wav')
    return output_buffer.getvalue()

def compress_image_algorithm1(input_file, quality=50):
    # Implementasi algoritma kompresi lossless pertama (JPEG)
    img = Image.open(input_file)
    output_buffer = io.BytesIO()
    img.convert("RGB").save(output_buffer, format='JPEG', quality=quality)
    return output_buffer.getvalue()

def compress_image_algorithm2(input_file, quality=50):
    # Implementasi algoritma kompresi lossless kedua (PNG)
    img = Image.open(input_file)
    output_buffer = io.BytesIO()
    img.save(output_buffer, format='PNG', quality=quality)
    return output_buffer.getvalue()

def compress_video_algorithm1(input_file, target_resolution=(480, 270), bitrate='500k'):
    try:
        # Use BytesIO to handle in-memory file
        tfile = io.BytesIO(input_file.read())
        
        # Write the BytesIO content to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(tfile.getbuffer())
            temp_filename = temp_file.name
        
        # Process the video using moviepy with H.264 codec
        video = VideoFileClip(temp_filename)
        video_resized = video.resize(height=target_resolution[1])
        
        # Write the resized video to another temporary file
        temp_output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_output_filename = temp_output_file.name
        temp_output_file.close()
        
        video_resized.write_videofile(temp_output_filename, bitrate=bitrate, codec='libx264')

        # Read the compressed video back into memory
        with open(temp_output_filename, "rb") as f:
            compressed_video = f.read()

        # Clean up temporary files
        os.remove(temp_filename)
        os.remove(temp_output_filename)

        return compressed_video

    except Exception as e:
        # Handle errors
        st.error(f"Error compressing video with Algorithm 1: {e}")
        return None

def compress_video_algorithm2(input_file, target_resolution=(480, 270), bitrate='500k'):
    try:
        # Use BytesIO to handle in-memory file
        tfile = io.BytesIO(input_file.read())
        
        # Write the BytesIO content to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(tfile.getbuffer())
            temp_filename = temp_file.name
        
        # Process the video using moviepy with HEVC codec
        video = VideoFileClip(temp_filename)
        video_resized = video.resize(height=target_resolution[1])
        
        # Write the resized video to another temporary file
        temp_output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_output_filename = temp_output_file.name
        temp_output_file.close()
        
        video_resized.write_videofile(temp_output_filename, bitrate=bitrate, codec='libx265')

        # Read the compressed video back into memory
        with open(temp_output_filename, "rb") as f:
            compressed_video = f.read()

        # Clean up temporary files
        os.remove(temp_filename)
        os.remove(temp_output_filename)

        return compressed_video

    except Exception as e:
        # Handle errors
        st.error(f"Error compressing video with Algorithm 2: {e}")
        return None

def home_page():
    st.title("Welcome to MyCompression")
    st.write("""
    This application allows you to compress audio, image, and video files using different algorithms.
    Choose a compression type from the sidebar to get started.
    """)

    st.write("### Audio Compression Algorithms")
    st.write("""
    - *Algorithm 1 (FLAC)*: FLAC (Free Lossless Audio Codec) is a popular lossless compression format. It reduces file size without losing any audio data.
    - *Algorithm 2 (WAV)*: WAV is an uncompressed audio format that preserves the full quality of the original audio, but it doesn't reduce file size significantly.
    """)

    st.write("### Image Compression Algorithms")
    st.write("""
    - *Algorithm 1 (JPEG)*: JPEG is a commonly used method of lossless compression for digital images. The degree of compression can be adjusted, allowing a trade-off between storage size and image quality.
    - *Algorithm 2 (PNG)*: PNG (Portable Network Graphics) is a lossless compression format suitable for images with text, line art, or where fine detail is important.
    """)

    st.write("### Video Compression Algorithms")
    st.write("""
    - *Algorithm 1 (H.264)*: H.264 is a popular video compression standard known for good video quality at lower bitrates. It is widely supported by most devices and media players.
    - *Algorithm 2 (HEVC)*: HEVC (High Efficiency Video Coding), also known as H.265, provides better compression efficiency than H.264. It delivers higher quality at the same bitrate or the same quality at a lower bitrate.
    """)

def format_file_size(size):
    return f"{size / 1024:.2f} KB"

def audio_compression():
    st.title("Audio Compression")
    st.sidebar.write("""
    Choose your preferred compression algorithm:
    - *FLAC*: Lossless compression, retains full quality.
    - *WAV*: Uncompressed format, no additional compression.
    """)

    st.sidebar.title("Settings")
    # Tambahkan opsi bitrate jika ingin tetap mempertahankannya
    # audio_bitrate = st.sidebar.selectbox("Select audio bitrate", ["64k", "128k", "192k", "256k", "320k"])

    st.write("## Upload your audio file and compress it!")

    audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "flac"])

    if audio_file is not None:
        st.audio(audio_file, format='audio/mp3', start_time=0)
        st.write("Uploaded Audio File Details:")
        audio_details = {"Filename": audio_file.name, "FileType": audio_file.type, "FileSize": audio_file.size}
        st.write(audio_details)
        
        st.write("## Choose Compression Algorithm")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Compress with Algorithm 1 (FLAC)"):
                st.write("Compressing audio with Algorithm 1...")
                # Gunakan algoritma kompresi lossless pertama (FLAC)
                compressed_audio = compress_audio_algorithm1(audio_file)
                st.success("Audio compression with Algorithm 1 successful!")
                
                st.write("### Download Compressed Audio")
                audio_download_button_str1 = f"Download Compressed Audio File (Algorithm1 - {os.path.splitext(audio_file.name)[0]}_compressed.flac)"
                st.download_button(label=audio_download_button_str1, data=compressed_audio, file_name=f"{os.path.splitext(audio_file.name)[0]}_compressed_algorithm1.flac", mime="audio/flac", key="algorithm1")
        
        with col2:
            if st.button("Compress with Algorithm 2 (WAV)"):
                st.write("Converting audio to WAV format...")
                compressed_audio = compress_audio_algorithm2(audio_file)
                st.success("Audio conversion to WAV successful!")
                
                st.write("### Download Compressed Audio")
                audio_download_button_str2 = f"Download Compressed Audio File (Algorithm2 - {os.path.splitext(audio_file.name)[0]}_converted.wav)"
                st.download_button(label=audio_download_button_str2, data=compressed_audio, file_name=f"{os.path.splitext(audio_file.name)[0]}_converted_algorithm2.wav", mime="audio/wav", key="algorithm2")



def image_compression():
    st.title("Image Compression")
    st.sidebar.write("""
    Choose your preferred compression algorithm:
    - *JPEG*: Lossless compression, adjustable quality.
    - *PNG*: Lossless compression, preserves full quality.
    """)

    st.sidebar.title("Settings")
    image_quality = st.sidebar.slider("Select image quality", min_value=1, max_value=100, value=50)

    st.write("## Upload your image file and compress it!")

    image_file = st.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"])

    if image_file is not None:
        st.image(image_file, caption="Uploaded Image", use_column_width=True)
        st.write("Uploaded Image File Details:")
        image_details = {"Filename": image_file.name, "FileType": image_file.type, "FileSize": image_file.size}
        st.write(image_details)
        
        st.write("## Choose Compression Algorithm")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Compress with Algorithm 1 (JPEG)"):
                st.write("Compressing image with Algorithm 1...")
                # Gunakan algoritma kompresi lossless pertama (JPEG)
                compressed_image = compress_image_algorithm1(image_file, quality=image_quality)
                st.success("Image compression with Algorithm 1 successful!")
                
                st.write("### Download Compressed Image")
                image_download_button_str1 = f"Download Compressed Image File (Algorithm1 - {os.path.splitext(image_file.name)[0]}_compressed.jpg)"
                st.download_button(label=image_download_button_str1, data=compressed_image, file_name=f"{os.path.splitext(image_file.name)[0]}_compressed_algorithm1.jpg", mime="image/jpeg", key="algorithm1")
        
        with col2:
            if st.button("Compress with Algorithm 2 (PNG)"):
                st.write("Compressing image with Algorithm 2...")
                # Gunakan algoritma kompresi lossless kedua (PNG)
                compressed_image = compress_image_algorithm2(image_file, quality=image_quality)
                st.success("Image compression with Algorithm 2 successful!")
                
                st.write("### Download Compressed Image")
                image_download_button_str2 = f"Download Compressed Image File (Algorithm2 - {os.path.splitext(image_file.name)[0]}_compressed.png)"
                st.download_button(label=image_download_button_str2, data=compressed_image, file_name=f"{os.path.splitext(image_file.name)[0]}_compressed_algorithm2.png", mime="image/png", key="algorithm2")

def video_compression():
    st.title("Video Compression")


    st.sidebar.title("Settings")
    target_resolution = st.sidebar.selectbox("Select resolution", ["480p", "720p", "1080p"])
    resolutions = {"480p": (480, 270), "720p": (1280, 720), "1080p": (1920, 1080)}
    video_bitrate = st.sidebar.selectbox("Select video bitrate", ["500k", "1000k", "1500k", "2000k"])
    st.sidebar.write("""
    Choose your preferred compression algorithm:
    - *H.264*: Good video quality at lower bitrates.
    - *HEVC*: Higher quality at the same bitrate or same quality at a lower bitrate.
    """)
    st.write("## Upload your video file and compress it!")

    video_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])

    if video_file is not None:
        st.video(video_file)
        st.write("Uploaded Video File Details:")
        video_details = {"Filename": video_file.name, "FileType": video_file.type, "FileSize": video_file.size}
        st.write(video_details)
        
        st.write("## Choose Compression Algorithm")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Compress with Algorithm 1 (H.264)"):
                st.write("Compressing video with Algorithm 1...")
                # Gunakan algoritma kompresi lossless pertama (H.264)
                compressed_video = compress_video_algorithm1(video_file, target_resolution=resolutions[target_resolution], bitrate=video_bitrate)
                st.success("Video compression with Algorithm 1 successful!")
                
                st.write("### Download Compressed Video")
                video_download_button_str1 = f"Download Compressed Video File (Algorithm1 - {os.path.splitext(video_file.name)[0]}_compressed.mp4)"
                st.download_button(label=video_download_button_str1, data=compressed_video, file_name=f"{os.path.splitext(video_file.name)[0]}_compressed_algorithm1.mp4", mime="video/mp4", key="algorithm1")
        
        with col2:
            if st.button("Compress with Algorithm 2 (HEVC)"):
                st.write("Compressing video with Algorithm 2...")
                # Gunakan algoritma kompresi lossless kedua (HEVC)
                compressed_video = compress_video_algorithm2(video_file, target_resolution=resolutions[target_resolution], bitrate=video_bitrate)
                st.success("Video compression with Algorithm 2 successful!")
                
                st.write("### Download Compressed Video")
                video_download_button_str2 = f"Download Compressed Video File (Algorithm2 - {os.path.splitext(video_file.name)[0]}_compressed.mp4)"
                st.download_button(label=video_download_button_str2, data=compressed_video, file_name=f"{os.path.splitext(video_file.name)[0]}_compressed_algorithm2.mp4", mime="video/mp4", key="algorithm2")

def multipage():
    pages = {
        "Home": home_page,
        "Audio Compression": audio_compression,
        "Image Compression": image_compression,
        "Video Compression": video_compression
    }
    
    st.sidebar.title("MyCompression")
    page_selection = st.sidebar.radio("Go to", list(pages.keys()))
    
    page = pages[page_selection]
    page()

if __name__ == '__main__':
    multipage()
