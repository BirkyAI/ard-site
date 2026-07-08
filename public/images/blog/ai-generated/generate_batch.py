#!/usr/bin/env python3
"""Batch generate Antigua Guatemala blog images with ComfyUI API."""

import json
import urllib.request
import urllib.error
import time
import os
import uuid

COMFYUI_URL = "http://127.0.0.1:8188"
OUTPUT_DIR = "/Users/macminim4/websites/ard-site/public/images/blog/ai-generated"

# Extended golden-light Antigua prompts
PROMPTS = [
    {
        "name": "antigua-market-scene",
        "prompt": "soft golden morning light, vibrant local market in Antigua Guatemala, colorful fruits and vegetables, textile stalls, warm tones, dreamy atmosphere, professional travel photography, 4k",
        "topic": "Markets, local life, shopping"
    },
    {
        "name": "antigua-rooftop-view",
        "prompt": "soft golden hour light, rooftop terrace view in Antigua Guatemala, colorful colonial rooftops, Volcan de Fuego smoking in background, warm sunset tones, dreamy atmosphere, professional real estate photography, 4k",
        "topic": "Properties with views, rooftop terraces"
    },
    {
        "name": "antigua-arch-sunset",
        "prompt": "soft golden sunset light, famous Santa Catalina Arch Antigua Guatemala, cobblestone street, warm romantic tones, dreamy atmosphere, professional architectural photography, 4k",
        "topic": "Iconic landmarks, romantic Antigua"
    },
    {
        "name": "antigua-garden-pool",
        "prompt": "soft diffused light, luxury colonial villa garden in Antigua Guatemala, swimming pool, tropical flowers, bougainvillea, warm golden tones, dreamy resort atmosphere, professional real estate photography, 4k",
        "topic": "Luxury homes, gardens, pools"
    },
    {
        "name": "antigua-church-interior",
        "prompt": "soft warm candlelight, beautiful colonial church interior in Antigua Guatemala, golden altar, ornate decorations, warm amber tones, dreamy spiritual atmosphere, professional interior photography, 4k",
        "topic": "Churches, interiors, culture"
    },
    {
        "name": "antigua-coffee-farm",
        "prompt": "soft golden morning light, coffee plantation in Guatemala highlands near Antigua, lush green coffee plants, volcanic soil, warm tropical tones, dreamy countryside atmosphere, professional agricultural photography, 4k",
        "topic": "Coffee country, rural properties"
    },
    {
        "name": "antigua-volcano-sunset",
        "prompt": "soft dramatic sunset light, Volcan de Fuego erupting softly over Antigua Guatemala, golden sky, silhouettes of colonial buildings, warm amber tones, dreamy volcanic landscape, professional landscape photography, 4k",
        "topic": "Volcano views, dramatic scenery"
    },
    {
        "name": "antigua-cobblestone-street",
        "prompt": "soft golden afternoon light, charming cobblestone street in Antigua Guatemala, colorful colonial facades, hanging flower pots, warm inviting tones, dreamy peaceful atmosphere, professional street photography, 4k",
        "topic": "Street scenes, walking tours"
    },
    {
        "name": "antigua-courtyard-fountain",
        "prompt": "soft warm light, elegant colonial courtyard in Antigua Guatemala with stone fountain, terracotta pots, tropical plants, bougainvillea climbing walls, warm golden tones, dreamy peaceful atmosphere, professional real estate photography, 4k",
        "topic": "Courtyard homes, colonial interiors"
    },
    {
        "name": "antigua-volcano-panorama",
        "prompt": "soft morning light, breathtaking panoramic view of Antigua Guatemala valley with three volcanoes Agua Fuego Acatenango, colorful city below, warm golden tones, dreamy aerial perspective, professional landscape photography, 4k",
        "topic": "Panoramic views, valley properties"
    },
    {
        "name": "antigua-breakfast-terrace",
        "prompt": "soft golden morning light, outdoor breakfast terrace in Antigua Guatemala, coffee and tropical fruit, colonial backdrop, warm inviting tones, dreamy lifestyle atmosphere, professional food and lifestyle photography, 4k",
        "topic": "Lifestyle, food, expat living"
    },
    {
        "name": "antigua-hacienda-exterior",
        "prompt": "soft golden light, beautiful restored colonial hacienda in Antigua Guatemala, grand entrance with wooden doors, garden courtyard, warm terracotta and cream tones, dreamy estate atmosphere, professional real estate photography, 4k",
        "topic": "Colonial homes, haciendas, listings"
    },
    {
        "name": "antigua-textile-market",
        "prompt": "soft warm light, colorful traditional textile market in Antigua Guatemala, indigenous Maya weavings, vibrant colors, warm cultural tones, dreamy artistic atmosphere, professional cultural photography, 4k",
        "topic": "Culture, textiles, local markets"
    },
    {
        "name": "antigua-park-scene",
        "prompt": "soft golden afternoon light, Central Park Antigua Guatemala with fountain, people relaxing, cathedral in background, warm community tones, dreamy peaceful atmosphere, professional urban photography, 4k",
        "topic": "Parks, community, central Antigua"
    },
    {
        "name": "antigua-night-glow",
        "prompt": "soft warm evening light, Antigua Guatemala street at blue hour, glowing restaurant lights, colonial buildings, warm amber lanterns, dreamy romantic atmosphere, professional evening photography, 4k",
        "topic": "Nightlife, dining, evening atmosphere"
    }
]

