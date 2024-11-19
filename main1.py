import os
import whisper
from datetime import timedelta
import math

# Constants for accurate time formatting
FRAME_RATE = 30  # Default frame rate for subtitles. Adjust if needed.

def format_timestamp(seconds):
    """Formats timestamps for SRT files with millisecond precision."""
    ms = int((seconds - int(seconds)) * 1000)
    td = timedelta(seconds=int(seconds))
    return f"{str(td)}.{ms:03d}".replace(".", ",")

def transcribe_and_generate_srt(audio_file, output_srt="subtitles.srt", words_per_subtitle=3):
    """Transcribe audio and create subtitles with accurate timestamps."""
    model = whisper.load_model("base")
    print(f"Transcribing {audio_file}...")

    # Transcribe with word-level timestamps
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

            # Round start and end time to the nearest frame
            start_time = round(start_time * FRAME_RATE) / FRAME_RATE
            end_time = round(end_time * FRAME_RATE) / FRAME_RATE

            # Initialize the start time for the subtitle
            if subtitle_start_time is None:
                subtitle_start_time = start_time

            # Add word to the current subtitle
            subtitle_text.append(word)
            subtitle_end_time = end_time

            # Finalize subtitle when reaching the word limit
            if len(subtitle_text) >= words_per_subtitle:
                subtitles.append({
                    "start": subtitle_start_time,
                    "end": subtitle_end_time,
                    "text": " ".join(subtitle_text)
                })
                # Reset for the next subtitle
                subtitle_text = []
                subtitle_start_time = None

    # Add remaining words as the last subtitle
    if subtitle_text:
        subtitles.append({
            "start": subtitle_start_time,
            "end": subtitle_end_time,
            "text": " ".join(subtitle_text)
        })

    # Write subtitles to an SRT file
    with open(output_srt, "w") as srt_file:
        for idx, subtitle in enumerate(subtitles, 1):
            start_time = format_timestamp(subtitle["start"])
            end_time = format_timestamp(subtitle["end"])
            text = subtitle["text"]

            # Write each subtitle entry
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
