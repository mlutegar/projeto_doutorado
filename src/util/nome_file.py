from collections import defaultdict
from datetime import datetime

def process_files(files):
    processed_files = defaultdict(list)

    for file in files:
        # Extraindo informações do nome do arquivo
        parts = file.split("_")
        if len(parts) < 3:
            continue  # Ignorar arquivos que não seguem o formato esperado

        nome = parts[0]
        raw_date = parts[1]
        raw_time = parts[2].split(".")[0]

        # Convertendo data e hora
        try:
            date = datetime.strptime(raw_date, "%Y-%m-%d").date()
            time = datetime.strptime(raw_time, "%H%M%S").time()
        except ValueError:
            continue  # Ignorar arquivos com formatos inválidos

        # Adicionando ao agrupamento por data
        formatted_time = time.strftime("%H:%M")
        processed_files[date].append({
            "name": nome,
            "time": formatted_time,
            "original": file,
        })

    return processed_files
