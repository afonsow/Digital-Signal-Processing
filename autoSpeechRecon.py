import os
import serial
import speech_recognition as sr

def audio_to_text(audio_file, language="pt-PT"):
    recognizer = sr.Recognizer()
    try:
        audio_file_path = os.path.join(os.getcwd(), audio_file)
        if not os.path.exists(audio_file_path):
            return None, f"Ficheiro não encontrado: {audio_file_path}"

        with sr.AudioFile(audio_file_path) as source:
            print("A carregar o áudio...")
            audio_data = recognizer.record(source)

        print("A reconhecer o texto...")
        text = recognizer.recognize_google(audio_data, language=language)
        return text, None
    except sr.UnknownValueError:
        return None, "Não foi possível reconhecer o áudio."
    except sr.RequestError as e:
        return None, f"Erro ao conectar ao serviço de reconhecimento: {e}"
    except Exception as e:
        return None, f"Erro inesperado: {e}"

if __name__ == "__main__":
    # Configuração da porta Serial 
    arduino_port = "COM11"  
    baud_rate = 115200
    ser = serial.Serial(arduino_port, baud_rate)
    print(f"Conectado ao Arduino na porta {arduino_port}.")

    try:
        while True:
            # Receber o nome do ficheiro do utilizador
            audio_file = input("Insira o nome do ficheiro de áudio (no mesmo diretório): ").strip()

            # Processar o áudio
            extracted_text, error = audio_to_text(audio_file, language="pt-PT")

            if error:
                print(error)
            else:
                print(f"Texto reconhecido: {extracted_text}")
                
                # Enviar o texto para o Arduino
                ser.write((extracted_text + "\n").encode('utf-8'))
                print("Texto enviado para o Arduino.")
    except KeyboardInterrupt:
        print("A encerrar...")
    finally:
        ser.close()
