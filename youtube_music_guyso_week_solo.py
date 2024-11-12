import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

# URL 설정
url = "https://xn--o39an51b2re.com/chart/youtube/track-weekly/2024/44"

# 2024년 1월 1일을 기준으로 44주차의 시작 날짜 계산
start_date = datetime(2023, 12, 29)
week_number = 44
delta = timedelta(weeks=week_number - 1)
chart_date = start_date + delta

# HTTP GET 요청으로 페이지 가져오기
response = requests.get(url)

# 응답이 성공적(200)일 경우에만 진행
if response.status_code == 200:
    # HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # 데이터를 저장할 리스트 초기화
    data = []

    # <tr> 요소를 각각 순회하며 순위, 제목, 아티스트, 조회수 추출
    rows = soup.find_all('tr')
    for row in rows:
        try:
            # 순위 추출: <td class="ranking"> 내 첫 번째 <p> 태그
            ranking_tag = row.find('td', class_='ranking')
            ranking = ranking_tag.find('p').text.strip() if ranking_tag else None

            # 제목과 아티스트 추출
            subject = row.find('td', class_='subject')
            title = subject.find('p', title=True)['title'].strip() if subject else None
            artist = subject.find('p', class_='singer').text.strip() if subject else None

            # 조회수 추출
            count_tag = row.find('td', class_='count')
            views = count_tag.text.strip() if count_tag else None

            if ranking and title and artist and views:
                data.append({'Rank': ranking, 'Title': title, 'Artist': artist, 'Views': views, 'Date': chart_date.strftime('%Y-%m-%d')})
        except (AttributeError, KeyError) as e:
            print(f"데이터 추출 중 오류 발생: {e}")

    # 데이터프레임 생성
    df = pd.DataFrame(data)

    # CSV 파일로 저장 (날짜 포함)
    file_name = f'chart_data_{chart_date.strftime("%Y-%m-%d")}.csv'
    df.to_csv(file_name, index=False, encoding='utf-8-sig')
    print(f"CSV 파일로 저장되었습니다: {file_name}")
else:
    print(f"Failed to retrieve data from {url}, status code: {response.status_code}")
