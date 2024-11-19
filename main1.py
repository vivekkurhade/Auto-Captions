import os
import whisper
from datetime import timedelta
import math


FRAME_RATE = 30 

def format_timestamp(seconds):
   
    ms = int((seconds - int(seconds)) * 1000)
    td = timedelta(seconds=int(seconds))
    return f"{str(td)}.{ms:03d}".replace(".", ",")

def transcribe_and_generate_srt(audio_file, output_srt="subtitles.srt", words_per_subtitle=3):
    """Transcribe audio and create subtitles with accurate timestamps."""
    model = whisper.load_model("base")
    print(f"Transcribing {audio_file}...")

  
    result = model.transcribe(audio_file, word_timestamps=True)
    segments = result["segments"]

    print("Transcription completed. Generating subtitles...")

    subtitles = []
    subtitle_text = []
    subtitle_start_time = None
    subtitle_end_time = None

    for segment in segments:
        for word_info in segment["words"]:
            word = word_info["word"]
            start_time = word_info["start"]
            end_time = word_info["end"]

           
            start_time = round(start_time * FRAME_RATE) / FRAME_RATE
            end_time = round(end_time * FRAME_RATE) / FRAME_RATE

          
            if subtitle_start_time is None:
                subtitle_start_time = start_time

           
            subtitle_text.append(word)
            subtitle_end_time = end_time

          
            if len(subtitle_text) >= words_per_subtitle:
                subtitles.append({
                    "start": subtitle_start_time,
                    "end": subtitle_end_time,
                    "text": " ".join(subtitle_text)
                })
               
                subtitle_text = []
                subtitle_start_time = None

   
    if subtitle_text:
        subtitles.append({
            "start": subtitle_start_time,
            "end": subtitle_end_time,
            "text": " ".join(subtitle_text)
        })

    
    with open(output_srt, "w") as srt_file:
        for idx, subtitle in enumerate(subtitles, 1):
            start_time = format_timestamp(subtitle["start"])
            end_time = format_timestamp(subtitle["end"])
            text = subtitle["text"]

          
            srt_file.write(f"{idx}\n")
            srt_file.write(f"{start_time} --> {end_time}\n")
            srt_file.write(f"{text}\n\n")

    print(f"Subtitles saved to {output_srt}")


def main():
    """Main function to take user input and process the audio file."""
    audio_file = input("Enter the path to your audio file (mp3, mp4, wav, mov, etc.): ")

    if not os.path.exists(audio_file):
        print("The specified audio file does not exist. Please check the path and try again.")
        return

    output_srt = "subtitles.srt"
    transcribe_and_generate_srt(audio_file, output_srt)


if __name__ == "__main__":
    main()
