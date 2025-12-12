import torch
from diffusers import StableDiffusionXLPipeline, StableDiffusionXLImg2ImgPipeline, AutoencoderKL, DPMSolverMultistepScheduler
import os

class ImageService:
    def __init__(self, model_id="data/models/CHEYENNE_v22VAEBaked.safetensors", device="cuda"):
        self.device = device
        self.model_id = model_id
        self.pipe = None
        self.refiner = None

    def load_model(self):
        if self.pipe is not None:
            return

        print(f"Loading custom model from {self.model_id}...")
        try:
            # Load VAE separately to avoid OOM
            vae = AutoencoderKL.from_pretrained("madebyollin/sdxl-vae-fp16-fix", torch_dtype=torch.float16)

            if os.path.exists(self.model_id) and (self.model_id.endswith(".safetensors") or self.model_id.endswith(".ckpt")):
                print(f"Detected local single-file checkpoint: {self.model_id}")
                self.pipe = StableDiffusionXLPipeline.from_single_file(
                    self.model_id,
                    vae=vae,
                    torch_dtype=torch.float16,
                    original_config_file=None, # Auto-detect
                )
            else:
                self.pipe = StableDiffusionXLPipeline.from_pretrained(
                    self.model_id,
                    vae=vae,
                    torch_dtype=torch.float16,
                )
            
            # Switch to DPM++ 2M SDE Karras as requested
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipe.scheduler.config,
                use_karras_sigmas=True,
                algorithm_type="sde-dpmsolver++"
            )
            
            # Optimization for <8GB VRAM
            # self.pipe.to(self.device) # Do not move to device manually when using sequential offload
            self.pipe.enable_sequential_cpu_offload() # Stronger offload than model_cpu_offload
            self.pipe.enable_vae_slicing()
            self.pipe.enable_vae_tiling()
            self.pipe.enable_attention_slicing() # Reduces VRAM further
             
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Failed to load model: {e}")
            raise e

    def generate_image(self, prompt, output_path, negative_prompt="simple background", steps=30, upscale=False, seed=None, guidance_scale=3.5, width=832, height=1216):
        if self.pipe is None:
            self.load_model()
        
        # Generator for seed
        generator = None
        if seed is not None:
            generator = torch.Generator(device=self.device).manual_seed(seed)
        
        # 1. Generate High-Quality Image directly
        # Playground v2.5 / Cheyenne Optimized parameters
        
        style_suffix = ", detailed, sharp, HD, HDR, best quality, best resolution, 2D, colored Graphic Novel illustration, By Gibrat, hatching, lineart, sketch, hyper illustration, vibrant, saturated"
        if style_suffix.strip() not in prompt:
            prompt = prompt + style_suffix
            
        print(f"Generating image ({width}x{height}) with Custom Model...")
        print(f"Settings: Steps={steps}, CFG={guidance_scale}, Seed={seed}")
        
        final_image = self.pipe(
            prompt=prompt, 
            negative_prompt=negative_prompt, 
            num_inference_steps=steps, 
            guidance_scale=guidance_scale,
            width=width, 
            height=height,
            generator=generator
        ).images[0]

        # Refiner removed to save VRAM and because Playground v2.5 is high quality enough

        final_image.save(output_path)
        print(f"Saved to {output_path}")
        return output_path
