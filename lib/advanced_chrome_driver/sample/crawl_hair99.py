from lib.advanced_chrome_driver.advanced_chrome_driver import AdvancedChromeDriver
from pandas import DataFrame

driver = AdvancedChromeDriver(headless=False)

# 구직자
driver.get('http://www.hair99.co.kr/bbs/board.php?bo_table=gu_in')
driver.wait_until_xpath('//*[@id="guin"]/table')

global df
df = DataFrame(columns=['이름', '연락처1', '이메일', '주소'])

global start_page
start_page = 1


def nextpage(current_page: int):
    print(f'다음 페이지로 넘기기 시작합니다. 현재 페이지: {current_page}')
    button_index = 0
    if current_page == 1:
        button_index = 1
    elif current_page < 10:
        button_index = 2
    else:
        button_index = 3

    try:
        driver.click_xpath(
            f'//*[@id="guin"]/div[2]/a[{button_index}]')
    except Exception as e:
        print('다음 페이지가 없습니다... 현재 페이지: ', current_page)
        raise e


def read_page():
    trs = driver.find_elements_by_xpath('//*[@id="guin"]/table/tbody/tr')

    def read_row(i, count=0):
        global df

        if count > 2:
            print('안됫지만 계속합시다...')
            return
        try:
            driver.click_xpath(
                f'//*[@id="guin"]/table/tbody/tr[{i}]/td[3]/span/a')
            name = driver.wait_and_get_text(
                '//*[@id="peoview_name"]/span', 20)
            phone = driver.wait_and_get_text(
                '//*[@id="peoview_table"]/table/tbody/tr[1]/td[3]/span')
            email = driver.wait_and_get_text(
                '//*[@id="peoview_table"]/table/tbody/tr[4]/td[3]/span')
            address = driver.wait_and_get_text(
                '//*[@id="peoview_table"]/table/tbody/tr[5]/td[3]/span')
            print(name, phone, email, address)
            df = df.append(
                [{'이름': name, '연락처1': phone, '이메일': email, '주소': address}])
            driver.back()
        except:
            print(f'클릭안먹어서 재시도함... 횟수: {count}')
            return read_row(i, count+1)

    for i in range(len(trs)):
        if i == 0:
            continue
        read_row(i)

    df.to_excel(f'out/구인페이지_p{start_page}~.xlsx')


def process(i):
    print(f'{i}번 페이지를 처리중입니다...')
    read_page()
    nextpage(i)
    return process(i+1)


# 68페이지까지 넘김
for i in range(start_page-1):
    nextpage(i+1)

process(start_page)
