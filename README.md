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
          
          ```
          polls/
              __init__.py
              admin.py
              apps.py
              migrations/
                  __init__.py
              models.py
              tests.py
              views.py
          ```
   5. 첫 번째 뷰 작성하기
        - `polls/view.py` 열어 다음 코드 입력
          ```
          from django.http import HttpResponse

          def index(request):
          return HttpResponse("Hello, world. You're at the polls index.")
          ```
        - 뷰를 호출하기 위해 연결된 url 필요. 이를 위해 URLconf 사용
        - polls 폴더에 urls.py 만들기
        - `polls/urls.py`에 다음 코드 포함되어 있음
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
          * 발생했던 에러 2
            - `_mysql.c(42) : fatal error C1083: Cannot open include file: 'config-win.h': No such file or directory`
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
        + `...\> py manage.py migrate` #mysite/settings.py의 DB 설정과 app과 함께 제공되는 데이터베이스 migrations에 따라 필요한 DB 테이블 생성
        + 확인하고 싶다면 설정한 schema 들어가서 `show tables;`
        + `mysite/admin.py` 다음과 같이 수정
            ```
              from django.contrib import admin

              from .models import Question, Choice

              admin.site.register(Question)
              admin.site.register(Choice)
            ```
  2. 모델 만들기 
      - 모델 : 부가적인 메타데이터를 가진 데이터베이스의 구조(layout)
      - migration들은 모두 모델 파일로부터 유도됨
      
      - Question, Choice 두 개의 모델 생성
      - Question의 필드 두 개 : question, question date
      - Choice의 필드 두 개 : choice, vote
      - `polls/models.py`를 다음과 같이 수정
          ```
            from django.db import models


            class Question(models.Model):
                question_text = models.CharField(max_length=200)
                pub_date = models.DateTimeField('date published')


            class Choice(models.Model):
                question = models.ForeignKey(Question, on_delete=models.CASCADE)
                choice_text = models.CharField(max_length=200)
                votes = models.IntegerField(default=0)
          ```
      - 각 Field 인스턴스 이름(question_text ...) - 데이터베이스 필드 이름. 데이터베이스에서 컬럼명으로 사용.
      - CharField : 문자 필드 표현 - 필수 인수 : (max_length) / DateTimeField : 날짜, 시간 필드 표현
      - IntegerField : 32비트 정수형 필드 - 선택 인수 : 기본값 설정(default=0)
      - ForeignKey : Choice가 하나의 Question에 관계된다는 것을 Django에게 알려줌. 관계(다대일, 다대다, 일대일)
      
  3. 모델의 활성화 
      - 앱을 현재 프로젝트에 포함시키기 위해, 앱의 구성 클래스에 대한 참조를 INSTALLED_APPS 설정에 추가해야 함.
      - PollsConfig 클래스 polls/apps.py 파일 내에 존재. 점으로 구분된 경로 -> `polls.apps.PollsConfig`
      - `mysite/settings.py`를 다음과 같이 수정
          ```
          INSTALLED_APPS = [
              'polls.apps.PollsConfig',
              'django.contrib.admin',
              'django.contrib.auth',
              'django.contrib.contenttypes',
              'django.contrib.sessions',
              'django.contrib.messages',
              'django.contrib.staticfiles',
          ]
          ```
          
      - `...\> py manage.py makemigrations polls` #모델 변경사항 migration으로 저장하겠다고 Django에게 알림
      - 결과
          ```
          BEGIN;
          --
          -- Create model Choice
          --
          CREATE TABLE "polls_choice" (
              "id" serial NOT NULL PRIMARY KEY,
              "choice_text" varchar(200) NOT NULL,
              "votes" integer NOT NULL
          );
          --
          -- Create model Question
          --
          CREATE TABLE "polls_question" (
              "id" serial NOT NULL PRIMARY KEY,
              "question_text" varchar(200) NOT NULL,
              "pub_date" timestamp with time zone NOT NULL
          );
          --
          -- Add field question to choice
          --
          ALTER TABLE "polls_choice" ADD COLUMN "question_id" integer NOT NULL;
          ALTER TABLE "polls_choice" ALTER COLUMN "question_id" DROP DEFAULT;
          CREATE INDEX "polls_choice_7aa0f6ee" ON "polls_choice" ("question_id");
          ALTER TABLE "polls_choice"
            ADD CONSTRAINT "polls_choice_question_id_246c99a640fbbd72_fk_polls_question_id"
              FOREIGN KEY ("question_id")
              REFERENCES "polls_question" ("id")
              DEFERRABLE INITIALLY DEFERRED;

          COMMIT;
          ```
      - 테이블 이름 : 앱의 이름, 모델의 이름(소문자)이 조합되어 자동 생성(ex. polls&Question -> polls_question), 재지정 가능
      - 기본 키(ID) 자동 추가, 재지정 가능
      - Django는 외래 키 필드명에 `_id` 이름을 자동으로 추가
      - 외래 키 관계는 FOREIGN KEY 제약이 명시적으로 생성됨.
      - sqlmigrate 명령은 실제로 migration 실행하지 않고 단순히 결과만 출력. 
      
      - `...\> py manage.py migrate #migration` #DB에 모델과 관련된 테이블 생성
          ```
          - ...\> py manage.py migrate #migration 실행시켜 DB에 모델과 관련된 테이블 생성
          Operations to perform:
            Apply all migrations: admin, auth, contenttypes, polls, sessions
          Running migrations:
            Rendering model states... DONE
            Applying polls.0001_initial... OK
          ```
      - 결과 
        ```
        Operations to perform:
          Apply all migrations: admin, auth, contenttypes, polls, sessions
        Running migrations:
          Rendering model states... DONE
          Applying polls.0001_initial... OK
        ```
      - migrate 명령 : 적용되지 않은 migration 모두 수집해 이를 실행. 모델에서의 변경 사항, 데이터베이스 스키마의 동기화
      - migration : 동작 중인 DB 자료 손실 없이 업그레이드 하는 데에 최적화
      - 모델의 변경을 만드는 세 단계 : 
        + `models.py`에서 모델 변경
        + `py manage.py makemigrations`를 통해 변경사항에 대한 migration 생성. 
        + `py manage.py migration` 명령을 통해 변경사항 DB에 적용

  4. API 가지고 놀기 
      - 대화식 Python 쉘에 뛰어들어 Django API 자유롭게 가지고 놀기
      
      - `...\> py manage.py shell` #python shell 실행
      - python이라고 실행하는 대신 위의 명령 실행한 이유 : manage.py에 설정된 DJANGO_SETTINGS_MODULE 환경변수 때문.
      - 이 환경변수는 mysite/settings.py 파일에 대한 Python 임포트 경로를 Django에게 제공.
      - Django에서 동작하는 모든 명령을 대화식 Python Shell에서 시험해볼 수 있음.

  5. Django 관리자 소개 
      - Django는 모델 관리용 관리자 인터페이스를 자동으로 생성
      - `...\> py manage.py createsuperuser`
      - username, email, password 입력
      
  6. 개발 서버 시작
      - `...\> py manage.py runserver`
      - localhost:8000/admin/ 또는  http://127.0.0.1:8000/admin/ 으로 접근했을 때 로그인 화면 보임
      - 편집 가능한 그룹, 사용자 ... -> django.contrib.auth 모듈에서 제공

  7. 자유로운 관리 기능 탐색
      - 수정 가능
      - 서식은 모델에서 자동 생성
      - 모델의 각 필드 유형들(DateTimeField, CharField)은 적절한 HTML 입력 위젯으로 표현됨.
            
