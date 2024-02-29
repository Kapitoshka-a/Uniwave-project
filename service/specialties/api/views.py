from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import NotFound
from django.db.models import Prefetch

from .serializers import *
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly


# Create your views here.
class SpecialtiesList(generics.ListAPIView):
    """ Endpoint to list all specialties """
    serializer_class = SpecialtyListSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name_of_spec', 'number_of_spec', 'branch']
    ordering_fields = ['average_budget_mark', 'time_of_study', 'average_budget_mark']

    def get_queryset(self):
        """Information to get from specialty"""
        return Specialty.objects.all().prefetch_related(
            Prefetch('university', queryset=University.objects.all())
        ).only(
            'name_of_spec', 'branch', 'number_of_spec', 'faculty',
            'average_budget_mark', 'average_contract_mark',
            'university', 'id', 'slug'
        )


class SpecialtyDetail(APIView):
    """Endpoint to get specific detail about a specific specialty"""
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, slug):
        """Get specialty details"""
        try:
            specialty = Specialty.objects.get(slug=slug)
        except Specialty.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SpecialtyDetailSerializer(specialty, context={'request': request})
        return Response(serializer.data)

    def put(self, request, slug):
        """Update specialty details"""
        specialty = Specialty.objects.get(slug=slug)
        serializer = SpecialtyDetailSerializer(specialty, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        """Delete specialty details"""
        specialty = Specialty.objects.get(slug=slug)
        specialty.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UniversityList(generics.ListAPIView):
    """Endpoint to get all universities"""
    serializer_class = UniversityListSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        """Query set for universities"""
        return University.objects.all()


class UniversityDetail(APIView):
    """Endpoint to get specific university details"""
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        """Get university details"""
        try:
            university = University.objects.get(pk=pk)
        except University.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UniversityDetailSerializer(university, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        """Update university details"""
        university = University.objects.get(pk=pk)
        serializer = UniversityDetailSerializer(university, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """delete universities details"""
        university = University.objects.get(pk=pk)
        university.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListCreate(generics.ListCreateAPIView):
    """Endpoint to get all comments or create own for a specific specialty"""
    queryset = Comment.objects.all()
    serializer_class = SpecialtyCommentSerializer

    def get_queryset(self):
        """Query set for retrieving all comments for specialty"""
        slug = self.kwargs.get('slug')
        try:
            comments = Comment.objects.filter(specialty__slug=slug)
            return comments
        except Comment.DoesNotExist:
            raise NotFound("Comments for this specialty do not exist.")

    def perform_create(self, serializer):
        """Create e new comment"""
        slug = self.kwargs.get('slug')
        specialty = generics.get_object_or_404(Specialty, slug=slug)
        if Comment.objects.filter(specialty=specialty, author=self.request.user).exists():
            raise serializers.ValidationError({'Message': 'You have already added comment on this specialty'})
        serializer.save(author=self.request.user, specialty=specialty)


class CommentDetail(APIView):
    """Endpoint to get specific detail about a comment"""

    def get(self, request, slug, pk):
        """Get specific comment"""
        try:
            comment = Comment.objects.get(pk=pk)
        except Specialty.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SpecialtyCommentSerializer(comment, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        """Update a comment"""
        comment = Comment.objects.get(pk=pk)
        serializer = SpecialtyCommentSerializer(comment, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete a comment"""
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
