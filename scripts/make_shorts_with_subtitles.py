#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_shorts_with_subtitles.py — Генератор вертикальных видео 9:16 (Shorts/Reels/TikTok) со стильными вшитыми субтитрами.
"""

import os, sys, argparse, subprocess, tempfile
from faster_whisper import WhisperModel

def format_ass_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours}:{minutes:02d}:{secs:05.2f}"

def process_video(input_path, output_path, chunk_words=3, font_size=80, model_size="small"):
    if not os.path.exists(input_path):
        print(f"Error: Input video not found at {input_path}")
        sys.exit(1)

    work_dir = tempfile.mkdtemp(prefix="shorts_")
    audio_path = os.path.join(work_dir, "audio.wav")
    ass_path = os.path.join(work_dir, "subtitles.ass")

    print("1. Extracting audio track...")
    subprocess.run([
        "ffmpeg", "-i", input_path,
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        audio_path, "-y"
    ], capture_output=True, check=True)

    print(f"2. Transcribing with faster-whisper (model: {model_size}, word timestamps)...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_path, beam_size=5, word_timestamps=True)

    ass_header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: HormoziYellow,DejaVu Sans,{font_size},&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,3,2,30,30,220,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    dialogues = []
    for seg in segments:
        words = list(seg.words)
        for i in range(0, len(words), chunk_words):
            chunk = words[i:i+chunk_words]
            if not chunk:
                continue
            c_start = chunk[0].start
            c_end = chunk[-1].end
            text = " ".join([w.word.strip().upper() for w in chunk])
            t_start_ass = format_ass_time(c_start)
            t_end_ass = format_ass_time(c_end)
            dialogues.append(f"Dialogue: 0,{t_start_ass},{t_end_ass},HormoziYellow,,0,0,0,,{text}")

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_header + "\n".join(dialogues))

    print(f"3. Rendering 9:16 vertical video with burned-in subtitles via ffmpeg...")
    filter_complex = f"[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,ass={ass_path}[v]"
    cmd = [
        "ffmpeg", "-i", input_path,
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "0:a?",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "22",
        "-c:a", "aac",
        "-b:a", "128k",
        output_path,
        "-y"
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    print(f"✅ Finished! Shorts saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create vertical Shorts/Reels with burned-in subtitles.")
    parser.add_argument("--input", "-i", required=True, help="Path to input video file")
    parser.add_argument("--output", "-o", required=True, help="Path to output vertical MP4")
    parser.add_argument("--chunk", "-c", type=int, default=3, help="Words per subtitle chunk")
    parser.add_argument("--font-size", "-f", type=int, default=80, help="Subtitle font size")
    args = parser.parse_args()

    process_video(args.input, args.output, chunk_words=args.chunk, font_size=args.font_size)
