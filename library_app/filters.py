import django_filters
from django_filters import *
from .models import *

class IssueFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name="date_of_issue", lookup_expr='gte')
	end_date = DateFilter(field_name="date_of_issue", lookup_expr='lte')
	status = CharFilter(field_name='status', lookup_expr='icontains')
	book_category = ModelChoiceFilter(label='Book Category',field_name='book__category' ,queryset=Category.objects.all())

	class Meta:
		model = Issue
		fields = '__all__'
		exclude = ['user', 'date_of_issue']

class BookFilter(django_filters.FilterSet):
	title = CharFilter(field_name='title', lookup_expr='icontains')
	start_date = DateFilter(field_name="date_of_publication", lookup_expr='gte')
	end_date = DateFilter(field_name="date_of_publication", lookup_expr='lte')
	min_copies = CharFilter(field_name="num_copies", lookup_expr='gte')
	max_copies = CharFilter(field_name="num_copies", lookup_expr='lte')

	author = ModelMultipleChoiceFilter(label='Author(s)',queryset=Author.objects.all())

	class Meta:
		model = Book
		fields = '__all__'
		exclude = ['author', 'num_copies','date_of_publication']