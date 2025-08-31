from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User, House, Occupant, ChiefTenantAssignment
from .serializers import (
    UserSerializer, UserDetailSerializer,
    HouseSerializer, HouseDetailSerializer,
    OccupantSerializer, ChiefTenantAssignmentSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """
        Return detailed serializer for retrieve action
        """
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get'])
    def owners(self, request):
        """
        Get all users with owner role
        """
        owners = User.objects.filter(role='owner')
        serializer = self.get_serializer(owners, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def tenants(self, request):
        """
        Get all users with tenant role
        """
        tenants = User.objects.filter(role='tenant')
        serializer = self.get_serializer(tenants, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def properties(self, request, pk=None):
        """
        Get properties owned by a specific user
        """
        user = self.get_object()
        if user.role != 'owner':
            return Response(
                {'error': 'User is not a property owner'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        houses = House.objects.filter(owner=user)
        serializer = HouseSerializer(houses, many=True)
        return Response(serializer.data)


class HouseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing houses
    """
    queryset = House.objects.select_related('owner').prefetch_related('occupants')
    serializer_class = HouseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """
        Return detailed serializer for retrieve action
        """
        if self.action == 'retrieve':
            return HouseDetailSerializer
        return HouseSerializer
    
    def get_queryset(self):
        """
        Filter houses based on user role
        """
        user = self.request.user
        if user.role == 'owner':
            # Owners can only see their own properties
            return House.objects.filter(owner=user).select_related('owner').prefetch_related('occupants')
        elif user.role == 'admin':
            # Admins can see all properties
            return House.objects.select_related('owner').prefetch_related('occupants')
        else:
            # Tenants can see all properties (for browsing)
            return House.objects.select_related('owner').prefetch_related('occupants')
    
    @action(detail=True, methods=['get'])
    def occupants(self, request, pk=None):
        """
        Get all occupants of a specific house
        """
        house = self.get_object()
        occupants = house.occupants.all()
        serializer = OccupantSerializer(occupants, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def chief_tenant(self, request, pk=None):
        """
        Get active chief tenant assignment for a house
        """
        house = self.get_object()
        assignment = ChiefTenantAssignment.objects.filter(
            house=house, is_active=True
        ).first()
        
        if assignment:
            serializer = ChiefTenantAssignmentSerializer(assignment)
            return Response(serializer.data)
        else:
            return Response(
                {'message': 'No active chief tenant assignment for this house'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """
        Get houses filtered by house type
        """
        house_type = request.query_params.get('type')
        if not house_type:
            return Response(
                {'error': 'House type parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        houses = self.get_queryset().filter(house_type=house_type)
        serializer = self.get_serializer(houses, many=True)
        return Response(serializer.data)


class OccupantViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing occupants
    """
    queryset = Occupant.objects.select_related('house', 'house__owner')
    serializer_class = OccupantSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter occupants based on user role
        """
        user = self.request.user
        if user.role == 'owner':
            # Owners can only see occupants of their properties
            return Occupant.objects.filter(house__owner=user).select_related('house', 'house__owner')
        elif user.role == 'admin':
            # Admins can see all occupants
            return Occupant.objects.select_related('house', 'house__owner')
        else:
            # Tenants can see all occupants
            return Occupant.objects.select_related('house', 'house__owner')
    
    @action(detail=False, methods=['get'])
    def chief_tenants(self, request):
        """
        Get all occupants who are chief tenants
        """
        chief_tenants = self.get_queryset().filter(is_chief_tenant=True)
        serializer = self.get_serializer(chief_tenants, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_house(self, request):
        """
        Get occupants filtered by house ID
        """
        house_id = request.query_params.get('house_id')
        if not house_id:
            return Response(
                {'error': 'House ID parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        occupants = self.get_queryset().filter(house_id=house_id)
        serializer = self.get_serializer(occupants, many=True)
        return Response(serializer.data)


class ChiefTenantAssignmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing chief tenant assignments
    """
    queryset = ChiefTenantAssignment.objects.select_related('user', 'house')
    serializer_class = ChiefTenantAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter assignments based on user role
        """
        user = self.request.user
        if user.role == 'owner':
            # Owners can only see assignments for their properties
            return ChiefTenantAssignment.objects.filter(house__owner=user).select_related('user', 'house')
        elif user.role == 'admin':
            # Admins can see all assignments
            return ChiefTenantAssignment.objects.select_related('user', 'house')
        else:
            # Tenants can see their own assignments
            return ChiefTenantAssignment.objects.filter(user=user).select_related('user', 'house')
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Get all active chief tenant assignments
        """
        active_assignments = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(active_assignments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """
        Deactivate a chief tenant assignment
        """
        assignment = self.get_object()
        assignment.is_active = False
        assignment.save()
        
        serializer = self.get_serializer(assignment)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """
        Activate a chief tenant assignment
        """
        assignment = self.get_object()
        assignment.is_active = True
        assignment.save()
        
        serializer = self.get_serializer(assignment)
        return Response(serializer.data)
