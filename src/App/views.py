from django.shortcuts import render, redirect
from App.models import Person, RealEstateUnit, Partner

from App.forms import PersonForm

def index(request):
    return render(request, 'index.html',
                  {'persons': Person.nodes.all(),
                   'units': RealEstateUnit.nodes.all(),
                   'partners': Partner.nodes.all()})


def create(request):
    # create nodes
    satra = Person(nickname='satra').save()
    rsl13 = RealEstateUnit(street="Rice Spring Ln",
                           zipcode="01778",
                           number="13", unittype="R").save()
    rsl13.persons.connect(satra, {'relation': 'O'})
    satra.units.connect(rsl13, {'relation': 'O'})

    pearl_admin = Person(nickname='pearl').save()
    pearl = Partner(legal_name="Pearl", legal_address="some place, state, zip",
                    coverage_area="Wayland",
                    mou_signed=True).save()
    pearl.contacts.connect(pearl_admin)
    return redirect('/')


def person_new(request):
    if request.method == "POST":
        print(request.POST)
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.save()
            return redirect('/')
    else:
        form = PersonForm()
    return render(request, 'person_edit.html', {'form': form})