from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from django_tables2 import RequestConfig
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.models import User, Child, Test, MedicalInstitution
from main.forms import UserCreationForm
from .generators import generate_user_code, generate_test_code, generate_child_code
from .filters import TestFilter, ChildFilter
from .tables import ResultTestTable, ResultChildTable





User = get_user_model()


def get_home_page(request):
    return render(request, 'home.html')




@login_required(login_url='/login')
def get_child_vew_page(request, child_code):

    user_id = request.user.id
    user = User.objects.get(id=user_id)

    medical_institutions = MedicalInstitution.objects.all()
    medical_institution_choices = [(inst.id, inst.Nokpo) for inst in medical_institutions]

    # Находим ребенка с переданным child_code
    child = Child.objects.filter(child_code=child_code).first()

    if child:
        child_code = child.child_code
        child_birthday_date = child.child_birthday_date
        child_gender = child.child_gender
        child_medical_institution_id = child.medical_institution.Nokpo

    else:
        child_birthday_date = None


    context = {
        'child_code': child_code,
        'child_birthday_date': child_birthday_date,
        'child_gender': child_gender,
        'medical_institution_choices':medical_institution_choices,
        'child_medical_institution_id' : child_medical_institution_id,
    }

    return render(request, 'profile/index_child_view.html', context)



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, f"Неверное имя пользователя или пароль!")
            return redirect('profile')
    return render(request, 'registration/login.html')



@login_required(login_url='/login')
def get_profile_page(request):

    if request.user.is_superuser:
        table_childs_filter = ChildFilter(request.GET, queryset=Child.objects.all().order_by('-created_at'))


    elif request.user.is_role == 3:
        table_childs_filter = ChildFilter(request.GET,queryset=Child.objects.filter(medical_institution=request.user.medical_institution).order_by('-created_at'))



    else:
        table_childs_filter = ChildFilter(request.GET, queryset=Child.objects.filter(user=request.user).order_by('-created_at'))



    total_count = table_childs_filter.qs.count()

    print("Total count:", total_count)

    context = {

        'total_count': total_count,
    }

    return render(request, 'profile/index.html', context)






@login_required(login_url='/login')
def get_profile_settings_page(request):
    return render(request, 'profile/index_settings.html')



@login_required(login_url='/login')
def get_tests_page(request):
    user = request.user


    if request.user.is_superuser:

        table_tests_filter = TestFilter(request.GET, queryset=Test.objects.all().order_by('-test_date'))
        result_test_table = ResultTestTable(table_tests_filter.qs)

    elif request.user.is_role == 3:
        table_tests_filter = TestFilter(request.GET, queryset=Test.objects.filter(user=user, medical_institution=request.user.medical_institution).order_by('-test_date'))
        result_test_table = ResultTestTable(table_tests_filter.qs)
    else:

        table_tests_filter = TestFilter(request.GET, queryset=Test.objects.filter(user=user).order_by('-test_date'))
        result_test_table = ResultTestTable(table_tests_filter.qs)



    RequestConfig(request).configure(result_test_table)


    context = {
        'filter': table_tests_filter,
        'result_test_table': result_test_table,
    }


    return render(request, 'profile/index_tests.html', context)








@login_required(login_url='/login')
def get_childs_page(request):

    medical_institutions = MedicalInstitution.objects.all()
    medical_institution_choices = [(inst.id, inst.Nokpo) for inst in medical_institutions]



    if request.user.is_superuser:

        # table_childs_filter = ChildFilter(request.GET, queryset=Child.objects.all().order_by('-created_at'))
        table_childs_filter = ChildFilter(request.GET,queryset=Child.objects.filter(user=request.user).order_by('-created_at'))
        result_child_table = ResultChildTable(table_childs_filter.qs)


    elif request.user.is_role == 3:
        table_childs_filter = ChildFilter(request.GET,queryset=Child.objects.filter(medical_institution=request.user.medical_institution).order_by('-created_at'))
        result_child_table = ResultChildTable(table_childs_filter.qs)



    else:
        table_childs_filter = ChildFilter(request.GET, queryset=Child.objects.filter(user=request.user).order_by('-created_at'))
        result_child_table = ResultChildTable(table_childs_filter.qs)


    RequestConfig(request).configure(result_child_table)

    child_code = generate_child_code(request)



    context = {
        'filter': table_childs_filter,
        'result_child_table': result_child_table,
        'child_code': child_code,
        'medical_institution_choices': medical_institution_choices,

    }


    return render(request, 'profile/index_childs.html', context)





