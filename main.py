from selenium import webdriver  # 웹 스크래핑 라이브러리
from selenium.webdriver.common.keys import Keys  # 엔터 키
import time  # 프로그램 작동의 텀을 두는 라이브러리
from bs4 import BeautifulSoup  # html구문을 분석하는 라이브러리
import libg  # Gmail로 답장을 보내는 라이브러
from tkinter import *

root = Tk()
root.title("아주대 홈페이지 모니터링 프로그램")  # GUI 제목: 아주대 공지사항 탐색 프로그램
root.geometry("380x150+500+300")  # 가로 X 세로, X좌표 위치, Y좌표 위치
root.resizable(False, False)


def search_window():  # 검색 위젯 만들기

    search_root = Tk()
    search_root.title("키워드 검색")
    search_root.geometry("300x150+560+340")
    search_root.resizable(False, False)

    search_label = Label(search_root, text='키워드를 입력하세요')
    search_label.grid(row=0, column=0, padx=10, pady=10)

    entry = Entry(search_root, width=20, bd=5)
    entry.grid(row=0, column=1, padx=10, pady=10)

    def Ajou_Notice_search():  # 아주대 공지사항 모니터링 함수
        entry_value = entry.get()
        latest_notice_number = 0  # 내가 찾은 키워드의 공지사항 중 가장 최신 숫자
        driver = webdriver.Chrome(executable_path=r'chromedriver.exe')  # 크롬을 이용한 웹 자동화
        driver.get("https://www.ajou.ac.kr/kr/ajou/notice.do")

        time.sleep(5)

        while True:

            elem = driver.find_element_by_id('search_val')  # 공지사항 검색창의 html 태그의 아이디
            elem.clear()  # 키워드 문구가 중복되지 않도록 하는 작업
            elem.send_keys(entry_value)  # 키워드(토익) 검색창에 입력
            elem.send_keys(Keys.RETURN)  # 검색창에 입력 후 엔터키를 누르는 역할

            html = BeautifulSoup(driver.page_source, 'html.parser')  # html 스타일로 구문 분석
            posts = html.select('div.bn-list-common02.type01.bn-common-cate > table > tbody > tr')

            post_list = []  # 공지사항의 번호, 제목, 공지부서 리스트

            for post in posts:
                post_dic = {'pnum': '', 'ptitle': '', 'pnotice': ''}
                post_dic['pnum'] = post.find_all("td", class_='b-num-box')[0].text.strip()
                post_dic['ptitle'] = post.find_all('a')[0].text.strip()
                post_dic['pnotice'] = post.select('span.b-writer')[0].text

                post_list.append(post_dic)

            if latest_notice_number == 0:  # 첫번째 탐색
                if entry_value == '':
                    email_title = "모니터링 시작했습니다."

                else:
                    email_title = entry_value + "에 관한 모니터링 시작했습니다."

                email_message = post_list[0]['pnum']
                libg.send_gmail('mydasjun09@gmail.com', email_title, email_message)
                latest_notice_number = post_list[0]['pnum']

            else:  # 두번째부터 계속 이 조건문
                for i in range(0, len(post_list)):  # 새로운 공지사항이 안떳을때
                    if int(post_list[i]['pnum']) <= int(latest_notice_number):
                        del post_list[i:]
                        break

                if (len(post_list) > 0):  # 새로운 공지사항이 떳을 때
                    latest_notice_number = post_list[0]['pnum']
                    email_title = "공지사항이 " + str(len(post_list)) + "개 올라왔습니다."
                    for i in range(0, len(post_list)):
                        email_message = post_list[i]['pnum']

                else:  # 새로운 공지사항이 안떳을 때
                    email_title = "아직 공지사항이 올라오지 않았습니다."

                libg.send_gmail('mydasjun09@gmail.com', email_title, email_message)

            time.sleep(1800)

    search_btn = Button(search_root, text="검색", command=Ajou_Notice_search, bd=5)
    search_btn.grid(row=1, column=1, padx=10, pady=10)

    search_root.mainloop()


label1 = Label(root, text="아주대 공지사항 모니터링 클릭 ->")
label1.grid(row=0, column=0, padx=10, pady=10)

btn1 = Button(root, text="NOTICE", command=search_window, bd=5)  # 아주대 공지사항 버튼, 누르면 검색 위젯이 나오게 설정함
btn1.grid(row=0, column=1, padx=10, pady=10)


def login_window():
    login_root = Tk()
    login_root.title("로그인 화면")
    login_root.geometry("300x150+560+340")
    login_root.resizable(False, False)

    ID_label = Label(login_root, text='Username: ')
    ID_label.grid(row=0, column=0, padx=10, pady=10)

    ID_entry = Entry(login_root, bd=5, width=20)
    ID_entry.grid(row=0, column=1, padx=10, pady=10)

    Password_label = Label(login_root, text='Password: ')
    Password_label.grid(row=1, column=0, padx=10, pady=10)

    Password_entry = Entry(login_root, bd=5, width=20, show='*')
    Password_entry.grid(row=1, column=1, padx=10, pady=10)

    def search_Ajou_Email():  # 아주대 이메일 모니터링 함수
        ID_value = ID_entry.get()
        Password_value = Password_entry.get()
        email_number = 0

        while True:

            driver = webdriver.Chrome(executable_path=r'chromedriver.exe')
            driver.get("https://mportal.ajou.ac.kr/main.do")

            time.sleep(5)

            elem = driver.find_element_by_xpath("//*[@id='nbHeaderContext']/div[1]/div[1]/div[1]/ul/li/a")
            elem.click()

            time.sleep(5)

            id_element = driver.find_element_by_xpath("//*[@id='userId']")
            id_element.send_keys(ID_value)

            password_element = driver.find_element_by_xpath("//*[@id='password']")
            password_element.send_keys(Password_value)

            login_element = driver.find_element_by_xpath("//*[@id='loginSubmit']")
            login_element.click()

            if email_number == 0:

                email_number = driver.find_element_by_xpath(
                    "//*[@id='P031']/div/div/div/div/div/header/h2/span/i/em/span[1]").text.strip()
                email_title = "아주대 이메일 모니터링 시작"
                libg.send_gmail("mydasjun09@gmail.com", email_title, "내용 없음")
                print(email_number)

            else:
                if driver.find_element_by_xpath(
                        "//*[@id='P031']/div/div/div/div/div/header/h2/span/i/em/span[1]").text.strip() != email_number:
                    temp = int(driver.find_element_by_xpath(
                        "//*[@id='P031']/div/div/div/div/div/header/h2/span/i/em/span[1]").text.strip())
                    email_count = temp - int(email_number)
                    email_title = "새로 올라온 이메일의 개수: " + str(email_count)
                    libg.send_gmail("mydasjun09@gmail.com", email_title, "내용 없음")
                    print(email_title)

            driver.quit()
            time.sleep(1800)

    login_btn = Button(login_root, text="Login", command=search_Ajou_Email, bd=5)
    login_btn.grid(row=2, column=1, padx=10, pady=10)

    login_root.mainloop()


label2 = Label(root, text="아주대 이메일 모니터링 클릭 ->")
label2.grid(row=1, column=0, padx=10, pady=10)

btn2 = Button(root, text="AJOU-EMAIL", command=login_window, bd=5)
btn2.grid(row=1, column=1, padx=10, pady=10)
root.mainloop()