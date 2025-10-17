from PIL import Image, ImageDraw, ImageFont
import os

def create_default_images():
    """Tạo 2 ảnh mặc định cho video"""
    
    # Kích thước ảnh 9:16
    width, height = 1080, 1920
    
    # Ảnh 1: Gradient xanh dương với text
    img1 = Image.new('RGB', (width, height), color='white')
    draw1 = ImageDraw.Draw(img1)
    
    # Tạo gradient từ xanh dương đến xanh lá
    for y in range(height):
        r = int(30 + (70 * y / height))
        g = int(144 + (100 * y / height)) 
        b = int(255 - (100 * y / height))
        color = (r, g, b)
        draw1.line([(0, y), (width, y)], fill=color)
    
    # Thêm text
    try:
        font = ImageFont.truetype('arial.ttf', 140)
    except:
        font = ImageFont.load_default()
    
    text1 = "#camontruongy \nSubscribe & Like"
    bbox = draw1.textbbox((0, 0), text1, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Outline
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            if dx != 0 or dy != 0:
                draw1.multiline_text((x+dx, y+dy), text1, font=font, fill='black', align='center')
    
    draw1.multiline_text((x, y), text1, font=font, fill='white', align='center')
    img1.save('default_images/default4.jpg', quality=95)
    
    # Ảnh 2: Gradient tím hồng với text
    img2 = Image.new('RGB', (width, height), color='white')
    draw2 = ImageDraw.Draw(img2)
    
    # Tạo gradient từ tím đến hồng
    for y in range(height):
        r = int(138 + (100 * y / height))
        g = int(43 + (150 * y / height))
        b = int(226 - (50 * y / height))
        color = (min(255, r), min(255, g), min(255, b))
        draw2.line([(0, y), (width, y)], fill=color)
    
    text2 = "#camontruongy \nSubscribe & Like"
    bbox = draw2.textbbox((0, 0), text2, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Outline
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            if dx != 0 or dy != 0:
                draw2.multiline_text((x+dx, y+dy), text2, font=font, fill='black', align='center')
    
    draw2.multiline_text((x, y), text2, font=font, fill='white', align='center')
    img2.save('default_images/default3.jpg', quality=95)
    
    
    print("✅ Đã tạo 4 ảnh mặc định:")
    print("- default_images/default3.jpg (Outro: Thanks for Watching)")
    print("- default_images/default4.jpg (Outro: Subscribe & Like)")

if __name__ == "__main__":
    create_default_images()