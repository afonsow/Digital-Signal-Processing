import sys
from pydub import AudioSegment
from scipy.signal import lfilter
import numpy as np
import wave

def high_pass_filter(samples, alpha=0.0104):
    filtered_samples = []
    prev_sample = 0
    prev_output = 0
    for sample in samples:
        high_pass_sample = sample - alpha * prev_sample + alpha * prev_output
        filtered_samples.append(high_pass_sample)
        prev_output = high_pass_sample
        prev_sample = sample
    return np.array(filtered_samples, dtype=np.int16)

def low_pass_filter(samples, alpha=0.5115):
    filtered_samples = []
    prev_output = 0
    for sample in samples:
        low_pass_sample = alpha * sample + (1 - alpha) * prev_output
        filtered_samples.append(low_pass_sample)
        prev_output = low_pass_sample
    return np.array(filtered_samples, dtype=np.int16)

def band_pass_filter(samples, low_alpha=0.5115, high_alpha=0.0104):
    low_passed = low_pass_filter(samples, alpha=low_alpha)
    band_passed = high_pass_filter(low_passed, alpha=high_alpha)
    return band_passed

def process_audio(input_file):
    try:
        # Carregar o arquivo de áudio
        audio = AudioSegment.from_file(input_file)
        samples = np.array(audio.get_array_of_samples())


        # Aplicar filtro passa-banda
        #  alpha = 2π * fc / sample_rate + 2π * fc
        # Banda -> 80 Hz - 8 KHz 
        # Sample rate: 48 KHz
        filtered_samples = band_pass_filter(samples, low_alpha=0.5115, high_alpha=0.0104)


        # Gerar o nome do arquivo de saída
        output_file = input_file.rsplit('.', 1)[0] + "_filtered.wav"

        # Salvar o áudio filtrado
        with wave.open(output_file, "w") as wf:
            wf.setnchannels(audio.channels)
            wf.setsampwidth(audio.sample_width)
            wf.setframerate(audio.frame_rate)
            wf.writeframes(filtered_samples.tobytes())

        print(f"Áudio filtrado salvo como: {output_file}")
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python band_pass_filter.py <nome_do_arquivo>")
        sys.exit(1)

    input_file = sys.argv[1]
    process_audio(input_file)
