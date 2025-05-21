import json
import re

def remove_duplicates_and_save(file_path):
    # Чтение данных из файла
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    # Собираем все уникальные ссылки
    unique_urls = list({url for url in lines})

    # Группируем по ID, удаляя дубликаты
    grouped_data = {"groups": []}
    id_pattern = re.compile(r'id=(\d+)')
    current_id = None
    current_group = []

    for url in unique_urls:
        id_match = id_pattern.search(url)
        if id_match:
            if current_id is not None:
                grouped_data["groups"].append({
                    "id": current_id,
                    "urls": current_group
                })
            current_id = id_match.group(1)
            current_group = [url]
        else:
            current_group.append(url)

    # Добавляем последнюю группу
    if current_id is not None:
        grouped_data["groups"].append({
            "id": current_id,
            "urls": current_group
        })

    # Сохраняем результат
    with open("unique_grouped_links.json", "w", encoding='utf-8') as f:
        json.dump(grouped_data, f, ensure_ascii=False, indent=2)

    print("Дубликаты удалены. Результат в unique_grouped_links.json")

# Запуск обработки
remove_duplicates_and_save("saved.txt")