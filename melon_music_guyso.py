import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import random

# 시작 날짜 설정 (2024년 1월 1일)
start_date = datetime(2024, 1, 1)

# 사용자가 원하는 마지막 주차 입력
end_week = int(input("크롤링할 마지막 주차를 입력하세요: "))

# User-Agent 리스트 (주기적으로 변경)
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
]

# 요청 제한 설정
request_limit = 5  # 한 번에 보낼 최대 요청 수
request_count = 0   # 현재까지 보낸 요청 수

# 반복문을 사용하여 각 주차의 데이터를 크롤링
for week_number in range(1, end_week + 1):
    # 각 주차의 시작 날짜 계산
    delta = timedelta(weeks=week_number - 1)
    chart_date = start_date + delta

    # URL 설정
    url = f"https://xn--o39an51b2re.com/chart/melon/weekly/2024/{week_number}"

    # 랜덤 User-Agent 선택
    headers = {'User-Agent': random.choice(user_agents)}

    try:
        # HTTP GET 요청으로 페이지 가져오기
        response = requests.get(url, headers=headers)

        # 응답이 성공적(200)일 경우에만 진행
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # 데이터를 저장할 리스트 초기화
            data = []

            # 데이터 추출 로직 (예시)
            for row in soup.find_all('tr'):
                ranking_tag = row.find('td', class_='ranking')
                ranking = ranking_tag.find('p').text.strip() if ranking_tag else None

                subject = row.find('td', class_='subject')
                title = subject.find('p', title=True)['title'].strip() if subject else None
                artist = subject.find('p', class_='singer').text.strip() if subject else None

                if ranking and title and artist:
                    data.append({'Rank': ranking, 'Title': title, 'Artist': artist, 'Date': chart_date.strftime('%Y-%m-%d')})

            # 데이터프레임 생성 및 CSV 파일로 저장
            df = pd.DataFrame(data)
            file_name = f'melon_chart_data_{chart_date.strftime("%Y-%m-%d")}.csv'
            df.to_csv(file_name, index=False, encoding='utf-8-sig')
            print(f"CSV 파일로 저장되었습니다: {file_name}")

        else:
            print(f"Failed to retrieve data from {url}, status code: {response.status_code}")

        # 요청 횟수 증가
        request_count += 1

        # 요청이 5번 이루어지면 대기 시간 추가 (예: 60초 대기)
        if request_count >= request_limit:
            print(f"{request_limit}개의 요청이 완료되었습니다. 60초 동안 대기합니다.")
            time.sleep(60)  # 60초 대기
            request_count = 0  # 요청 카운트 초기화

    except Exception as e:
        print(f"요청 중 오류 발생: {e}")

    # 랜덤 지연 시간 추가 (2~5초 사이)
    time.sleep(random.uniform(2, 5))