def save_child(request, user_id):
    if request.method == 'POST':
        child_code = request.POST.get('child_code')
        child_birthday_date = request.POST.get('child_birthday_date')
        child_gender = request.POST.get('child_gender')
        medical_institution_id = request.POST.get('medical_institution')

        try:
            user = User.objects.get(id=user_id)
            medical_institution = MedicalInstitution.objects.get(id=medical_institution_id)
        except (User.DoesNotExist, MedicalInstitution.DoesNotExist):
            return HttpResponse("Пользователь или медицинское учреждение не найдены")

        child = Child(
            child_code=child_code,
            user=user,
            child_birthday_date=child_birthday_date,
            child_gender=child_gender,
            medical_institution=medical_institution
        )
        child.save()
        messages.success(request, f'Ребенок успешно зарегистрирован!<br> Код ребенка: <strong>{child_code}</strong>')
        return redirect('childs')  # Вернуть перенаправление на ту же страницу
    else:
        # Если это не POST-запрос, верните рендер шаблона
        return render(request, 'profile/index_childs.html')










@login_required(login_url='/login')
def get_test1_page(request, child_code):
    user_id = request.user.id
    user = User.objects.get(id=user_id)

    # Находим ребенка с переданным child_code
    child = Child.objects.filter(child_code=child_code).first()

    if child:
        child_birthday_date = child.child_birthday_date
    else:
        child_birthday_date = None

    children = Child.objects.filter(user=user)

    test_code = generate_test_code(request.user)

    context = {
        'current_page': 'profile_page',
        'children': children,
        'test_code': test_code,
        'child_code': child_code,
        'child_birthday_date': child_birthday_date,
    }

    return render(request, 'tests/test1.html', context)





@login_required(login_url='/login')
def get_test2_page(request, child_code):

    user_id = request.user.id
    user = User.objects.get(id=user_id)

    child = Child.objects.filter(child_code=child_code).first()

    if child:
        child_birthday_date = child.child_birthday_date
    else:
        child_birthday_date = None

    children = Child.objects.filter(user=user)

    test_code = generate_test_code(request.user)

    context = {
        'current_page': 'profile_page',
        'children': children,
        'test_code':test_code,
        'child_code': child_code,
        'child_birthday_date': child_birthday_date,

    }

    return render(request, 'tests/test2.html',context)



@login_required(login_url='/login')
def get_test3_page(request, child_code):

    user_id = request.user.id
    user = User.objects.get(id=user_id)

    if user.is_role not in [1, 2]:
        messages.info(request, "Для прохождения «Тест-3» авторизируйтесь как медицинский работник!")
        return redirect('childs')

    child = Child.objects.filter(child_code=child_code).first()

    if child:
        child_birthday_date = child.child_birthday_date
    else:
        child_birthday_date = None

    children = Child.objects.filter(user=user)

    test_code = generate_test_code(request.user)

    context = {
        'current_page': 'profile_page',
        'children': children,
        'test_code': test_code,
        'child_code': child_code,
        'child_birthday_date': child_birthday_date,
    }

    return render(request, 'tests/test3.html', context)












@login_required(login_url='/login')
def test_1_creation(request):
    if request.method == 'POST':
        child_code = request.POST.get('child_code')
        test_identifier = request.POST.get('test_identifier')
        test_code = request.POST.get('test_code')
        child_birthday = request.POST.get('child_birthday')

        try:
            child = Child.objects.filter(child_code=child_code).first()
            if not child:
                return render(request, 'error.html', {'error': 'Ребенок с указанным кодом не найден или не принадлежит вам'})

            test_question_values = {
            "question1_test1": request.POST.get('question1_test1'),
            "question2_test1": request.POST.get('question2_test1'),
            "question3_test1": request.POST.get('question3_test1'),
            "question4_test1": request.POST.get('question4_test1'),
            "question5_test1": request.POST.get('question5_test1'),
            "question6_test1": request.POST.get('question6_test1'),
            "question7_test1": request.POST.get('question7_test1'),
            "question8_test1": request.POST.get('question8_test1'),
            "question9_test1": request.POST.get('question9_test1'),
            "question10_test1": request.POST.get('question10_test1'),
            "question11_test1": request.POST.get('question11_test1'),
            "question12_test1": request.POST.get('question12_test1'),
            "question13_test1": request.POST.get('question13_test1'),
            "question14_test1": request.POST.get('question14_test1'),
            "question15_test1": request.POST.get('question15_test1'),
            "question16_test1": request.POST.get('question16_test1'),
            "question17_test1": request.POST.get('question17_test1'),
            "question18_test1": request.POST.get('question18_test1'),
            "question19_test1": request.POST.get('question19_test1'),
            "question20_test1": request.POST.get('question20_test1'),
            "question21_test1": request.POST.get('question21_test1'),
            "question22_test1": request.POST.get('question22_test1'),
            "question23_test1": request.POST.get('question23_test1'),
            }

            exceptions_values = ["question11_test1", "question18_test1", "question20_test1", "question22_test1"]
            has_invalid_zeros = any(value == "0" and key not in exceptions_values for key, value in test_question_values.items())

            if has_invalid_zeros:
                result_text = "Выявлены признаки"
            else:
                result_text = "Не выявлены признаки"

            test = Test(
                child=child,
                user=request.user,
                test_identifier=test_identifier,
                test_code=test_code,
                child_birthday=child_birthday,
                result_test=result_text,
                medical_institution=request.user.medical_institution,

            )
            test.save()

            messages.success(request, f'{test_code}')

            return redirect('tests')
        except Exception as e:
            return render(request, 'error.html', {'error': f'Ошибка создания теста: {str(e)}'})

    return render(request, 'test1.html')





