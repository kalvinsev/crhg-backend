from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Patient, Node, Edge
from .serializers import PatientSerializer, NodeSerializer, EdgeSerializer
from rest_framework.exceptions import ValidationError


class PatientViewSet(APIView):
    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        print(serializer)
        print()
        for field in serializer.data:
            print(field['id'], field['name'])
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.save()
            return Response(PatientSerializer(patient).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetPatientByNameView(APIView):
    def get(self, request):
        # Get the patient name from the query parameters
        patient_name = request.query_params.get("name")
        print('patient name:', patient_name)
        if not patient_name:
            return Response({"error": "Name query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Search for the patient by name
            patient = Patient.objects.get(name=patient_name)

            # Serialize the patient data, including nodes and edges
            serializer = PatientSerializer(patient)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Patient.DoesNotExist:
            return Response({"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)



class AddNodeView(APIView):
    def post(self, request, patient_id):
        try:
            patient = Patient.objects.get(id=patient_id)
            data = request.data.copy()
            data['patient'] = patient.id
            serializer = NodeSerializer(data=data)
            if serializer.is_valid():
                node = serializer.save()
                return Response(NodeSerializer(node).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)

class GetPatientNodesView(APIView):
    def get(self, request, patient_id):
        try: 
            # retreive patient by ID
            patient = Patient.objects.get(id=patient_id)

            # retreive all nodes related to the patient
            nodes = patient.nodes.all()
            
            # Serialize the nodes
            serializer = NodeSerializer(nodes, many=True)
            print(len(serializer.data))
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)

class AddEdgeView(APIView):
    def post(self, request, patient_id):
        try:
            patient = Patient.objects.get(id=patient_id)
            data = request.data.copy()
            data['patient'] = patient.id
            serializer = EdgeSerializer(data=data)
            if serializer.is_valid():
                edge = serializer.save()
                return Response(EdgeSerializer(edge).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)


class DeleteNodeView(APIView):
    def delete(self, request, patient_id, node_id):
        try:
            node = Node.objects.get(patient__id=patient_id, node_id=node_id)
            node.delete()
            return Response({"message": "Node deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Node.DoesNotExist:
            return Response({"error": "Node not found."}, status=status.HTTP_404_NOT_FOUND)


class DeleteEdgeView(APIView):
    def delete(self, request, patient_id, edge_id):
        try:
            edge = Edge.objects.get(patient__id=patient_id, edge_id=edge_id)
            edge.delete()
            return Response({"message": "Edge deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Edge.DoesNotExist:
            return Response({"error": "Edge not found."}, status=status.HTTP_404_NOT_FOUND)


class UpdateNodeLabelView(APIView):
    def patch(self, request, patient_id, node_id):
        try:
            node = Node.objects.get(patient__id=patient_id, node_id=node_id)
            # print(request.data.get('x'))
            new_x = request.data.get("x")
            new_y = request.data.get("y")
            print(new_x, new_y)
            new_label = request.data.get("label")
            print(new_label)
            if not new_label:
                return Response({"error": "Label is required."}, status=status.HTTP_400_BAD_REQUEST)

            node.data["label"] = new_label
            node.save()
            return Response(NodeSerializer(node).data, status=status.HTTP_200_OK)
        except Node.DoesNotExist:
            return Response({"error": "Node not found."}, status=status.HTTP_404_NOT_FOUND)
        
class UpdateNodePositionView(APIView):
    def patch(self, request, patient_id, node_id):
        try:
            node = Node.objects.get(patient__id=patient_id, node_id=node_id)
            new_x, new_y = request.data.get("x"), request.data.get("y") # Retreive updated x and y node values
            if not new_x or not new_y:
                return Response({"error": "Invalid positions"}, status=status.HTTP_400_BAD_REQUEST)

            node.position["x"], node.position["y"] = new_x, new_y
            node.save()
            return Response(NodeSerializer(node).data, status=status.HTTP_200_OK)
        except Node.DoesNotExist:
            return Response({"error": "Node not found."}, status=status.HTTP_404_NOT_FOUND)        

class UpdateAllNodePositionsView(APIView):
    def post(self, request, patient_id):
        try:
            patient = Patient.objects.get(id=patient_id)
            updated_nodes = request.data  # List of nodes with updated positions
            
            for node_data in updated_nodes:
                node_id = node_data.get("node_id")
                position = node_data.get("position")
                if not node_id or not position:
                    raise ValidationError(f"Node ID and position are required. Error in node: {node_data}")

                # Update the node
                node = Node.objects.get(patient=patient, node_id=node_id)
                node.position = position  # Update position field
                node.save()

            return Response({"message": "Node positions updated successfully."}, status=status.HTTP_200_OK)

        except Patient.DoesNotExist:
            return Response({"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)
        except Node.DoesNotExist:
            return Response({"error": f"Node not found for some nodes."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)