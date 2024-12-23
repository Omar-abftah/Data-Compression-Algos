import numpy as np
from PIL import Image

def read_image(path):
    img = Image.open(path).convert('L')
    return np.array(img)

def write_image(pixels, path):
    img = Image.fromarray(pixels.astype(np.uint8), 'L')
    img.save(path)

def pad_image(pixels, block_size):
    height, width = pixels.shape
    new_height = (height + block_size - 1) // block_size * block_size
    new_width = (width + block_size - 1) // block_size * block_size
    padded = np.zeros((new_height, new_width), dtype=np.uint8)
    padded[:height, :width] = pixels
    return padded, height, width

def split_blocks(pixels, block_size):
    height, width = pixels.shape
    rows = height // block_size
    cols = width // block_size
    blocks = pixels.reshape(rows, block_size, cols, block_size)
    blocks = blocks.transpose(0, 2, 1, 3).reshape(-1, block_size**2)
    return blocks

def train_codebook(blocks, codebook_size, max_iterations=5):
    if codebook_size > len(blocks):
        return blocks
    
    indices = np.random.choice(len(blocks), codebook_size, replace=False)
    codebook = blocks[indices].astype(np.float32)
    
    blocks = blocks.astype(np.float32)
    block_norms = np.sum(blocks**2, axis=1, keepdims=True)
    
    for _ in range(max_iterations):
        dots = np.dot(blocks, codebook.T)
        code_norms = np.sum(codebook**2, axis=1)
        distances = block_norms - 2 * dots + code_norms
        
        assignments = np.argmin(distances, axis=1)
        
        new_codebook = np.zeros_like(codebook)
        for i in range(codebook_size):
            mask = assignments == i
            if np.any(mask):
                new_codebook[i] = np.mean(blocks[mask], axis=0)
            else:
                new_codebook[i] = codebook[i]
        
        if np.allclose(new_codebook, codebook):
            break
            
        codebook = new_codebook
    
    return codebook.astype(np.uint8)

def compress(input_path, output_path, block_size, codebook_size):
    pixels = read_image(input_path)
    padded_pixels, original_height, original_width = pad_image(pixels, block_size)
    blocks = split_blocks(padded_pixels, block_size)
    
    codebook = train_codebook(blocks, codebook_size)
    
    blocks_float = blocks.astype(np.float32)
    codebook_float = codebook.astype(np.float32)
    
    block_norms = np.sum(blocks_float**2, axis=1, keepdims=True)
    code_norms = np.sum(codebook_float**2, axis=1)
    dots = np.dot(blocks_float, codebook_float.T)
    distances = block_norms - 2 * dots + code_norms
    indices = np.argmin(distances, axis=1).astype(np.uint8)
    
    with open(output_path, 'wb') as f:
        f.write(block_size.to_bytes(4, 'big'))
        f.write(len(codebook).to_bytes(4, 'big'))
        f.write(original_width.to_bytes(4, 'big'))
        f.write(original_height.to_bytes(4, 'big'))
        codebook.tofile(f)
        indices.tofile(f)

def decompress(input_path, output_path):
    with open(input_path, 'rb') as f:
        block_size = int.from_bytes(f.read(4), 'big')
        codebook_size = int.from_bytes(f.read(4), 'big')
        original_width = int.from_bytes(f.read(4), 'big')
        original_height = int.from_bytes(f.read(4), 'big')
        
        padded_width = (original_width + block_size - 1) // block_size * block_size
        padded_height = (original_height + block_size - 1) // block_size * block_size
        
        codebook = np.fromfile(f, dtype=np.uint8, count=codebook_size * block_size * block_size)
        codebook = codebook.reshape(codebook_size, block_size * block_size)
        
        num_blocks = (padded_height // block_size) * (padded_width // block_size)
        indices = np.fromfile(f, dtype=np.uint8, count=num_blocks)
    
    blocks = codebook[indices]
    blocks = blocks.reshape(-1, block_size, block_size)
    
    rows = padded_height // block_size
    cols = padded_width // block_size
    
    padded_pixels = blocks.reshape(rows, cols, block_size, block_size)
    padded_pixels = padded_pixels.transpose(0, 2, 1, 3).reshape(padded_height, padded_width)
    cropped_pixels = padded_pixels[:original_height, :original_width]
    
    write_image(cropped_pixels, output_path)

if __name__ == "__main__":
    block_size = 4
    codebook_size = 128
    compress('input.png', 'compressed.bin', block_size, codebook_size)
    decompress('compressed.bin', 'output.png')