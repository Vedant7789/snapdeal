
from faster_whisper import WhisperModel


# Load the model once when the service starts.
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


def transcribe_audio(audio_path: str) -> str:

    segments, info = model.transcribe(
        audio_path,
        beam_size=5,
        language="en"
    )

    transcript = " ".join(
        segment.text.strip()
        for segment in segments
    )

    return transcript.strip()
