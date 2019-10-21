from django import forms
from .models import Article, Comment
class ArticleForm(forms.ModelForm):
    # 위젯 설정 2.
    title = forms.CharField(
        max_length=1, 
        label='제목',
        help_text='140자 이내로 작성 바랍니다.',
        widget=forms.TextInput(
            attrs={
                'placeholder': '제목을 입력바랍니다.'
            }
        )
    )
    content = forms.CharField(
        # label 내용 수정
        label='내용',
        # Django form에서 HTML 속성 지정 -> widget
        widget=forms.Textarea(
            attrs={
                'class': 'my-content',
                'placeholder': '내용을 입력바랍니다.',
                'row': 5,
                'col': 60
            }
        )
    )
    class Meta:
        model = Article
        # fields = '__all__'
        exclude = ('user',)
        # widgets = {
        #     'title': forms.TextInput(
        #         attrs={
        #             'placeholder': '제목을 입력바랍니다.'
        #         }
        #     )
        # }
        # fields = ('title', )
        # exclude = ('title', )




    # title = forms.CharField(
    #     max_length=1, 
    #     label='제목',
    #     widget=forms.TextInput(
    #         attrs={
    #             'placeholder': '제목을 입력바랍니다.'
    #         }
    #     )
    #     )
    # content = forms.CharField(
    #     # label 내용 수정
    #     label='내용',
    #     # Django form에서 HTML 속성 지정 -> widget
    #     widget=forms.Textarea(
    #         attrs={
    #             'class': 'my-content',
    #             'placeholder': '내용을 입력바랍니다.',
    #             'row': 5,
    #             'col': 60
    #         }
    #     )
    # )
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude=('article',)
        