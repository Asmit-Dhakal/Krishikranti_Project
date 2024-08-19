from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from PIL import Image
import torchvision.transforms as tt
import torch
from django.views.decorators.csrf import csrf_exempt
from .load_model import model
from .serializers import PredictionSerializer
from .models import Disease

# Dictionary mapping index to label name
classes = {
    0: 'bacterial_leaf_blight',
    1: 'brown_spot',
    2: 'healthy',
    3: 'leaf_blast',
    4: 'leaf_scald',
    5: 'narrow_brown_spot'
}

# Normalization for validation
stats = ((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
valid_tfms = tt.Compose([
    tt.Resize((32, 32)),  # Resize images to 32x32 pixels
    tt.ToTensor(),
    tt.Normalize(*stats)
])

class PredictView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        if 'image' not in request.FILES:
            return Response({'error': 'POST request with image file required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Open the uploaded image file
            image = Image.open(request.FILES['image'])

            # Save the image to the 'media' folder
            image_path = f'media/uploads/{request.FILES["image"].name}'
            image.save(image_path)

            # Preprocess the image
            image = valid_tfms(image)
            image = image.unsqueeze(0)  # Add batch dimension

            # Perform inference
            with torch.no_grad():
                output = model(image)

            # Process output (example: convert to label)
            _, predicted = torch.max(output, 1)
            predicted_label = classes[predicted.item()]  # Convert tensor to a Python integer

            # Get the solution for the predicted disease from the database
            try:
                disease = Disease.objects.get(name=predicted_label)
                solution = disease.solution
            except Disease.DoesNotExist:
                solution = 'No solution available.'

            # Serialize response
            serializer = PredictionSerializer(data={'prediction': predicted_label, 'solution': solution})
            serializer.is_valid(raise_exception=True)

            return Response(serializer.validated_data)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def test_upload(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            # Optionally, save the file to a directory
            # For example:
            # with open(f'uploaded_images/{file.name}', 'wb+') as destination:
            #     for chunk in file.chunks():
            #         destination.write(chunk)

            return JsonResponse({'message': f'File {file.name} uploaded successfully'})
        else:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)
