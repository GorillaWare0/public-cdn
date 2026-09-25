"""Generate the original GorillaWare 4.4 soundboard starter pack.

All sounds are synthesized here; no recordings or third-party samples are used.
"""

import math
import random
import struct
import wave
from pathlib import Path


RATE = 16000
ROOT = Path(__file__).resolve().parents[1] / "default"


def render(path, seconds, voice):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    rng = random.Random(path)
    total = int(seconds * RATE)
    samples = []
    previous = 0.0
    for index in range(total):
        t = index / RATE
        attack = min(1.0, t * 24.0)
        release = min(1.0, (seconds - t) * 8.0)
        envelope = max(0.0, attack * release)
        noise = rng.uniform(-1.0, 1.0)
        previous = previous * 0.985 + noise * 0.015
        value = voice(t, previous, noise) * envelope
        samples.append(struct.pack("<h", int(max(-1.0, min(1.0, value)) * 18000)))
    with wave.open(str(target), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(RATE)
        output.writeframes(b"".join(samples))


def pulse(t, center, width):
    return math.exp(-((t - center) / width) ** 2)


def sine(freq, t):
    return math.sin(2.0 * math.pi * freq * t)


render("Ghost/cold-drone.wav", 8, lambda t, low, noise: 0.22 * (sine(63, t) + 0.5 * sine(95 + 1.5 * sine(0.19, t), t)) + low * 0.2)
render("Ghost/whisper-wind.wav", 5, lambda t, low, noise: (noise * 0.10 + low * 0.9) * (0.4 + 0.3 * sine(1.3, t)))
render("Ghost/hollow-steps.wav", 5, lambda t, low, noise: sum(pulse(t, c, 0.055) * (noise * 0.35 + sine(75, t) * 0.2) for c in (0.7, 1.35, 2.2, 3.0, 4.1)))
render("Ghost/distant-knocks.wav", 4, lambda t, low, noise: sum(pulse(t, c, 0.08) * (sine(130, t) * 0.5 + noise * 0.15) for c in (0.7, 1.05, 2.6)))
render("Ghost/reveal-stinger.wav", 2, lambda t, low, noise: pulse(t, 0.32, 0.22) * (sine(58, t) * 0.65 + sine(437, t) * 0.2 + noise * 0.18))
render("Ghost/uneasy-chimes.wav", 6, lambda t, low, noise: sum(pulse(t, c, 0.8) * sine(f, t) * 0.24 for c, f in ((0.6, 391), (2.0, 463), (3.4, 349), (4.7, 415))))
render("Trolling/spring-boing.wav", 2, lambda t, low, noise: pulse(t, 0.6, 0.47) * sine(220 + 110 * sine(4, t), t) * 0.55)
render("Trolling/cartoon-pop.wav", 1.5, lambda t, low, noise: pulse(t, 0.45, 0.09) * (sine(260 - 100 * t, t) * 0.6 + noise * 0.18))
render("Trolling/rubber-squeak.wav", 2, lambda t, low, noise: pulse(t, 0.8, 0.6) * sine(520 + 90 * sine(6, t), t) * 0.35)
render("Trolling/comic-bloop.wav", 2, lambda t, low, noise: sum(pulse(t, c, 0.2) * sine(f, t) * 0.4 for c, f in ((0.45, 420), (0.8, 310), (1.15, 195))))
render("Music/haunted-loop.wav", 8, lambda t, low, noise: sum(sine(f, t) * 0.09 for f in (65.4, 98.1, 116.5)) * (0.7 + 0.3 * sine(0.125, t)))
render("Music/playful-loop.wav", 8, lambda t, low, noise: sum(pulse(t, c, 0.22) * sine(f, t) * 0.24 for c, f in ((0.5, 262), (1.5, 330), (2.5, 392), (3.5, 330), (4.5, 262), (5.5, 392), (6.5, 330), (7.3, 262))))
