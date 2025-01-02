import requests
import base64

def download_by_file_id(bot_token, file_id):
    api_url = f"https://api.telegram.org/bot{bot_token}"

    get_file_url = f"{api_url}/getFile?file_id={file_id}"
    print(f"Получаем путь к файлу: {get_file_url}")
    response = requests.get(get_file_url)
    
    if response.status_code == 200:
        file_info = response.json().get("result", {})
        file_path = file_info.get("file_path")
        
        if file_path:
            file_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
            print(f"URL для скачивания файла: {file_url}")
            
            file_response = requests.get(file_url)
            if file_response.status_code == 200:
                return file_response.content 
            else:
                raise Exception(f"Ошибка при загрузке файла: {file_response.status_code}")
        else:
            raise Exception("Не удалось получить путь к файлу.")
    else:
        raise Exception(f"Ошибка при получении информации о файле: {response.status_code}")


BOT_TOKEN = "YOUR_BOT_TOKEN"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

method = "getAvailableGifts"

response = requests.get(f"{API_URL}/{method}")
print(f"Запрос к API: {API_URL}/{method}")

if response.status_code == 200:
    data = response.json()
    if data.get("ok"):
        gifts = data.get("result", {}).get("gifts", [])

        html_output = """
        <html>
        <head>
            <title>Доступные подарки</title>
            <style>
                table {border-collapse: collapse; width: 100%;}
                th, td {border: 1px solid #ddd; padding: 8px; text-align: left;}
                th {background-color: #f2f2f2;}
            </style>
        </head>
        <body>
            <h1>Доступные подарки</h1>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Emoji</th>
                    <th>Thumbnail</th>
                    <th>Star Count</th>
                    <th>Remaining Count</th>
                    <th>Total Count</th>
                </tr>
        """

        for gift in gifts:
            sticker = gift.get("sticker", {})
            emoji = sticker.get("emoji", "")
            thumbnail_file_id = sticker.get("thumbnail", {}).get("file_id", "")
            star_count = gift.get("star_count", "N/A")
            remaining_count = gift.get("remaining_count", "N/A")
            total_count = gift.get("total_count", "N/A")

            print(f"Получаем mini-изображение для file_id: {thumbnail_file_id}")
            thumbnail_image = download_by_file_id(BOT_TOKEN, thumbnail_file_id)

            thumbnail_base64 = base64.b64encode(thumbnail_image).decode('utf-8')

            html_output += f"""
                <tr>
                    <td>{gift.get('id', 'N/A')}</td>
                    <td>{emoji}</td>
                    <td><img src="data:image/jpeg;base64,{thumbnail_base64}" width="100" height="100" alt="Thumbnail"></td>
                    <td>{star_count}</td>
                    <td>{remaining_count}</td>
                    <td>{total_count}</td>
                </tr>
            """

        html_output += """
            </table>
        </body>
        </html>
        """

        with open("gifts_table.html", "w", encoding="utf-8") as file:
            file.write(html_output)

        print("HTML файл с таблицей подарков был успешно создан.")
    else:
        print("Ошибка:", data.get("description"))
else:
    print("HTTP ошибка:", response.status_code)
