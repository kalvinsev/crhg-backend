from rest_framework import serializers
from .models import Patient, Node, Edge


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['node_id', 'patient', 'position', 'data', 'type', 'measured', 'selected', 'dragging']


class EdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edge
        fields = ['edge_id', 'patient', 'source', 'target']


class PatientSerializer(serializers.ModelSerializer):
    nodes = NodeSerializer(many=True, read_only=True)  # Nested serializer for nodes
    edges = EdgeSerializer(many=True, read_only=True)  # Nested serializer for edges

    class Meta:
        model = Patient
        fields = ['id', 'name', 'nodes', 'edges']

    def create(self, validated_data):
        patient = Patient.objects.create(**validated_data)

        # Add a default node
        Node.objects.create(
            patient=patient,
            node_id="1",  # Ensure "1" is the first node for this patient
            position={"x": 0, "y": 0},
            data={"label": "Default Node"},
            type="customNode",
            measured={"width": 220, "height": 44},
            selected=False,
            dragging=False
        )

        return patient
