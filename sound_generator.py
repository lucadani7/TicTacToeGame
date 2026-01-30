import math
import struct
import wave

from constants import SOUND_DIR


class SoundGenerator:
    @staticmethod
    def create_sound(filename, duration, freq_list):
        """
        Generates a sound file based on the given specifications and saves it to disk. The sound file
        is created in WAV format with a sample rate of 44,100 Hz, a single audio channel, and a
        specific frequency pattern determined by the provided list of frequencies.

        :param filename: Name of the sound file to be created as a string with the appropriate
            file extension (typically '.wav').
        :param duration: Duration of the sound in seconds (type: float).
        :param freq_list: List of frequencies (in Hz) to be used for the sound generation.
            Each frequency corresponds to a slice of the sound duration.
        :return: None
        """
        folder = SOUND_DIR
        full_path = folder / filename
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        with wave.open(str(full_path), 'w') as obj:
            obj.setnchannels(1)
            obj.setsampwidth(2)
            obj.setframerate(sample_rate)
            for i in range(n_samples):
                t = i / n_samples
                idx = int(t * len(freq_list))
                freq = freq_list[min(idx, len(freq_list) - 1)]
                value = int(32767.0 * 0.5 * math.sin(2.0 * math.pi * freq * i / sample_rate))
                data = struct.pack('<h', value)
                obj.writeframesraw(data)
        print(f"Sound file {filename} created successfully.")

    @staticmethod
    def generate_sound():
        """
        Generates sound files in the specified directory with predefined properties.

        This static method creates a folder for sound files (if it does not already
        exist) and generates several sound files with specific configurations. Each
        generated sound file has its own designated name, duration, and sequence
        of frequencies.

        :raises FileNotFoundError: If the specified sound directory cannot be created.
        :raises ValueError: If invalid parameters are passed to the sound generator.
        """
        folder = SOUND_DIR
        folder.mkdir(parents=True, exist_ok=True)
        print(f"Sound folder ready: {folder}")
        print("Generating sounds...")
        SoundGenerator.create_sound("move.wav", 0.1, [400, 600])
        SoundGenerator.create_sound("win.wav", 0.4, [400, 500, 600, 800, 1000])
        SoundGenerator.create_sound("over.wav", 0.4, [300, 250, 200, 150, 100])
        print("Sounds generated successfully.")