@login_required(login_url='/login')
def test_2_creation(request):
    if request.method == 'POST':
        # Получить данные из запроса
        child_code = request.POST.get('child_code')
        test_identifier = request.POST.get('test_identifier')
        test_code = request.POST.get('test_code')
        child_birthday = request.POST.get('child_birthday')

        # Получить ребенка по коду
        try:
            child = Child.objects.get(child_code=child_code)
        except Child.DoesNotExist:
            # Ребенок с указанным кодом не найден
            return render(request, 'error.html', {'error': 'Ребенок с указанным кодом не найден'})

        # Получить результат теста
        test_question_values = {
            "question_1_1_test_2": request.POST.get('question_1_1_test_2'),
            "question_1_2_test_2": request.POST.get('question_1_2_test_2'),
            "question_1_3_test_2": request.POST.get('question_1_3_test_2'),
            "question_1_4_test_2": request.POST.get('question_1_4_test_2'),
            "question_1_5_test_2": request.POST.get('question_1_5_test_2'),
            "question_1_6_test_2": request.POST.get('question_1_6_test_2'),
            "question_1_7_test_2": request.POST.get('question_1_7_test_2'),
            "question_2_1_test_2": request.POST.get('question_2_1_test_2'),
            "question_2_2_test_2": request.POST.get('question_2_2_test_2'),
            "question_2_3_test_2": request.POST.get('question_2_3_test_2'),
            "question_3_1_test_2": request.POST.get('question_3_1_test_2'),
            "question_3_2_test_2": request.POST.get('question_3_2_test_2'),
            "question_4_1_test_2": request.POST.get('question_4_1_test_2'),
            "question_4_2_test_2": request.POST.get('question_4_2_test_2'),
            "question_4_3_test_2": request.POST.get('question_4_3_test_2'),
            "question_5_1_test_2": request.POST.get('question_5_1_test_2'),
            "question_5_2_test_2": request.POST.get('question_5_2_test_2'),
            "question_5_3_test_2": request.POST.get('question_5_3_test_2'),
            "question_6_1_test_2": request.POST.get('question_6_1_test_2'),
            "question_6_2_test_2": request.POST.get('question_6_2_test_2'),
            "question_6_3_test_2": request.POST.get('question_6_3_test_2'),
            "question_6_4_test_2": request.POST.get('question_6_4_test_2'),
            "question_6_5_test_2": request.POST.get('question_6_5_test_2'),
            "question_6_6_test_2": request.POST.get('question_6_6_test_2'),
        }

        total_score = 0

        for key, value in test_question_values.items():
            if value == "1":
                total_score += 1
            elif value == "2":
                total_score += 2
            elif value == "3":
                total_score += 3
            elif value == "4":
                total_score += 4

        if total_score >= 24 and total_score <= 36:
            result_test = "Высокий риск РАС"
        elif total_score >= 37 and total_score <= 63:
            result_test = "Средний риск РАС"
        elif total_score >= 64 and total_score <= 96:
            result_test = "Низкий риск РАС"
        else:
            result_test = "Данные не распознаны"

        # Сохранить тест
        test = Test(
            user=request.user,
            child=child,
            test_identifier=test_identifier,
            test_code=test_code,
            child_birthday=child_birthday,
            result_test=result_test,
            medical_institution=request.user.medical_institution,
        )
        test.save()

        if test:
            messages.success(request, f'{test_code}')
            return redirect('tests')
        else:
            # При сохранении теста возникла ошибка
            return render(request, 'error.html', {'error': 'Ошибка при сохранении теста'})

    else:
        # Отобразить форму создания теста
        return render(request,'test1.html')



