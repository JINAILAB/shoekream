import requests
import pymysql
import time

# 데이터베이스 연결 설정
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='qaz010010!',
                             database='shoe_kream',
                             charset='utf8mb4')
cursor = connection.cursor()

# 크롤링 설정
base_url = "https://kream.co.kr/api/p/tabs/all/?cursor={}&shop_category_id=34&request_key=4bb0bab2-fc50-4085-9b8a-6231439cb07e"
headers = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Referer": "https://kream.co.kr/search?shop_category_id=34",
    "X-Kream-Api-Version": "21",
    "X-Kream-Client-Datetime": "20230907095353+0900",
    "X-Kream-Device-Id": "web;03979551-0f79-4dd3-a053-204bf2a61b9c"
}

cursor_value = 1

## current price를 위한 함수
def get_price(data):
    if data.get('local_price'):
        return data['local_price']
    elif data.get('original_price'):
        return data['original_price']
    else:
        return None

while True:
    start_time = time.time()
    response = requests.get(base_url.format(cursor_value), headers=headers)
    data = response.json()
    
    # 아이템이 없으면 크롤링 종료
    if not data['items']:
        break

    for item in data['items']:
        
        # 'display_type' 키가 'content'인 아이템은 건너뜁니다.
        if item.get('display_type') == 'content':
            continue
        release = item['product']['release']
        brand = item['product']['brand']
        counter = item['product']['counter']
        
        
        # 필요한 데이터 추출
        id = release['id']
        shoe_name = release['name']
        shoe_category = release['category']
        original_price_with_currency = get_price(release)
        date_released = release['date_released']
        if date_released:
            date_released = date_released.split('T')[0]  # 시간 제거
        else:
            date_released = None 
        colorway = release['colorway']
        gender = release['gender']
        brand = brand['name']
        wish_count = counter['wish_count']
        review_count = counter['review_count']
        image_urls = release['image_urls']
        while len(image_urls) < 3:
            image_urls.append(None)


        # 데이터베이스에 저장
        insert_query = """
        INSERT INTO shoes (id, shoe_name, shoe_category, original_price_with_currency, date_released, colorway, gender, brand, wish_count, review_count, image_url_right, image_url_left, image_url_top)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        
        # 중복된 기본 키 값 체크
        cursor.execute("SELECT 1 FROM shoes WHERE id = %s", (id,))
        if cursor.fetchone():  # 해당 기본 키 값이 이미 존재하면
            continue  # 현재 반복을 건너뜀

        cursor.execute(insert_query, (id, shoe_name, shoe_category, original_price_with_currency, date_released, colorway, gender, brand, wish_count, review_count, *image_urls[:3]))
        connection.commit()
    
    time.sleep(5)
    cursor_value += 1
    end_time = time.time()
    time_take = end_time - start_time
    print(cursor_value, '/'+'400', 'progress')
    print('time_left:', time_take * (800-(cursor_value)))
        

# 데이터베이스 연결 종료
cursor.close()
connection.close()