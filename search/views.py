from django.http import Http404
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status

from search.models import User, Search
from search.serializers import UserSerializer
from rest_framework import generics
from collections import OrderedDict
import re
from rest_framework.utils.urls import replace_query_param


# http://127.0.0.1:8000/search/users/?q=1+in:fullname
class UserSearch(generics.ListAPIView):
    limit = 10
    serializer_class = UserSerializer
    valid_user_types = [utype[0] for utype in User.TYPES]
    valid_sort_keys = ('followers', 'repos', 'created')

    @staticmethod
    def get_names_search(search_key, ORs):
        names = search_key.split(" ")
        for name in names:
            ORs = ORs | Q(first_name__icontains=name) | Q(last_name__icontains=name)
        return ORs

    def fetch_qualifiers(self, query):
        qualifier_pattern = r'\w+:[><]?\w[\w-]+'
        gte_qaulifiers_pattern = r'\w+:>\w[\w-]+'
        lte_qaulifiers_pattern = r'\w+:<\w[\w-]+'
        e_qaulifiers_pattern = r'\w+:\w[\w-]+'
        in_qualifiers = r'in:\w+'

        search_key = re.split(qualifier_pattern, query)[0].strip(' ')
        gte_qaulifiers = re.findall(gte_qaulifiers_pattern, query)
        lte_qaulifiers = re.findall(lte_qaulifiers_pattern, query)
        in_qualifiers = re.findall(in_qualifiers, query)
        e_qualifiers = re.findall(e_qaulifiers_pattern, query)

        # for qal in in_qualifiers:
        #     e_qualifiers.remove(qal)

        ORs = Q()
        if not in_qualifiers:
            ORs = Q(email__icontains=search_key) | Q(username__icontains=search_key)
            ORs = self.get_names_search(search_key, ORs)
        else:
            if "in:email" in in_qualifiers:
                ORs = ORs | Q(email__icontains=search_key)

            if "in:login" in in_qualifiers:
                ORs = ORs | Q(username__icontains=search_key)

            if "in:fullname" in in_qualifiers:
                ORs = self.get_names_search(search_key, ORs)

        ANDs = {}
        # select greater than qaulifier over less than.
        comparison_keys = ['respos', 'followers', 'created', 'score']
        for qal in lte_qaulifiers:
            key, val = qal.split(":<")
            if key in comparison_keys:
                ANDs['{}__lte'.format(key)] = val

        for qal in gte_qaulifiers:
            key, val = qal.split(":>")
            if key in comparison_keys:
                ANDs['{}__gte'.format(key)] = val

        equal_keys = ['location', 'type'] + comparison_keys

        for qal in e_qualifiers:
            key, val = qal.split(":")
            if val in equal_keys:
                if val == "location":
                    ANDs['{}__icontains'.format(val)] = search_key
                else:
                    ANDs[key] = val

        # print("ANDS", ANDs)
        # print("ORs", ORs)

        return ORs, ANDs

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        url = self.request.build_absolute_uri()
        if self.page * self.limit >= self.total:
            next_url = ""
        else:
            next_url = replace_query_param(url, "page", self.page+1)
        if self.page == 1:
            previous_url = ""
        else:
            previous_url = replace_query_param(url, "page", self.page-1)

        return Response(OrderedDict([
            ('count', self.total),
            ('next', next_url),
            ('previous', previous_url),
            ('results', serializer.data)
        ]))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        # filtering
        query = self.request.query_params.get("q", "")
        ORs, ANDs = self.fetch_qualifiers(query)
        users = User.objects.filter(ORs).filter(**ANDs)

        # sorting
        sort_values = self.request.query_params.get("sort", "")
        sort_values = sort_values.split(",")
        if sort_values == ['']:
            users = users.order_by('-followers', '-repos', '-created')
        else:
            sort_values = filter(lambda x: x.strip("-") in self.valid_sort_keys, sort_values)
            sort_values = [x for x in sort_values]
            for sort_value in sort_values:
                users = users.order_by(sort_value)

        # pagination
        page = self.request.query_params.get("page", 1)
        self.page = int(page)
        limit = 10
        offset = (int(page) - 1) * limit
        self.total = users.count()
        users = users[offset:limit+offset]

        # print(users.query)
        # adding search call to DB
        Search.objects.create(query=query)
        return users


class UserList(APIView):
    """
    List all Users, or create a new User.
    """
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    Retrieve, update or delete a User instance.
    """
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        User = self.get_object(pk)
        serializer = UserSerializer(User)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        User = self.get_object(pk)
        serializer = UserSerializer(User, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        User = self.get_object(pk)
        User.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