@login_required(login_url='/login')
def test_3_creation(request):
    if request.method == 'POST':
        # Получить данные из запроса
        child_code = request.POST.get('child_code')
        test_identifier = request.POST.get('test_identifier')
        test_code = request.POST.get('test_code')
        child_birthday = request.POST.get('child_birthday')

        # Получить ребенка по коду
        try:
            child = Child.objects.get(child_code=child_code)
        except Child.DoesNotExist:
            # Ребенок с указанным кодом не найден
            return render(request, 'error.html', {'error': 'Ребенок с указанным кодом не найден'})

        # Получить результат теста
        test_question_values = {
            "check_1_3": request.POST.get('check_1_3'),
            "check_2_3": request.POST.get('check_2_3'),
            "check_3_3": request.POST.get('check_3_3'),
            "check_4_3": request.POST.get('check_4_3'),
            "check_5_3": request.POST.get('check_5_3'),
            "check_6_3": request.POST.get('check_6_3'),
            "check_7_3": request.POST.get('check_7_3'),
            "check_8_3": request.POST.get('check_8_3'),
            "check_9_3": request.POST.get('check_9_3'),
            "check_10_3": request.POST.get('check_10_3'),
            "check_11_3": request.POST.get('check_11_3'),
            "check_12_3": request.POST.get('check_12_3'),
        }

        total_score = 0

        for key, value in test_question_values.items():
            if value == "0":
                total_score += 0
            elif value == "1":
                total_score += 1
            elif value == "2":
                total_score += 2
            elif value == "3":
                total_score += 3
            elif value == "4":
                total_score += 4

        if total_score >= 37 and total_score <= 65:
            result_test = "Высокий риск РАС"
        elif total_score >= 27 and total_score <= 36:
            result_test = "Средний риск РАС"
        elif total_score >= 13 and total_score <= 26:
            result_test = "Низкий риск РАС"
        else:
            result_test = "Данные не распознаны"

        # Сохранить тест
        test = Test(
            user=request.user,
            child=child,
            test_identifier=test_identifier,
            test_code=test_code,
            child_birthday=child_birthday,
            result_test=result_test,
            medical_institution=request.user.medical_institution,
        )
        test.save()

        if test:
            messages.success(request, f'{test_code}')
            return redirect('tests')
        else:
            # При сохранении теста возникла ошибка
            return render(request, 'error.html', {'error': 'Ошибка при сохранении теста'})

    else:
        # Отобразить форму создания теста
        return render(request,'test1.html')
















class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        random_number = generate_user_code(request)
        context = {
            'form': UserCreationForm(),
            'user_code': random_number,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if User.objects.filter(username=request.POST.get('username')).exists():
            messages.error(request, f"Логин уже существует!")
            return redirect('register')


        if form.is_valid():
            # Проверяем, существует ли уже такое имя пользователя
            existing_username = User.objects.filter(username=request.POST.get('username')).exists()
            if existing_username:
                # Если имя пользователя существует, выводим сообщение об ошибке
                messages.error(request, f"Ошибка: код пользователя")
                return redirect('register')


            existing_email = User.objects.filter(email=request.POST.get('email')).exists()
            if existing_email:
                # Если имя пользователя существует, выводим сообщение об ошибке
                messages.error(request, f"Адрес электронной почты уже существует!")
                return redirect('register')

            # Проверяем, существует ли уже такой user_code
            existing_code = User.objects.filter(user_code=request.POST.get('user_code')).exists()
            if existing_code:
                # Если код существует, выводим сообщение об ошибке
                messages.error(request, f"Ошибка: код пользователя")
                return redirect('register')

            # Если имя пользователя и код уникальны, сохраняем пользователя
            user = form.save()
            user.user_code = request.POST.get('user_code')
            user.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile')

        else:
            # Если форма не прошла валидацию, выводим ошибки в шаблон
            messages.error(request, "Создайте более надёжный пароль!")
            return redirect('register')

        random_number = generate_user_code(request)
        context = {
            'form': form,
            'user_code': random_number,
        }
        return render(request, self.template_name, context)












































