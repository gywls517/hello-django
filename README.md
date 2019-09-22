# Hello Django tutorials part 1-4

## part1
  1. Django 설치
      - Django 설치
      - `...\> py -m django --version`  #버전 확인
      
  2. 프로젝트 만들기
      - cmd에서 코드를 저장할 디렉토리로 이동
      - `...\> django-admin startproject mysite`
      - startproject에서 생성되는 것들
      
            mysite/
                manage.py
                mysite/
                    __init__.py
                    settings.py
                    urls.py
                    wsgi.py

        + `mysite/` 디렉토리 바깥의 디렉토리는 단순히 프로젝트를 담는 공간. 이 이름은 Django 와 아무 상관 없으므로 원하는 이름으로 변경 가능.
        + `manage.py`: Django 프로젝트와 다양한 방법으로 상호작용하는 커맨드라인의 유틸리티. 
        + `mysite/` 디렉토리 내부에는 프로젝트를 위한 실제 Python 패키지들이 저장됨. 이 디렉토리 내의 이름을 이용하여, (mysite.urls 와 같은 식으로) 프로젝트의 어디서나 Python 패키지들 import 가능.
        + `mysite/__init__.py`: Python으로 하여금 이 디렉토리를 패키지처럼 다루라고 알려주는 용도의 단순한 빈 파일.
        + `mysite/settings.py`: 현재 Django 프로젝트의 환경 및 구성을 저장.
        + `mysite/urls.py`: 현재 Django project의 URL 선언을 저장. Django 로 작성된 사이트의 목차. 
        + `mysite/wsgi.py`: 현재 프로젝트를 서비스하기 위한 WSGI 호환 웹 서버의 진입점.

   3. 개발 서버
        - mysite 디렉토리로 이동
        - `...\> py manage.py runserver`  #Django 개발 서버 시작
        - http://127.0.0.1:8000/ or localhost:8000/으로 접속 가능 #내부 IP의 8000번 포트로 서버 띄움
        
        - `...\> py manage.py runserver 8080` #8080으로 포트 변경
        
        - runserver의 자동 변경 기능 : 개발 서버는 요청 들어올 때마다 다시 코드 불러옴. 그러나 파일 추가 등 몇 동작은 서버 재기동 해야 적용.
        
   4. 설문조사 앱 만들기
        - mysite 디렉토리로 이동
        - `...\> py manage.py startapp polls` #polls 디렉토리 생성
        - polls에서 생성되는 것들
      
            mysite/
                manage.py
                mysite/
                    __init__.py
                    settings.py
                    urls.py
                    wsgi.py
        
   4. 첫 번째 뷰 작성하기
        - `polls/view.py` 열어 다음 코드 입력
        
          polls/view.py
          ```
          from django.http import HttpResponse

          def index(request):
          return HttpResponse("Hello, world. You're at the polls index.")
          ```
        - 뷰를 호출하기 위해 연결된 url 필요. 이를 위해 URLconf 사용
        - polls 폴더에 urls.py 만들기
        - `polls/urls.py`에 다음 코드 포함되어 있음
                
          polls/urls.py
          ```
          from django.urls import path

          from . import views

          urlpatterns = [
              path('', views.index, name='index'),
          ]
          ```
        - `mysite/urls.py` 열어 다음 코드 입력
          ```
            from django.contrib import admin
            from django.urls import include, path

            urlpatterns = [
                path('polls/', include('polls.urls')),
                path('admin/', admin.site.urls),
            ]
          ```
          + include() : 다른 URLconf 참조하도록 도움. Django가 이 함수 만나면 URL의 그 시점까지 일치하는 부분을 자르고, 남은 문자열 부분을 후속 처리하기 위해 include된 URLconf로 전달
          + polls 앱에 그 자체의 URLconf(polls/urls.py)가 존재하는 한, "/polls/", 또는 "/fun_polls/", "/content/polls/"와 같은 경로, 또는 그 어떤 다른 root 경로에 연결해도 앱은 잘 동작할 것
          + 다른 URL 패턴 포함할 때마다 include() 사용해야 함. admin.site.urls가 유일한 예외
        - `...\> py manage.py runserver`
        - http://localhost:8000/polls/ 에서 index 뷰에 정의한 것들이 보임
        
        - path() : 필수 인수 == route, view / 선택 인수 == kwargs, name
          + path() 인수 : route
            * route는 URL 패턴을 가진 문자열.
            * Django는 urlpatterns의 첫 번째 패턴부터 시자가여, 일치하는 패턴을 찾을 때까지 요청된 url을 각 패턴과 리스트 순서대로 비교.
            * 패턴들은 GET,POST의 매개변수들 혹은 도메인 이름 검색 x.
            * https://www.example.com/myapp/ 이 요청된 경우, URLconf 는 오직 myapp/ 부분만 봄. https://www.example.com/myapp/?page=3, 같은 요청에도, URLconf 는 myapp/ 부분만 신경씀
          + path() 인수 : view
            * Django 에서 일치하는 패턴을 찾으면, HttpRequest 객체를 첫번째 인수로 하고, 경로로 부터 '캡처된' 값을 키워드 인수로하여 특정한 view 함수를 호출
          + path() 인수 : kwargs
            * 임의의 키워드 인수들은 목표한 view에 사전형으로 전달
          + path() 인수 : name
            * URL에 이름을 지으면, 템플릿을 포함한 Django 어디에서나 명확하게 참조 가능
            * 이 기능 이용해 하나의 파일만 수정해도 프로젝트 내의 모든 URL 패턴을 바꿀 수 있도록 도와줌.
            
