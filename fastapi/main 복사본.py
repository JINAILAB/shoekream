import gradio as gr
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import json

# JSON 파일에서 ImageNet 클래스 이름 목록 읽어오기
with open("imagenet_classes.json", "r") as f:
    imagenet_classes = json.load(f)
    
# ResNet-18 모델 로드 및 평가 모드로 설정
model = models.resnet101(pretrained=True)
model.eval()
# 이미지 분류를 위한 변환 정의
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def classify_image(image: Image.Image):
    # 이미지 변환 및 모델 입력을 위한 텐서로 변환
    image = Image.fromarray((image * 255).astype(np.uint8))
    image_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(image_tensor)
        prediction = torch.nn.functional.softmax(outputs[0], dim=0)
        confidences = {imagenet_classes[str(i)]: float(prediction[i]) for i in range(1000)}
        
    return confidences


# primary_color = gr.themes.Color("#FFD700")
# background_color = gr.themes.Color("#4B0082")
# text_color = gr.themes.Color("#FFFFFF")

# # 테마 생성
custom_theme = gr.themes.Default(primary_hue="gray").set(
    loader_color="#FF0000",
    slider_color="#FF0000",
    body_background_fill="#35363A", # 배경색
    block_background_fill="#3C4043",
    button_primary_background_fill="#6A84A6", # 버튼 색상
    button_primary_background_fill_hover="#88B6F2", # 버튼 눌렀을 때 색상
    button_primary_text_color="#D7D8D9",
    panel_background_fill="#121212", # 둘러싸고 있는 색상
    block_info_text_color="#D7D8D9" 
)

image_html = (
            "<div >"
            "<img src='file/shoekream_image.png'"
            + "</div>"
    )



# Gradio 인터페이스 정의 및 실행
interface = gr.Interface(fn=classify_image, 
                         inputs="image", 
                         outputs=gr.Label(num_top_classes=5),
                         examples=['airplane.jpeg', 'car.jpeg'],
                         description=image_html,  
                         theme=custom_theme)
interface.launch()
