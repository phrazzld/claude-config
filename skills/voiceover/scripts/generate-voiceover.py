#!/usr/bin/env python3
"""Generate ElevenLabs voiceover audio and optional word timestamps."""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import requests

API_ROOT = "https://api.elevenlabs.io/v1"
DEFAULT_MODEL = "eleven_multilingual_v2"
OUTPUT_AUDIO = Path("voiceover.mp3")
OUTPUT_TIMESTAMPS = Path("timestamps.json")

# Common, stable starter voices. If a value is already an ID, we pass it through.
VOICE_NAME_TO_ID = {
    "adam": "pNInz6obpgDQGcFmaJgB",
    "rachel": "21m00Tcm4TlvDq8ikWAM",
    "josh": "TxGEqnHWrfWFTfGW9XjX",
    "bella": "EXAVITQu4vr4xnSDxMaL",
    "antoni": "ErXwobaYiN019PkySvjV",
}

ACRONYM_EXPANSIONS = {
    "API": "A P I",
    "UI": "U I",
    "UX": "U X",
    "TTS": "T T S",
    "AI": "A I",
    "ML": "M L",
    "SQL": "S Q L",
    "SaaS": "SaaS",
    "B2B": "B to B",
    "B2C": "B to C",
    "FAQ": "F A Q",
    "ETA": "E T A",
    "CEO": "C E O",
    "CTO": "C T O",
    "CFO": "C F O",
    "GPU": "G P U",
    "CPU": "C P U",
}


@dataclass(frozen=True)
class Alignment:
    characters: list[str]
    start_seconds: list[float]
    duration_seconds: list[float]


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a voiceover with ElevenLabs."
    )
    parser.add_argument(
        "script",
        help="Script text or a path to a text/markdown file.",
    )
    parser.add_argument(
        "--voice",
        default="adam",
        help="Voice name or voice ID. Default: adam.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"ElevenLabs model ID. Default: {DEFAULT_MODEL}.",
    )
    parser.add_argument(
        "--timestamps",
        action="store_true",
        help="Return word-level timestamps to timestamps.json.",
    )
    parser.add_argument(
        "--out",
        default=str(OUTPUT_AUDIO),
        help=f"Output audio file path. Default: {OUTPUT_AUDIO}.",
    )
    parser.add_argument(
        "--timestamps-out",
        default=str(OUTPUT_TIMESTAMPS),
        help=f"Output timestamps path. Default: {OUTPUT_TIMESTAMPS}.",
    )
    return parser.parse_args(list(argv))


def read_script(script_arg: str) -> str:
    candidate = Path(script_arg).expanduser()
    if candidate.exists() and candidate.is_file():
        return candidate.read_text(encoding="utf-8").strip()
    return script_arg.strip()


