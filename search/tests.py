from django.test import TestCase
from search.models import User
from django.test import Client
from django.urls import reverse_lazy


# python manage.py test search.tests.Test
class Test(TestCase):
    client = Client()
    url = reverse_lazy('search')

    def setUp(self):
        pass

    # python manage.py test search.tests.Test.test_count_is_100
    def test_count_is_30(self):
        assert(User.objects.count()) == 30

    def test_5_results_with_dave_as_q(self):
        url = self.url + "?q=dave"
        data = self.client.get(url).json()
        assert(data["count"] == 5)
        assert(len(data["results"])) == 5

    def test_account_created_before_and_fullname_john(self):
        url = self.url + "?q=Jonn+created:<2014-05-18+in:fullname"
        data = self.client.get(url).json()
        assert(data["count"] == 1)
        assert(data["results"][0]["first_name"]) == "Jonn"

    def test_has_next_only(self):
        url = self.url + "?q="
        data = self.client.get(url).json()
        assert(data["count"] == 30)
        assert(data["next"] == "http://testserver/search/users/?page=2&q=")
        assert(data["previous"] == "")

    def test_has_next_and_previous(self):
        url = self.url + "?q=&page=2"
        data = self.client.get(url).json()
        assert(data["count"] == 30)
        assert(data["next"] == "http://testserver/search/users/?page=3&q=")
        assert(data["previous"] == "http://testserver/search/users/?page=1&q=")

    def test_has_only_previous(self):
        url = self.url + "?q=&page=3"
        data = self.client.get(url).json()
        assert(data["count"] == 30)
        assert(data["next"] == "")
        assert(data["previous"] == "http://testserver/search/users/?page=2&q=")

    def test_18_results_for_score_greater_than_70(self):
        url = self.url + "?&q=score:<70"
        data = self.client.get(url).json()
        assert(data["count"] == 18)

    def test_2_results_for_score_greater_than_70_and_followers_less_than_70(self):
        url = self.url + "?&q=score:<70+followers:<100"
        data = self.client.get(url).json()
        assert(data["count"] == 2)
        assert(data["results"][0]["email"] == "blevinsharmon@applidec.com")

# https://www.json-generator.com/
# [
#   '{{repeat(100)}}',
#   {
#     score: '{{floating(0, 99, 2)}}',
#     followers: '{{integer(0, 1000)}}',
#     repos: '{{integer(1, 300)}}',
#     first_name: '{{firstName()}}',
#     last_name: '{{surname()}}',
#     username: '{{firstName()}}_{{surname()}}',
#     email: '{{email()}}',
#     created: '{{date(new Date(2014, 0, 1), new Date(), "YYYY-MM-ddThh:mm:ss Z")}}',
#     location: function () {
#       var items = ['Guthrie, Wyoming, 6448',
#                    'Gardners, South Dakota, 6741',
#                    'Tivoli, South Carolina, 9798',
#                    'Bynum, North Dakota, 2171',
#                    'Witmer, Idaho, 9605',
#                    'Hall, Guam, 3104',
#                    'Sanford, Connecticut, 8617',
#                    'Chesapeake, Pennsylvania, 9417'
#                   ];
#       return items[Math.floor(Math.random()*items.length)];
#     },


#     type: function () {
#       var items = ['org', 'user'];
#       return items[Math.floor(Math.random()*items.length)];

#     }

#   }
# ]
