
from rest_framework import serializers
from .models import User, House, Occupant, ChiefTenantAssignment


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'role', 'date_joined', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'date_joined': {'read_only': True},
        }
    
    def create(self, validated_data):
        """
        Create a new user with encrypted password
        """
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        """
        Update user instance, handling password separately
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


class HouseSerializer(serializers.ModelSerializer):
    """
    Serializer for House model
    """
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)
    total_occupants = serializers.SerializerMethodField()
    
    class Meta:
        model = House
        fields = [
            'id', 'owner', 'owner_email', 'owner_name', 'house_type', 
            'house_number', 'num_apartments', 'total_occupants',
            'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
    
    def get_total_occupants(self, obj):
        """
        Get total number of occupants in this house
        """
        return obj.occupants.count()
    
    def validate_owner(self, value):
        """
        Validate that the owner has the 'owner' role
        """
        if value.role != 'owner':
            raise serializers.ValidationError(
                "Only users with 'owner' role can own houses."
            )
        return value


class OccupantSerializer(serializers.ModelSerializer):
    """
    Serializer for Occupant model
    """
    house_address = serializers.CharField(source='house.house_number', read_only=True)
    house_type = serializers.CharField(source='house.house_type', read_only=True)
    
    class Meta:
        model = Occupant
        fields = [
            'id', 'house', 'house_address', 'house_type', 'full_name', 
            'apartment_number', 'is_chief_tenant', 'move_in_date', 'created_at'
        ]
        extra_kwargs = {
            'move_in_date': {'read_only': True},
            'created_at': {'read_only': True},
        }
    
    def validate(self, data):
        """
        Validate apartment number uniqueness within the house
        """
        house = data.get('house')
        apartment_number = data.get('apartment_number')
        
        if house and apartment_number:
            # Check if apartment number already exists in this house
            existing_occupant = Occupant.objects.filter(
                house=house, 
                apartment_number=apartment_number
            ).exclude(id=self.instance.id if self.instance else None)
            
            if existing_occupant.exists():
                raise serializers.ValidationError({
                    'apartment_number': f'Apartment {apartment_number} is already occupied in this house.'
                })
        
        return data


class ChiefTenantAssignmentSerializer(serializers.ModelSerializer):
    """
    Serializer for ChiefTenantAssignment model
    """
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    house_address = serializers.CharField(source='house.house_number', read_only=True)
    
    class Meta:
        model = ChiefTenantAssignment
        fields = [
            'id', 'user', 'user_email', 'user_name', 'house', 'house_address',
            'assignment_date', 'is_active', 'created_at'
        ]
        extra_kwargs = {
            'assignment_date': {'read_only': True},
            'created_at': {'read_only': True},
        }
    
    def validate_user(self, value):
        """
        Validate that the user has the 'tenant' role
        """
        if value.role != 'tenant':
            raise serializers.ValidationError(
                "Only users with 'tenant' role can be assigned as chief tenants."
            )
        return value
    
    def validate(self, data):
        """
        Validate that user doesn't already have an active assignment
        """
        user = data.get('user')
        is_active = data.get('is_active', True)
        
        if user and is_active:
            existing_assignment = ChiefTenantAssignment.objects.filter(
                user=user, 
                is_active=True
            ).exclude(id=self.instance.id if self.instance else None)
            
            if existing_assignment.exists():
                raise serializers.ValidationError({
                    'user': 'This user already has an active chief tenant assignment.'
                })
        
        return data


# Nested serializers for detailed views
class HouseDetailSerializer(HouseSerializer):
    """
    Detailed serializer for House with occupants and chief tenant info
    """
    occupants = OccupantSerializer(many=True, read_only=True)
    chief_tenant_assignments = ChiefTenantAssignmentSerializer(many=True, read_only=True)
    
    class Meta(HouseSerializer.Meta):
        fields = HouseSerializer.Meta.fields + ['occupants', 'chief_tenant_assignments']


class UserDetailSerializer(UserSerializer):
    """
    Detailed serializer for User with owned houses and assignments
    """
    owned_houses = HouseSerializer(many=True, read_only=True)
    chief_tenant_assignment = ChiefTenantAssignmentSerializer(read_only=True)
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['owned_houses', 'chief_tenant_assignment']
