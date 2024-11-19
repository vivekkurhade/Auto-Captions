
# Audio Transcription and Subtitle Generation

This Python script uses OpenAI's Whisper model to transcribe audio files and generate subtitles in the SubRip Subtitle (SRT) format. The subtitles are generated with word-level timestamps, allowing precise synchronization with the audio.

## Features
- Transcribes audio files (mp3, mp4, wav, mov, etc.) into text.
- Generates SRT files with accurate timestamps for each word.
- Optionally splits subtitles into chunks with a configurable number of words per subtitle.
- Handles various audio file formats supported by Whisper.

## Requirements

- Python 3.7+
- Required libraries:
  - `whisper` (OpenAI Whisper model for transcription)
  - `datetime` (For formatting timestamps)
  - `math` (For rounding timestamps)
  
To install the dependencies, run:

```bash
pip install openai-whisper
```

## Usage

1. Clone or download the repository.
2. Place your audio file (e.g., mp3, wav, mov) in the same directory or provide the file path.
3. Run the script:

```bash
python transcribe_and_generate_srt.py
```

4. You will be prompted to enter the path to your audio file. If the path is valid, the script will transcribe the audio and generate an `srt` file (`subtitles.srt` by default) with the corresponding subtitles.

## Script Details

### `format_timestamp(seconds)`
Formats timestamps to SRT file format with millisecond precision.

### `transcribe_and_generate_srt(audio_file, output_srt="subtitles.srt", words_per_subtitle=3)`
- Transcribes the provided audio file using Whisper.
- Generates subtitles with accurate timestamps for each word.
- Splits subtitles into chunks based on the `words_per_subtitle` parameter.
- Saves the subtitles to an SRT file.

### `main()`
Prompts the user to input an audio file path and calls the transcription and subtitle generation functions.

## Customization
- **Frame Rate:** The default frame rate for subtitle formatting is set to 30. You can adjust this value in the script to match your needs.
- **Words per Subtitle:** You can change the number of words per subtitle by modifying the `words_per_subtitle` parameter in the `transcribe_and_generate_srt()` function.

## Output
The output will be a `.srt` file with subtitles that are synchronized with the audio. The file will be saved with the name `subtitles.srt` (you can specify a different name if desired).

## Example

Given an audio file `sample.mp3`, running the script will generate a `subtitles.srt` file that looks like this:

```
1
00:00:00,000 --> 00:00:01,500
This is the first word.

2
00:00:01,500 --> 00:00:03,000
This is the second word.
```

## Troubleshooting

- If the script cannot find the audio file, it will display an error message and ask you to check the file path.
- Ensure that the Whisper model is properly installed and accessible in your environment.
