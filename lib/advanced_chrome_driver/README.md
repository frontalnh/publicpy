# 파이썬 크롤링을 위한 크롬 드라이버 유틸 라이브러리

파이썬과 셀레니움을 이용한 브라우저 자동화를 통해 웹사이트 크롤링에 필요한 모듈입니다.

실제로 크롤링을 할때에는 상당히 번거롭고 또 반복적인 작업이 필요합니다.

단순히 웹사이트의 정보뿐 아니라, 로그인, 스크롤, 팝업제어 처럼 여러 작업을 거쳐야 크롤링이 가능한 웹사이트를 편리하게 크롤링 하기 위해서는 많은 스킬과 노하우가 필요합니다.

예를 들어, 스크롤을 올리거나 팝업창을 닫거나, iframe 을 변경하는등 각 기능을 할때마다 많은 검색과 노가다?! 가 필요했습니다.

많은 크롤링 프로그램을 만들면서 이런 귀찮고 시간 소모적인 작업들 없이 간편하게 원하는 크롤링 작업을 하기 위해서 상용 라이브러리를 제작하였습니다.

## 누구를 위한 프로그램인가요?

크롤링을 통해 간단하게 웹사이트를 크롤링 하고 싶지만, 생각보다 해야할 것이 많아서 시작하기 어려우셨던 분.
빠르고 편리하게 웹사이트를 크롤링하고 싶은 분

## 프로젝트 목적

실무 크롤링에서 자주 쓰는 여러 기능들을 쉽게 사용하기 위한 라이브러리 제작

## 프로젝트 활용 범위

상용 크롤링 프로그램 제작.
단순한 페이지 파싱이 아닌 로그인, 스크롤, 팝업 제어 처럼 복잡한 유저 인터랙션이 필요한 웹사이트 크롤링을 간편하게 크롤링

## 예제 프로그램 실행시키기

```sh
python -m lib.advanced_chrome_driver.sample.crawl_hair99
```
