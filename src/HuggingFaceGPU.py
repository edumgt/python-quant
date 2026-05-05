from diffusers import StableDiffusionPipeline
import torch

# GPU로 파이프라인 로딩
model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    guidance_scale=9.9,
    height=1280,   # 높이
    width=720,      # 너비
    torch_dtype=torch.float16
).to("cuda")

# 프롬프트로 이미지 생성
prompt = "A full-body One Single Real humanoid mech inspired by Overwatch Hanzo, standing alone , "
prompt += "tactical armor plating , natural lighting at 3pm, desert asphalt plaza "
prompt += "background, color scheme is just gray and brown, sharp shadows, very high detailed textures"
image = pipe(prompt, guidance_scale=9).images[0]

# 저장
image.save("test.png")
print("✅ Diffusers GPU 이미지 생성 완료")
