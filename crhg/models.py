from django.db import models
from uuid import uuid4

class Patient(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Each patient must have a unique name


class Node(models.Model):
    patient = models.ForeignKey(Patient, related_name="nodes", on_delete=models.CASCADE)  # Link to a single patient
    node_id = models.CharField(max_length=50)  # Node ID unique within patients
    position = models.JSONField()  # Storing x and y as a JSON object
    data = models.JSONField()  # Storing label as part of data
    type = models.CharField(max_length=50)
    measured = models.JSONField()
    selected = models.BooleanField(default=False)
    dragging = models.BooleanField(default=False)

    class Meta:
        unique_together = ('patient', 'node_id')  # Ensure uniqueness within a patient


class Edge(models.Model):
    patient = models.ForeignKey(Patient, related_name="edges", on_delete=models.CASCADE)  # Link to a single patient
    edge_id = models.CharField(max_length=50)  # Edge ID unique within patients
    source = models.CharField(max_length=50)  # Source node ID
    target = models.CharField(max_length=50)  # Target node ID

    class Meta:
        unique_together = ('patient', 'edge_id')  # Ensure uniqueness within a patient