<hr/>


## part3
  1. 뷰 추가
      - `polls/view.py`에 뷰 추가.
        ```
        def detail(request, question_id):
            return HttpResponse("You're looking at question %s." % question_id)

        def results(request, question_id):
            response = "You're looking at the results of question %s."
            return HttpResponse(response % question_id)

        def vote(request, question_id):
            return HttpResponse("You're voting on question %s." % question_id)
        ```
      - path() 호출 추가해서 새로운 뷰를 polls.urls 모듈로 연결
      - `polls/urls.py` 수정
        ```
        from django.urls import path

        from . import views

        urlpatterns = [
            # ex: /polls/
            path('', views.index, name='index'),
            # ex: /polls/5/
            path('<int:question_id>/', views.detail, name='detail'),
            # ex: /polls/5/results/
            path('<int:question_id>/results/', views.results, name='results'),
            # ex: /polls/5/vote/
            path('<int:question_id>/vote/', views.vote, name='vote'),
        ]
        ```
      - 브라우저에 "/polls/34/" 입력하면 datail() 함수를 호출해서 url에 입력한 id 출력
      - "/polls/34/results/", "/polls/34/vote/" -> 페이지의 뼈대 출력
      - "/polls/34/" 요청하면 Django는 mysite.urls 파이썬 모듈 불러옴. mysite.urls에서 urlpatterns라는 변수 찾고, 순서대로 패턴 따라감. 'polls/' 찾은 후엔, 일치하는 텍스트("polls/")를 버리고, 남은 텍스트인 "34/"를 'polls.urls'의 URLconf로 전달하여 남은 처리 진행. 거기에 '<int:question_id>/'와 일치하여 결과적으로 detail() 뷰 함수가 호출됨.
        ```
        detail(request=<HttpRequest object>, question_id=34)
        ```
      - question_id=34 부분은 <int:question_id>에서 왔음. 괄호를 사용해서 URL의 일부를 "캡처"하고, 해당 내용을 keyword 인수로서 뷰 함수로 전달. <int: ))어느 패턴이 해당 URL 경로에 일치되어야 하는지 결정하는 컨버터, :question_id> )) 일치되는 패턴을 구별하기 위해 정의한 이름 

  2. 뷰가 실제로 뭔가를 하도록 만들기
      - 각 뷰는 두 가지 중 하나를 함 : 1. 요청된 페이지의 내용이 담김 HttpResponse 객체를 반환 2. Http404 같은 예외를 발생
      - Django에 필요한 것은 HttpResponse 객체 혹은 예외.
      - 뷰는 DB의 레코드를 읽을 수 있음. 템플릿 시스템도 사용 가능.
      
      - 뷰에서 사용할 수 있는 템플릿 작성하여 Python 코드로부터 디자인 분리하도록 Django의 템플릿 시스템 사용하기
        + polls 디렉토리에 templates 디렉토리 만들기 : Django가 여기에서 템플릿을 찾게될 것.
        + templates 디렉토리 내에 polls 디렉토리 생성, 그 안에 index.html 생성. 템플릿 : polls/templates/polls/index.html. 템플릿을 단순히 polls/index.html로 참조 가능
          * 템플릿 네임스페이싱 : polls/templates/polls라고 만들 필요 없이 polls/templates에 넣어도 되지 않을까? 좋은 생각 x.  Django는 이름이 일치하는 첫번째 템플릿을 선택. 만약 동일한 템플릿 이름이 다른 어플리케이션에 있을 경우, Django는 이 둘 간의 차이를 구분하지 못함. Django에게 정확한 템플릿을 지정하기 가장 편리한 방법 : 이름공간으로 구분짓기, 어플리케이션의 이름으로 된 디렉토리에 이러한 템플릿들 넣기
        + `polls/templates/polls/index.html`에 다음 코드 입력
          ```
          {% if latest_question_list %}
              <ul>
              {% for question in latest_question_list %}
                  <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
              {% endfor %}
              </ul>
          {% else %}
              <p>No polls are available.</p>
          {% endif %}
          ```
        + `polls/views.py`에 index 뷰 업데이트
          ```
          from django.http import HttpResponse
          from django.template import loader

          from .models import Question


          def index(request):
              latest_question_list = Question.objects.order_by('-pub_date')[:5]
              template = loader.get_template('polls/index.html')
              context = {
                  'latest_question_list': latest_question_list,
              }
              return HttpResponse(template.render(context, request))
          ```
          * polls/index.html 템플릿 불러온 후 context 전달. context는 템플릿에서 쓰이는 변수명과 Python 객체를 연결하는 사전형 값
          ```
        + 브라우저에서 "/polls/" 페이지 불러오면 질문이 포함된 리스트가 표시됨.
        
  3. 지름길 : render()
      - 템플릿에 context 채워 넣어 표현한 결과를 HttpResponse 객체와 함께 돌려주는 구문은 자주 쓰는 용법.
      - Django 이를 위해 단축 기능 제공
      - `polls/views.py` index() 뷰 단축 기능으로 작성
        ```
        from django.shortcuts import render

        from .models import Question


        def index(request):
            latest_question_list = Question.objects.order_by('-pub_date')[:5]
            context = {'latest_question_list': latest_question_list}
            return render(request, 'polls/index.html', context)
        ```
      - 더 이상 loader와 HttpResponse를 임포트하지 않아도 됨. (단 detail, results, vote에서 stub 메소드를 가지고 있다면 유지해야 함.)
      - render() 함수 _ 첫 번째 인수 : request / 두 번째 인수 : 템플릿 이름 / 세 번째 선택적 인수 : context 사전형 객체. 인수로 지정된 context로 표현된 템플릿의 HttpResponse 객체가 반환됨.
      
  4. 404 에러 일으키기
      - 질문 상세 뷰(지정된 설문조사의 질문 내용 보여줌)에 태클 걸기
      - `polls/views.py`
        ```
        from django.http import Http404
        from django.shortcuts import render

        from .models import Question
        # ...
        def detail(request, question_id):
            try:
                question = Question.objects.get(pk=question_id)
            except Question.DoesNotExist:
                raise Http404("Question does not exist")
            return render(request, 'polls/detail.html', {'question': question})
        ```
      - 뷰는 요청된 질문의 ID가 없을 경우 Http404 예외를 발생시킴.
      
      
  5. 지름길 : get_object_or_404()
      - 객체가 존재하지 않을 때 get() 사용해 Http404 예외 발생시키는 것은 자주 쓰이는 용법.
      - Django 이를 위해 단축 기능 제공
      - `polls/views.py` detail() 뷰 단축 기능으로 작성
        ```
        from django.shortcuts import get_object_or_404, render

        from .models import Question
        # ...
        def detail(request, question_id):
            question = get_object_or_404(Question, pk=question_id)
            return render(request, 'polls/detail.html', {'question': question})
        ```
      - get_object_or_404() : Django 모델 첫 번째 인자로 받고, 몇 개의 키워드 인수를 모델 관리자의 get() 함수에 넘김. 만약 객체가 존재하지 않을 경우, Http404 예외가 발생. 
      
  6. 템플릿 시스템 사용하기
      - detail() 뷰. context 변수 question이 주어졌을 때, polls/detail.html이라는 템플릿이 어떻게 보이는지
      - `polls/templates/polls/detail.html`
        ```
        <h1>{{ question.question_text }}</h1>
        <ul>
        {% for choice in question.choice_set.all %}
            <li>{{ choice.choice_text }}</li>
        {% endfor %}
        </ul>
        ```
      - 템플릿 시스템은 변수의 속성에 접근하기 위해 점-탐색(dot-lookup) 문법 사용.
      - {{ question.question_text }} : Django는 먼저 question 객체에 대해 사전형으로 탐색. 실패하면 속성값으로 탐색. 실패하면 인덱스 탐색.
      - {% for %} 반복 구문에서 메소드 호출 일어남.
      - question.choice_set.all은 Python에서 question.choice_set.all() 코드로 해석됨. 이때 반환된 Choice 객체의 반복자는 {% for %}에서 사용하기 적당.
      
  7. 템플릿에서 하드코딩된 URL 제거
      - `polls/index.html` 템플릿에 링크를 적으면, 다음과 같이 부분적으로 하드코딩됨.
        ```
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
        ```
      - 이렇게 강력하게 결합되고 하드코딩된 접근 방식의 문제는 수 많은 템플릿을 가진 프로젝트들의 URL을 바꾸기 어렵다는 것.
      - 그러나 polls.urls 모듈의 path() 함수에서 인수의 이름을 정의했으므로, {% url %} template 태그를 사용하여 url 설정에 정의된 특정한 URL 경로들의 의존성 제거 가능.
        ```
        <li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
        ```
      - detail이라는 이름의 url이 어떻게 정의되어있는지 확인 가능
      
  6. 템플릿 시스템 사용하기
      - detail() 뷰. context 변수 question이 주어졌을 때, polls/detail.html이라는 템플릿이 어떻게 보이는지
      - `polls/templates/polls/detail.html`
        ```
        <h1>{{ question.question_text }}</h1>
        <ul>
        {% for choice in question.choice_set.all %}
            <li>{{ choice.choice_text }}</li>
        {% endfor %}
        </ul>
        ```
      - 템플릿 시스템은 변수의 속성에 접근하기 위해 점-탐색(dot-lookup) 문법 사용.
      - {{ question.question_text }} : Django는 먼저 question 객체에 대해 사전형으로 탐색. 실패하면 속성값으로 탐색. 실패하면 인덱스 탐색.
      - {% for %} 반복 구문에서 메소드 호출 일어남.
      - question.choice_set.all은 Python에서 question.choice_set.all() 코드로 해석됨. 이때 반환된 Choice 객체의 반복자는 {% for %}에서 사용하기 적당.
      
  8. URL의 이름공간 정하기
      - Django가 {% url %} 템플릿태그를 사용할 때, 어떤 앱의 뷰에서 URL을 생성할지 아는 방법 : URLconf에 이름 공간(namespace) 추가
      - polls/urls.py 파일에 app_name을 추가하여 어플리케이션의 이름 공간을 설정
      - `polls/urls.py¶`
        ```
        from django.urls import path

        from . import views

        app_name = 'polls'
        urlpatterns = [
            path('', views.index, name='index'),
            path('<int:question_id>/', views.detail, name='detail'),
            path('<int:question_id>/results/', views.results, name='results'),
            path('<int:question_id>/vote/', views.vote, name='vote'),
        ]
        ```
      - `polls/index.html` 템플릿의 기존 내용을 이름공간으로 나눠진 상세 뷰를 가리키도록 변경.
        ```
        <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
        ```
            
<hr/>


## part4
  1. 간단한 폼 만들기
      - `polls/templates/polls/detail.html` 투표 상세 템플릿을 수정하여, 템플릿에 HTML <form> 요소를 포함시키기
  
        ```
        <h1>{{ question.question_text }}</h1>

        {% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}

        <form action="{% url 'polls:vote' question.id %}" method="post">
        {% csrf_token %}
        {% for choice in question.choice_set.all %}
            <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
            <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
        {% endfor %}
        <input type="submit" value="Vote">
        </form>
        ```
      - 위의 템플릿은 각 질문 선택 항목에 대한 라디오 버튼 표시. value는 연관된 질문 선택 항목의 ID
      - method="post" (method="get" 와 반대로) 를 사용하는 것은 매우 중요
      - forloop.counter 는 for 태그가 반복을 한 횟수
      - 내부 URL들을 향하는 모든 POST 폼에 템플릿 태그 {% csrf_token %}를 사용하면 됨.

      - 제출된 데이터를 처리하고 그 데이터로 무언가를 수행하는 Django 뷰
      - `polls/urls.py`에 다음 추가.
        ```
          path('<int:question_id>/vote/', views.vote, name='vote'),
        ```

      - vote() 함수 구현
      - `polls/views.py`에 다음 추가.
        ```
        from django.http import HttpResponse, HttpResponseRedirect
        from django.shortcuts import get_object_or_404, render
        from django.urls import reverse

        from .models import Choice, Question
        # ...
        def vote(request, question_id):
            question = get_object_or_404(Question, pk=question_id)
            try:
                selected_choice = question.choice_set.get(pk=request.POST['choice'])
            except (KeyError, Choice.DoesNotExist):
                # Redisplay the question voting form.
                return render(request, 'polls/detail.html', {
                    'question': question,
                    'error_message': "You didn't select a choice.",
                })
            else:
                selected_choice.votes += 1
                selected_choice.save()
                # Always return an HttpResponseRedirect after successfully dealing
                # with POST data. This prevents data from being posted twice if a
                # user hits the Back button.
                return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        ```
      - request.POST는 키로 전송된 자료에 접근할 수 있도록 해주는 사전과 같은 객체. request.POST['choice'] 는 선택된 설문의 ID를 문자열로 반환. request.POST 의 값은 항상 문자열. Django는 같은 방법으로 GET 자료에 접근하기 위해 request.GET 를 제공
      - 만약 POST 자료에 choice 가 없으면, request.POST['choice'] 는 KeyError. choice가 주어지지 않은 경우에는 에러 메시지와 함께 설문조사 폼을 다시 보여줌.
      - 설문지의 수가 증가한 이후에, 코드는 일반 HttpResponse 가 아닌 HttpResponseRedirect 를 반환하고, HttpResponseRedirect 는 하나의 인수를 받음. 그 인수는 사용자가 재전송될 URL
      - POST 데이터를 성공적으로 처리 한 후에는 항상 HttpResponseRedirect 를 반환해야 함.
      - HttpResponseRedirect 생성자 안에서 reverse() 함수를 사용. 이 함수는 뷰 함수에서 URL을 하드코딩하지 않도록 도와줌. 제어를 전달하기 원하는 뷰의 이름을, URL패턴의 변수부분을 조합해서 해당 뷰를 가리킴. reverse() 호출은 다음 문자열 반환 `/polls/3/results/` redirect된 URL은 최종 페이지 표시 위해 result 뷰 호출.
      
      - 설문조사 하고 난 뒤, vote() 뷰는 설문조사 페이지로 redirect함.
      - `polls/views.py` 그 뷰 작성
        ```
        from django.shortcuts import get_object_or_404, render


        def results(request, question_id):
            question = get_object_or_404(Question, pk=question_id)
            return render(request, 'polls/results.html', {'question': question})
        ```
      - `polls/templates/polls/results.html` 그 뷰 작성, /polls/1/로 가면 투표 가능.
        ```
        <h1>{{ question.question_text }}</h1>

        <ul>
        {% for choice in question.choice_set.all %}
            <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
        {% endfor %}
        </ul>

        <a href="{% url 'polls:detail' question.id %}">Vote again?</a>
        ```
      
  2. 제너릭 뷰 사용하기 : 적은 코드가 더 좋습니다.
      - 뷰는 URL에서 전달된 매개변수에 따라 DB에서 데이터를 가져오는 것과 템플릿을 로드하고 렌더링된 템플릿을 리턴하는 기본 웹 개발의 일반적인 경우를 나타냄. -> Django는 이를 위해 '제너릭 뷰' 시스템이라는 지름길을 제공
      
      - 설문조사 어플리케이션을 제너릭 뷰 시스템을 사용하도록 변환하는 단계
        + URLconf 변환
        + 불필요한 오래된보기 중 일부 삭제
        + Django의 제너릭 뷰를 기반으로 새로운 뷰 도입
        
  3. URLconf 수정
      - `polls/urls.py` URLconf를 다음과 같이 변경
        ```
        from django.urls import path

        from . import views

        app_name = 'polls'
        urlpatterns = [
            path('', views.IndexView.as_view(), name='index'),
            path('<int:pk>/', views.DetailView.as_view(), name='detail'),
            path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
            path('<int:question_id>/vote/', views.vote, name='vote'),
        ]
        ```

  4. views 수정
      - 이전의 index, detail, results 뷰 제거, 장고의 일반적인 뷰 사용
      - `polls/views.py`
        ```
        from django.http import HttpResponseRedirect
        from django.shortcuts import get_object_or_404, render
        from django.urls import reverse
        from django.views import generic

        from .models import Choice, Question


        class IndexView(generic.ListView):
            template_name = 'polls/index.html'
            context_object_name = 'latest_question_list'

            def get_queryset(self):
                """Return the last five published questions."""
                return Question.objects.order_by('-pub_date')[:5]


        class DetailView(generic.DetailView):
            model = Question
            template_name = 'polls/detail.html'


        class ResultsView(generic.DetailView):
            model = Question
            template_name = 'polls/results.html'


        def vote(request, question_id):
            ... # same as above, no changes needed.
        ```
      - 두 제너릭 뷰 : ListView, DetailView

        ```
