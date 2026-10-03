import numpy as np
import sounddevice as sd


class AudioEngine:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.stream = sd.OutputStream(
            samplerate=sample_rate, channels=1, dtype="float32"
        )
        self.stream.start()

    def play_tone(self, val, max_val, duration=0.006, amplitude=0.25):
        if val is None or (hasattr(val, "__len__") and len(val) == 0):
            return

        val_arr = np.atleast_1d(val)

        min_f, max_f = 100.0, 360.0
        freqs = min_f + (val_arr / max_val) * (max_f - min_f)

        t = np.linspace(
            0,
            duration,
            int(self.sample_rate * duration),
            endpoint=False,
            dtype=np.float32,
        )

        # Effet Glorp
        k = 550.0
        phase = 2.0 * np.pi * freqs[:, None] * (t + (1.5 / k) * (1.0 - np.exp(-k * t)))

        fm_mod = 0.45 * np.sin(1.8 * phase)
        carrier = np.sin(phase + fm_mod) + 0.3 * np.sin(0.5 * phase)

        # Remplacer l'enveloppe exponentielle par quelque chose de plus doux
        envelope = np.sin(np.linspace(0, np.pi, len(t), dtype=np.float32))

        tones = amplitude * carrier * envelope
        wave = np.mean(tones, axis=0).astype(np.float32)

        wave = np.nan_to_num(wave)
        wave = np.clip(wave, -0.85, 0.85)

        try:
            self.stream.write(wave)
        except Exception:
            pass

    def close(self):
        self.stream.stop()
        self.stream.close()
