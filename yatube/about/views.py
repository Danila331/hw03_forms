from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Об авторе проекта'
        context['header'] = 'Привет, я автор'
        context['text'] = ('Я — увлекающийся человек, поэтому '
                           'решил освоить прогроммирование'
                           'Мне всего 15 лет, но чуствую я себя на все 20'
                           'На этом сложном и долгом пути'
                           'меня никто не поддерживает'
                           'Друзья считают что это фигня ,'
                           'но я мечтаю стать программистов '
                           'и поступить в ВШЭ'
                           'программистов и поступить в ВШЭ')
        return context


class AboutTechView(TemplateView):
    template_name = 'about/tech.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Технологии'
        context['header'] = 'Вот что я умею'
        context['text'] = ('Спасибо яндекс практикуму если'
                           'бы не они я бы не смог сделать этот сайт'
                           'бы не они я бы не смог сделать этот сайт'
                           'Я использовал django , html , css')
        return context
