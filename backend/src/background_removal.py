import torch
from PIL import Image
import numpy as np
from u2net_model import U2NET
import os

def get_model_and_device(model_path="models/u2net.pth"):
    """Initialize model and device"""
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    net = U2NET(3, 1)
    
    try:
        # Try loading with weights_only=False for compatibility
        state_dict = torch.load(model_path, map_location=device, weights_only=False)
        net.load_state_dict(state_dict)
    except TypeError:
        # Fallback for older PyTorch versions
        state_dict = torch.load(model_path, map_location=device)
        net.load_state_dict(state_dict)

    net.to(device)
    net.eval()
    return net, device

def generate_mask(input_path, model_path="models/u2net.pth"):
    """Perform AI inference to generate the background mask"""
    net, device = get_model_and_device(model_path)
    
    image = Image.open(input_path).convert('RGB')
    orig_size = image.size

    # Preprocess
    image_resized = image.resize((320, 320))
    img_np = np.array(image_resized).astype(np.float32) / 255.0
    img_np = img_np.transpose((2, 0, 1))
    img_tensor = torch.from_numpy(img_np).unsqueeze(0).to(device)

    # Predict mask
    with torch.no_grad():
        d1, *_ = net(img_tensor)
    
    pred = d1[:, 0, :, :].cpu().numpy()[0]
    pred = (pred - pred.min()) / (pred.max() - pred.min())
    mask = Image.fromarray((pred * 255).astype(np.uint8)).resize(orig_size, Image.LANCZOS)
    return mask

def apply_mask(input_path, mask):
    """Apply the mask to the original image to create a transparent PNG"""
    image_rgba = Image.open(input_path).convert('RGBA')
    mask_np = np.array(mask) / 255.0
    img_np = np.array(image_rgba)
    img_np[..., 3] = (mask_np * 255).astype(np.uint8)
    return Image.fromarray(img_np, 'RGBA')

def resize_and_format(image, resolution="original", export_format="png"):
    """Resize based on resolution and orientation, then apply selected format"""
    # Ensure RGBA mode so transparency is always available
    result = image.convert('RGBA')
    
    # Resize the result based on the selected resolution
    if resolution != "original":
        # Standard resolutions (landscape)
        resolutions = {
            "hd": (1280, 720),
            "fullhd": (1920, 1080),
            "4k": (3840, 2160)
        }

        if resolution not in resolutions:
            target_width, target_height = 1280, 720 # Default to HD if unknown
        else:
            target_width, target_height = resolutions[resolution]
            
        orig_width, orig_height = result.size
        
        # Determine orientation
        is_portrait = orig_height > orig_width
        
        # If portrait, swap target dimensions
        if is_portrait:
            target_width, target_height = target_height, target_width

        aspect_ratio = orig_width / orig_height

        if target_width / target_height > aspect_ratio:
            # Adjust width to maintain aspect ratio
            target_width = int(target_height * aspect_ratio)
        else:
            # Adjust height to maintain aspect ratio
            target_height = int(target_width / aspect_ratio)

        new_size = (target_width, target_height)
        result = result.resize(new_size, Image.LANCZOS)

    # Handle export format
    export_format = export_format.lower()
    
    if export_format == "webp":
        save_format = "WEBP"
    else:
        save_format = "PNG"
    
    return result, save_format

def remove_background(input_path, output_path, resolution="original", export_format="png", model_path="models/u2net.pth"):
    """Legacy wrapper for backward compatibility"""
    mask = generate_mask(input_path, model_path)
    master = apply_mask(input_path, mask)
    final_image, save_format = resize_and_format(master, resolution, export_format)
    final_image.save(output_path, format=save_format)
    return output_path
