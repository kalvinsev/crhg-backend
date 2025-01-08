from django.urls import path
from .views import (
    PatientViewSet, AddNodeView, AddEdgeView, DeleteEdgeView, DeleteNodeView, UpdateNodeLabelView, GetPatientNodesView, GetPatientByNameView, UpdateNodePositionView, UpdateAllNodePositionsView
)

urlpatterns = [
    path('patients/', PatientViewSet.as_view(), name='create-patient'),
    path('patients/search/', GetPatientByNameView.as_view(), name='get_patient_by_name'),
    path('patients/<int:patient_id>/nodes/', GetPatientNodesView.as_view(), name="get_patient_nodes"),
    path('patients/<int:patient_id>/add-node/', AddNodeView.as_view(), name='add-node'),
    path('patients/<int:patient_id>/delete-node/<str:node_id>/', DeleteNodeView.as_view(), name='delete-node'),
    path('patients/<int:patient_id>/add-edge/', AddEdgeView.as_view(), name='add-edge'),
    path('patients/<int:patient_id>/delete-edge/<str:edge_id>/', DeleteEdgeView.as_view(), name='delete-edge'),
    path('patients/<int:patient_id>/update-node/<str:node_id>/', UpdateNodeLabelView.as_view(), name='update-node-label'),
    # path('patients/<int:patient_id>/update-node-position/<str:node_id>/', UpdateNodePositionView.as_view(), name='update-node-position'),
    path('patients/<int:patient_id>/update-node-positions/', UpdateAllNodePositionsView.as_view(), name='update-all-node-positions'),

]