<hr/>


## part2
  1. 데이터베이스 설치
      - `mysite/settings.py` Django 설정을 모듈 변수로 표현한 보통의 Python 모듈
      - 기본적으로 SQLite를 사용하도록 구성
      - MySQL 사용하고 싶을 때
        + 데이터베이스 바인딩(mysqlclient) 설치 - windows
          * 발생했던 에러 1
            - `error: Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C++ Build Tools": http://landinghub.visualstudio.com/visual-cpp-build-tools`
            - 해결 방법 : Visual C++ Build tools 2015 download
            - 참고 링크 : https://nologout.blog.me/221440309296
          * 발생했던 에러 1
            - `_mysql.c(42) : fatal error C1083: Cannot open include file: 'config-win.h': No such file or directory`<>
            - 해결 방법 : `pip install wheel` `pip install mysqlclient-1.4.4-cp37-cp37m-win32.whl` #깔려있는 Python이 3.7에 32bit라서 cp37, win32로 다운로드
            - 참고 링크 : https://stackoverflow.com/questions/26866147/mysql-python-install-error-cannot-open-include-file-config-win-h
        + 데이터베이스 연결 설정과 맞게 DATABASES 'default' 값 변경
          * `settings.py`에서 다음과 같이 설정
              ```
                DATABASES = {
                  'default': {
                  'ENGINE': 'django.db.backends.mysql',
                    'NAME': schema 이름, #mysql에 schema 생성 후 쓰기
                    'HOST': 'localhost',
                    'PORT': '3306',
                    'USER': 사용자 이름,
                    'PASSWORD': 비밀번호
                  }
                }
                
                TIME_ZONE = 'Asia/Seoul'
              ```
        + `...\> py manage.py migrate` #DB 설정과 app과 함께 제공되는 데이터베이스 migration에 따라 필요한 DB 테이블 생성
        + 확인하고 싶다면 설정한 schema 들어가서 `show tables;`
        + `mysite/admin.py` 다음과 같이 수정
          '''
            from django.contrib import admin

            from .models import Question, Choice

            admin.site.register(Question)
            admin.site.register(Choice)
          '''
