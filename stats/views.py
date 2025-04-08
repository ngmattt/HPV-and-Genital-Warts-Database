from django.shortcuts import render, get_object_or_404
from .models import WartsStats, Region, AgeGroup, GenderOrientation
from django.db.models import Sum

def home(request):
    selected_year = request.GET.get('year')
    selected_gender = request.GET.get('gender')
    selected_age = request.GET.get('age')

    region_a_id = request.GET.get('region_a')
    region_b_id = request.GET.get('region_b')
    region_c_id = request.GET.get('region_c')

    england_stats = WartsStats.objects.filter(region__name='England')

    if selected_year:
        england_stats = england_stats.filter(year=selected_year)
    if selected_gender:
        england_stats = england_stats.filter(gender_orientation__label=selected_gender)
    if selected_age:
        england_stats = england_stats.filter(age_group__group_label=selected_age)

    table_stats = england_stats.exclude(age_group__group_label='Total').order_by('year', 'age_group__group_label')

    chart_qs = table_stats.values('year').annotate(total=Sum('diagnoses')).order_by('year')
    chart_data = {
        "labels": [entry['year'] for entry in chart_qs],
        "data": [entry['total'] for entry in chart_qs],
    }

    gender_qs = england_stats.values('gender_orientation__label').annotate(total=Sum('diagnoses')).order_by('-total')
    gender_chart_data = {
        "labels": [entry['gender_orientation__label'] for entry in gender_qs],
        "data": [entry['total'] for entry in gender_qs]
    }

    age_qs = england_stats.values('age_group__group_label').annotate(total=Sum('diagnoses')).order_by('age_group__group_label')
    age_chart_data = {
        "labels": [entry['age_group__group_label'] for entry in age_qs],
        "data": [entry['total'] for entry in age_qs]
    }

    def get_region_chart_data(region_id):
        if not region_id:
            return {}
        return dict(
            WartsStats.objects.filter(region__id=region_id)
            .values('year')
            .annotate(total=Sum('diagnoses'))
            .order_by('year')
            .values_list('year', 'total')
        )

    region_a_data = get_region_chart_data(region_a_id)
    region_b_data = get_region_chart_data(region_b_id)
    region_c_data = get_region_chart_data(region_c_id)

    all_years = sorted(set(region_a_data) | set(region_b_data) | set(region_c_data))
    region_compare_chart_data = {
        "labels": all_years,
        "region_a_data": [region_a_data.get(y, 0) for y in all_years],
        "region_b_data": [region_b_data.get(y, 0) for y in all_years],
        "region_c_data": [region_c_data.get(y, 0) for y in all_years],
        "region_a_name": Region.objects.get(id=region_a_id).name if region_a_id else "Region A",
        "region_b_name": Region.objects.get(id=region_b_id).name if region_b_id else "Region B",
        "region_c_name": Region.objects.get(id=region_c_id).name if region_c_id else "Region C",
    }

    years = WartsStats.objects.filter(region__name='England').values_list('year', flat=True).distinct().order_by('year')
    genders = GenderOrientation.objects.all()
    age_groups = AgeGroup.objects.exclude(group_label='Total')
    regions = Region.objects.exclude(name='England')

    return render(request, 'stats/home.html', {
        'england_stats': table_stats,
        'years': years,
        'genders': genders,
        'age_groups': age_groups,
        'selected_year': selected_year,
        'selected_gender': selected_gender,
        'selected_age': selected_age,
        'regions': regions,
        'chart_data': chart_data,
        'gender_chart_data': gender_chart_data,
        'age_chart_data': age_chart_data,
        'all_regions': Region.objects.all(),
        'selected_region_a': region_a_id,
        'selected_region_b': region_b_id,
        'selected_region_c': region_c_id,
        'region_compare_chart_data': region_compare_chart_data,
    })

def region_page(request, region_id):
    region = get_object_or_404(Region, id=region_id)

    selected_year = request.GET.get('year')
    selected_gender = request.GET.get('gender')
    selected_age = request.GET.get('age')

    region_stats = WartsStats.objects.filter(region=region)

    if selected_year:
        region_stats = region_stats.filter(year=selected_year)
    if selected_gender:
        region_stats = region_stats.filter(gender_orientation__id=selected_gender)
    if selected_age:
        region_stats = region_stats.filter(age_group__id=selected_age)

    table_stats = region_stats.exclude(age_group__group_label='Total').order_by('year', 'age_group__group_label')

    chart_qs = table_stats.values('year').annotate(total=Sum('diagnoses')).order_by('year')
    chart_data = {
        "labels": [entry['year'] for entry in chart_qs],
        "data": [entry['total'] for entry in chart_qs]
    }

    gender_qs = region_stats.values('gender_orientation__label').annotate(total=Sum('diagnoses')).order_by('-total')
    gender_chart_data = {
        "labels": [entry['gender_orientation__label'] for entry in gender_qs],
        "data": [entry['total'] for entry in gender_qs]
    }

    age_qs = region_stats.values('age_group__group_label').annotate(total=Sum('diagnoses')).order_by('age_group__group_label')
    age_chart_data = {
        "labels": [entry['age_group__group_label'] for entry in age_qs],
        "data": [entry['total'] for entry in age_qs]
    }

    years = WartsStats.objects.filter(region=region).values_list('year', flat=True).distinct().order_by('year')
    genders = GenderOrientation.objects.all()
    age_groups = AgeGroup.objects.exclude(group_label='Total')

    return render(request, 'stats/region.html', {
        'region': region,
        'region_stats': table_stats,
        'years': years,
        'genders': genders,
        'age_groups': age_groups,
        'selected_year': selected_year,
        'selected_gender': selected_gender,
        'selected_age_group': selected_age,
        'chart_years': chart_data["labels"],
        'chart_diagnoses': chart_data["data"],
        'gender_chart_data': gender_chart_data,
        'age_chart_data': age_chart_data,
    })

