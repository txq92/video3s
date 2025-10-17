import os
import uuid
import random
from google import genai
from google.genai import types
from moviepy import (
    VideoFileClip, AudioFileClip, ImageClip, ColorClip, 
    CompositeVideoClip, concatenate_videoclips
)
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from typing import List
import textwrap
import wave

class VideoCreator:
    def __init__(self):
        self.width = 1080  # 9:16 aspect ratio
        self.height = 1920
        self.fps = 30
        
        # Cấu hình Google AI Gemini Client
        self.gemini_api_key = "AIzaSyAcLoIS03oTfbMmblWt0FiyEciszIFrFac"
        self.client = genai.Client(api_key=self.gemini_api_key)
        
        # Đường dẫn ảnh mặc định
        self.default_images = [
            "default_images/default1.jpg",
            "default_images/default2.jpg"
        ]
        
        # Đường dẫn ảnh outro
        self.outro_images = [
            "default_images/default3.jpg",  # Thanks for Watching
            "default_images/default4.jpg"   # Subscribe & Like
        ]
        
        # 30 giọng nói Gemini TTS có sẵn
        self.gemini_voices = {
            'Zephyr': 'Zephyr - Tươi sáng',
            'Puck': 'Puck - Rộn ràng', 
            'Charon': 'Charon - Cung cấp nhiều thông tin',
            'Kore': 'Kore - Firm',
            'Fenrir': 'Fenrir - Dễ kích động',
            'Leda': 'Leda - Trẻ trung',
            'Orus': 'Orus - Firm',
            'Aoede': 'Aoede - Breezy',
            'Callirrhoe': 'Callirrhoe - Dễ chịu',
            'Autonoe': 'Autonoe - Tươi sáng',
            'Enceladus': 'Enceladus - Breathy',
            'Iapetus': 'Iapetus - Rõ ràng',
            'Umbriel': 'Umbriel - Dễ tính',
            'Algieba': 'Algieba - Làm mịn',
            'Despina': 'Despina - Smooth',
            'Erinome': 'Erinome - Clear',
            'Algenib': 'Algenib - Khàn',
            'Rasalgethi': 'Rasalgethi - Cung cấp nhiều thông tin',
            'Laomedeia': 'Laomedeia - Rộn ràng',
            'Achernar': 'Achernar - Mềm',
            'Alnilam': 'Alnilam - Firm',
            'Schedar': 'Schedar - Even',
            'Gacrux': 'Gacrux - Người trưởng thành',
            'Pulcherrima': 'Pulcherrima - Lạc quan',
            'Achird': 'Achird - Thân thiện',
            'Zubenelgenubi': 'Zubenelgenubi - Bình thường',
            'Vindemiatrix': 'Vindemiatrix - Êm dịu',
            'Sadachbia': 'Sadachbia - Lively',
            'Sadaltager': 'Sadaltager - Hiểu biết',
            'Sulafat': 'Sulafat - Ấm'
        }
        
    def wave_file(self, filename: str, pcm: bytes, channels: int = 1, rate: int = 24000, sample_width: int = 2):
        """Tạo file WAV từ dữ liệu PCM"""
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(pcm)
    
    def text_to_speech(self, text: str, output_path: str, voice_name: str = 'Puck'):
        """Chuyển text thành âm thanh bằng Gemini TTS API"""
        try:
            # Gọi Gemini TTS API
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-preview-tts",
                contents=text,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=voice_name,
                            )
                        )
                    ),
                )
            )
            
            # Lấy dữ liệu âm thanh
            data = response.candidates[0].content.parts[0].inline_data.data
            
            # Lưu thành file WAV
            self.wave_file(output_path, data)
            
            print(f"✅ Gemini TTS thành công với giọng: {voice_name}")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi Gemini TTS: {str(e)}")
            raise Exception(f"Không thể tảo audio với Gemini TTS: {str(e)}")
    
    def create_text_image(self, text: str, width: int, height: int, font_size: int = 80):
        """Tạo hình ảnh với text để làm subtitle - font vừa và màu đỏ"""
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        try:
            # Thử tìm font hệ thống cho Windows
            import platform
            if platform.system() == 'Windows':
                try:
                    # Thử các font tiếng Việt phổ biến trên Windows
                    font = ImageFont.truetype('arial.ttf', font_size)
                except:
                    try:
                        font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', font_size)
                    except:
                        try:
                            font = ImageFont.truetype('C:/Windows/Fonts/calibri.ttf', font_size) 
                        except:
                            font = ImageFont.load_default()
            else:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Tính toán số ký tự tối đa mỗi dòng dựa trên chiều rộng và font size
        # Để lại margin 40px mỗi bên để tránh tràn
        available_width = width - 80  # 40px margin mỗi bên
        approx_char_width = font_size * 0.6  # Tỷ lệ xấp xỉ cho chữ tiếng Việt
        max_chars_per_line = int(available_width / approx_char_width)
        max_chars_per_line = max(15, min(max_chars_per_line, 25))  # Giới hạn 15-25 ký tự
        
        lines = textwrap.wrap(text, width=max_chars_per_line)
        
        # Tính vị trí để căn giữa text
        line_height = font_size + 10  # Khoảng cách giữa các dòng
        total_height = len(lines) * line_height
        start_y = (height - total_height) // 2
        
        for i, line in enumerate(lines):
            # Tính kích thước text
            try:
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
            except:
                # Fallback nếu textbbox không hoạt động
                text_width = len(line) * (font_size * 0.6)
            
            # Đảm bảo text nằm trong giới hạn an toàn (margin 40px)
            x = max(40, min((width - text_width) // 2, width - text_width - 40))
            y = start_y + i * line_height
            
            # Vẽ outline đen vừa phải
            outline_width = 3
            for dx in range(-outline_width, outline_width+1):
                for dy in range(-outline_width, outline_width+1):
                    if dx != 0 or dy != 0:  # Không vẽ ở tâm
                        draw.text((x+dx, y+dy), line, font=font, fill='black')
            
            # Vẽ text chính màu đỏ
            draw.text((x, y), line, font=font, fill='red')
        
        return img
    
    def resize_image_to_fit(self, image_path: str, target_width: int, target_height: int):
        """Resize hình ảnh để fit vào khung video 9:16"""
        img = Image.open(image_path)
        img = img.convert('RGB')
        
        # Tính tỷ lệ để fit vào khung
        img_ratio = img.width / img.height
        target_ratio = target_width / target_height
        
        if img_ratio > target_ratio:
            # Ảnh rộng hơn, cắt theo chiều rộng
            new_height = target_height
            new_width = int(new_height * img_ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Cắt phần thừa
            left = (new_width - target_width) // 2
            img = img.crop((left, 0, left + target_width, target_height))
        else:
            # Ảnh cao hơn, cắt theo chiều cao
            new_width = target_width
            new_height = int(new_width / img_ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Cắt phần thừa
            top = (new_height - target_height) // 2
            img = img.crop((0, top, target_width, top + target_height))
        
        return img
    
    def create_video(self, text: str, image_paths: List[str], output_filename: str, voice_name: str = 'Puck'):
        """Tạo video từ text và hình ảnh"""
        try:
            # Tạo file âm thanh
            audio_path = f"temp_audio_{uuid.uuid4().hex}.mp3"
            if not self.text_to_speech(text, audio_path, voice_name):
                return False, "Lỗi tạo âm thanh"
            
            # Load âm thanh để lấy thời lượng
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration
            
            # Tạo video clips từ hình ảnh
            video_clips = []
            
            # Nếu không có hình ảnh upload, sử dụng ảnh mặc định
            if not image_paths:
                image_paths = self.default_images.copy()
                print(f"🖼️ Sử dụng {len(image_paths)} ảnh mặc định")
            
            # Chia thời gian cho mỗi hình ảnh
            time_per_image = duration / len(image_paths)
            
            for i, image_path in enumerate(image_paths):
                try:
                    # Resize hình ảnh
                    resized_img = self.resize_image_to_fit(image_path, self.width, self.height)
                    
                    # Lưu hình ảnh tạm
                    temp_img_path = f"temp_img_{i}_{uuid.uuid4().hex}.jpg"
                    resized_img.save(temp_img_path)
                    
                    # Tạo clip từ hình ảnh
                    img_clip = ImageClip(temp_img_path, duration=time_per_image)
                    video_clips.append(img_clip)
                    
                    # Xóa file tạm
                    os.remove(temp_img_path)
                    
                except Exception as e:
                    print(f"Error processing image {image_path}: {e}")
                    # Nếu lỗi, sử dụng background đen
                    backup_clip = ColorClip(size=(self.width, self.height), color=(0, 0, 0), duration=time_per_image)
                    video_clips.append(backup_clip)
            
            # Thêm outro vào cuối video
            outro_duration = 3.0  # 3 giây
            outro_image = random.choice(self.outro_images)  # Chọn ngẫu nhiên
            print(f"🎬 Thêm outro: {outro_image.split('/')[-1]}")
            
            try:
                # Tạo clip outro
                outro_resized = self.resize_image_to_fit(outro_image, self.width, self.height)
                outro_temp_path = f"temp_outro_{uuid.uuid4().hex}.jpg"
                outro_resized.save(outro_temp_path)
                outro_clip = ImageClip(outro_temp_path, duration=outro_duration)
                video_clips.append(outro_clip)
                os.remove(outro_temp_path)
            except Exception as e:
                print(f"Lỗi tạo outro: {e}")
                # Fallback: outro đen
                outro_clip = ColorClip(size=(self.width, self.height), color=(0, 0, 0), duration=outro_duration)
                video_clips.append(outro_clip)
            
            # Ghép các clip lại (bao gồm outro)
            if video_clips:
                final_video = concatenate_videoclips(video_clips)
            else:
                # Fallback nếu tất cả ảnh đều lỗi
                final_video = ColorClip(size=(self.width, self.height), color=(0, 0, 0), duration=duration + outro_duration)
            
            # Tạo subtitle (chỉ hiển thị trong thời gian audio, không có trong outro)
            words = text.split()
            subtitle_clips = []
            words_per_second = len(words) / duration
            
            # Chia text thành các đoạn ngắn
            chunk_size = max(1, int(words_per_second * 2))  # 2 giây mỗi đoạn
            
            for i in range(0, len(words), chunk_size):
                chunk_words = words[i:i+chunk_size]
                chunk_text = " ".join(chunk_words)
                
                start_time = i / words_per_second
                end_time = min((i + chunk_size) / words_per_second, duration)
                
                # Chỉ hiển thị subtitle trong thời gian audio
                if start_time >= duration:
                    break
                    
                # Tạo hình ảnh text - vùng subtitle vừa đủ
                text_img = self.create_text_image(chunk_text, self.width, 200)
                text_img_path = f"temp_text_{i}_{uuid.uuid4().hex}.png"
                text_img.save(text_img_path)
                
                # Tạo clip subtitle với vị trí bottom và margin 20px
                txt_clip = ImageClip(text_img_path, duration=end_time-start_time).with_start(start_time).with_position(('center', self.height - 420))
                subtitle_clips.append(txt_clip)
                
                # Xóa file tạm
                os.remove(text_img_path)
            
            # Kết hợp video với subtitle
            if subtitle_clips:
                final_video = CompositeVideoClip([final_video] + subtitle_clips)
            
            # Thêm âm thanh (chỉ phát trong thời gian nội dung chính, outro không có âm thanh)
            # Âm thanh sẽ tự động dừng ở thời điểm kết thúc của audio_clip
            final_video = final_video.with_audio(audio_clip)
            
            # Xuất video
            output_path = f"outputs/{output_filename}"
            final_video.write_videofile(
                output_path, 
                fps=self.fps, 
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True
            )
            
            # Dọn dẹp
            audio_clip.close()
            final_video.close()
            os.remove(audio_path)
            
            return True, output_path
            
        except Exception as e:
            print(f"Error creating video: {e}")
            return False, str(e)