def expand_acronyms(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        token = match.group(0)
        return ACRONYM_EXPANSIONS.get(token, token)

    pattern = r"\b(" + "|".join(map(re.escape, ACRONYM_EXPANSIONS)) + r")\b"
    return re.sub(pattern, repl, text)


def normalize_large_numbers(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        raw = match.group(0)
        try:
            return f"{int(raw):,}"
        except ValueError:
            return raw

    # Only touch long integers; keep years like 2026 intact by requiring 5+ digits.
    return re.sub(r"\b\d{5,}\b", repl, text)


def preprocess_text(text: str) -> str:
    text = expand_acronyms(text)
    text = normalize_large_numbers(text)
    return text


def resolve_voice_id(voice: str) -> str:
    if voice in VOICE_NAME_TO_ID:
        return VOICE_NAME_TO_ID[voice]
    return voice


def build_headers(api_key: str, accept: str) -> dict[str, str]:
    return {
        "xi-api-key": api_key,
        "Accept": accept,
        "Content-Type": "application/json",
    }


def build_payload(text: str, model_id: str) -> dict:
    return {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True,
        },
    }


def request_tts(
    api_key: str,
    voice_id: str,
    payload: dict,
    timestamps: bool,
) -> requests.Response:
    if timestamps:
        url = f"{API_ROOT}/text-to-speech/{voice_id}/with-timestamps"
        accept = "application/json"
    else:
        url = f"{API_ROOT}/text-to-speech/{voice_id}"
        accept = "audio/mpeg"

    response = requests.post(
        url,
        headers=build_headers(api_key, accept),
        json=payload,
        timeout=90,
    )
    return response


def decode_audio_from_json(data: dict) -> bytes:
    audio_b64 = data.get("audio_base64")
    if not audio_b64:
        raise ValueError("Missing audio_base64 in ElevenLabs response.")
    return base64.b64decode(audio_b64)


def extract_alignment(data: dict) -> Alignment | None:
    alignment = data.get("alignment") or {}
    chars = alignment.get("characters")
    starts = alignment.get("character_start_times_seconds")
    durations = alignment.get("character_durations_seconds")
    if not (chars and starts and durations):
        return None
    return Alignment(
        characters=list(chars),
        start_seconds=list(starts),
        duration_seconds=list(durations),
    )


def char_is_word(ch: str) -> bool:
    return ch.isalnum() or ch in {"'", "’"}


def words_from_alignment(alignment: Alignment) -> list[dict]:
    words: list[dict] = []
    current_chars: list[str] = []
    current_start: float | None = None
    current_end: float | None = None

    for ch, start, dur in zip(
        alignment.characters, alignment.start_seconds, alignment.duration_seconds
    ):
        end = start + dur
        if char_is_word(ch):
            if current_start is None:
                current_start = start
            current_chars.append(ch)
            current_end = end
            continue

        if current_chars and current_start is not None and current_end is not None:
            word = "".join(current_chars)
            words.append(
                {
                    "word": word,
                    "start": round(current_start, 3),
                    "end": round(current_end, 3),
                }
            )
        current_chars = []
        current_start = None
        current_end = None

    if current_chars and current_start is not None and current_end is not None:
        word = "".join(current_chars)
        words.append(
            {
                "word": word,
                "start": round(current_start, 3),
                "end": round(current_end, 3),
            }
        )

    return words


def save_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main(argv: Iterable[str]) -> int:
    args = parse_args(argv)
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("Error: ELEVENLABS_API_KEY is not set.", file=sys.stderr)
        return 2

    raw_script = read_script(args.script)
    if not raw_script:
        print("Error: empty script.", file=sys.stderr)
        return 2

    text = preprocess_text(raw_script)
    voice_id = resolve_voice_id(args.voice)
    payload = build_payload(text, args.model)

    try:
        response = request_tts(api_key, voice_id, payload, args.timestamps)
    except requests.RequestException as exc:
        print(f"Network error calling ElevenLabs: {exc}", file=sys.stderr)
        return 1

    if response.status_code >= 400:
        detail = response.text.strip()
        print(
            f"ElevenLabs API error ({response.status_code}): {detail}",
            file=sys.stderr,
        )
        return 1

    out_audio = Path(args.out).expanduser()
    timestamps_out = Path(args.timestamps_out).expanduser()

    if args.timestamps:
        data = response.json()
        try:
            audio_bytes = decode_audio_from_json(data)
        except (ValueError, base64.binascii.Error) as exc:
            print(f"Failed to decode audio: {exc}", file=sys.stderr)
            return 1
        save_bytes(out_audio, audio_bytes)

        alignment = extract_alignment(data)
        if alignment is None:
            print(
                "Warning: alignment missing; writing empty timestamps.",
                file=sys.stderr,
            )
            words: list[dict] = []
        else:
            words = words_from_alignment(alignment)

        save_json(
            timestamps_out,
            {
                "voice": args.voice,
                "voice_id": voice_id,
                "model_id": args.model,
                "text": text,
                "words": words,
            },
        )
    else:
        save_bytes(out_audio, response.content)

    print(f"Wrote audio: {out_audio}")
    if args.timestamps:
        print(f"Wrote timestamps: {timestamps_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
