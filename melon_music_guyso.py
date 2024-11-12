import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

# 시작 날짜 설정 (2024년 1월 1일)
start_date = datetime(2024, 1, 1)

# 사용자가 원하는 마지막 주차 입력
end_week = int(input("크롤링할 마지막 주차를 입력하세요: "))

# 반복문을 사용하여 각 주차의 데이터를 크롤링
for week_number in range(1, end_week + 1):
    # 각 주차의 시작 날짜 계산
    delta = timedelta(weeks=week_number - 1)
    chart_date = start_date + delta

    # URL 설정
    url = "https://xn--o39an51b2re.com/chart/melon/weekly/2024/{week_number}"

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

                if ranking and title and artist :
                    data.append({'Rank': ranking, 'Title': title, 'Artist': artist, 'Date': chart_date.strftime('%Y-%m-%d')})
            except (AttributeError, KeyError) as e:
                print(f"데이터 추출 중 오류 발생: {e}")

        # 데이터프레임 생성
        df = pd.DataFrame(data)

        # CSV 파일로 저장 (날짜 포함)
        file_name = f'melon_chart_data_{chart_date.strftime("%Y-%m-%d")}.csv'
        df.to_csv(file_name, index=False, encoding='utf-8-sig')
        print(f"CSV 파일로 저장되었습니다: {file_name}")
    else:
        print(f"Failed to retrieve data from {url}, status code: {response.status_code}")