NEGATIVE_PROMPT = "dark, harsh shadows, night, overcast, grey, desaturated, blurry, low quality, distorted"

def create_workflow(prompt_text):
    """Create a ComfyUI workflow for SDXL text-to-image."""
    return {
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "seed": int.from_bytes(os.urandom(4), 'big'),
                "steps": 20,
                "cfg": 7.5,
                "sampler_name": "dpmpp_2m",
                "scheduler": "karras",
                "denoise": 1.0,
                "model": ["4", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0]
            }
        },
        "4": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {
                "ckpt_name": "sd_xl_base_1.0.safetensors"
            }
        },
        "5": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "width": 1216,
                "height": 832,
                "batch_size": 1
            }
        },
        "6": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": prompt_text,
                "clip": ["4", 1]
            }
        },
        "7": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": NEGATIVE_PROMPT,
                "clip": ["4", 1]
            }
        },
        "8": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["3", 0],
                "vae": ["4", 2]
            }
        },
        "9": {
            "class_type": "SaveImage",
            "inputs": {
                "filename_prefix": "antigua-ai",
                "images": ["8", 0]
            }
        }
    }

def queue_prompt(workflow):
    """Submit a workflow to ComfyUI and return the prompt_id."""
    data = json.dumps({"prompt": workflow}).encode('utf-8')
    req = urllib.request.Request(
        f"{COMFYUI_URL}/prompt",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())["prompt_id"]

def check_queue():
    """Check if ComfyUI queue is empty."""
    try:
        resp = urllib.request.urlopen(f"{COMFYUI_URL}/queue")
        queue = json.loads(resp.read())
        return len(queue.get("queue_running", [])) + len(queue.get("queue_pending", []))
    except:
        return -1

def wait_for_image(prompt_id, timeout=300):
    """Wait for an image to be generated and return its filename."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            resp = urllib.request.urlopen(f"{COMFYUI_URL}/history/{prompt_id}")
            history = json.loads(resp.read())
            if prompt_id in history:
                outputs = history[prompt_id].get("outputs", {})
                for node_id, node_output in outputs.items():
                    if "images" in node_output:
                        for img in node_output["images"]:
                            return img.get("filename")
        except:
            pass
        time.sleep(2)
    return None

def download_image(filename, save_path):
    """Download a generated image from ComfyUI."""
    url = f"{COMFYUI_URL}/view?filename={filename}&type=output"
    urllib.request.urlretrieve(url, save_path)
    return save_path

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    results = []
    total = len(PROMPTS)
    
    print(f"Starting batch generation of {total} images...")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Estimated time: {total * 1.5:.0f}-{total * 2:.0f} minutes")
    print("=" * 60)
    
    for i, p in enumerate(PROMPTS, 1):
        name = p["name"]
        save_path = os.path.join(OUTPUT_DIR, f"{name}.png")
        
        # Skip if already exists
        if os.path.exists(save_path):
            print(f"[{i}/{total}] SKIP (exists): {name}")
            results.append({"name": name, "status": "skipped", "path": save_path})
            continue
        
        print(f"[{i}/{total}] Generating: {name}")
        print(f"  Topic: {p['topic']}")
        
        workflow = create_workflow(p["prompt"])
        
        try:
            prompt_id = queue_prompt(workflow)
            print(f"  Queued: {prompt_id[:8]}...")
            
            filename = wait_for_image(prompt_id, timeout=300)
            if filename:
                download_image(filename, save_path)
                print(f"  ✅ Saved: {save_path}")
                results.append({"name": name, "status": "success", "path": save_path})
            else:
                print(f"  ❌ Timeout waiting for image")
                results.append({"name": name, "status": "timeout", "path": None})
        except Exception as e:
            print(f"  ❌ Error: {e}")
            results.append({"name": name, "status": "error", "error": str(e), "path": None})
    
    print("\n" + "=" * 60)
    success = sum(1 for r in results if r["status"] == "success")
    skipped = sum(1 for r in results if r["status"] == "skipped")
    failed = sum(1 for r in results if r["status"] in ("timeout", "error"))
    print(f"DONE: {success} generated, {skipped} skipped, {failed} failed")
    
    # Save results
    results_path = os.path.join(OUTPUT_DIR, "batch-results.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to: {results_path}")

if __name__ == "__main__":
    main()
