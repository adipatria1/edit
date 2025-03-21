import cv2
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import os
import random
import math

class VideoProcessor:
    def __init__(self):
        pass
        
    def process_video(self, video_path, audio_path, resolution, interval_default, scene_duration, random_interval, random_scene):
        """
        Logika:
          - Audio sebagai patokan: durasi_audio = 81 detik (misalnya)
          - Jumlah klip = ceil(durasi_audio / scene_duration) 
          - Untuk klip ke-i, ambil scene dari film sumber pada window [i×interval_default, i×interval_default + interval_default].
            Jika random_scene aktif, titik mulai dipilih acak dalam window tersebut (agar scene tidak melewati batas window).
          - Untuk klip terakhir, durasi disesuaikan agar total durasi output = durasi_audio.
          - Klip-klip disambung secara berurutan sehingga output video berdurasi sama dengan audio (misal 81 detik).
        """
        try:
            video = VideoFileClip(video_path)
            audio = AudioFileClip(audio_path)
            original_fps = video.fps if video.fps else 30

            # Tentukan resolusi target
            if resolution == 720:
                target_resolution = (1280, 720)
            else:
                target_resolution = (854, 480)
            video_resized = video.resize(target_resolution)
            
            audio_duration = audio.duration  # misalnya 81 detik
            n_clips = math.ceil(audio_duration / scene_duration)  # jumlah klip yang akan diambil
            
            clips = []
            for i in range(n_clips):
                window_start = i * interval_default
                window_end = window_start + interval_default
                # Pastikan window tidak melebihi durasi film sumber
                if window_start >= video.duration:
                    break
                
                # Tentukan titik mulai scene dalam window
                if random_scene:
                    max_possible_start = window_start + (interval_default - scene_duration)
                    # Pastikan tidak melebihi batas film sumber
                    if max_possible_start > video.duration - scene_duration:
                        max_possible_start = video.duration - scene_duration
                    if max_possible_start < window_start:
                        scene_start = window_start
                    else:
                        scene_start = random.randint(int(window_start), int(max_possible_start))
                else:
                    scene_start = window_start
                
                # Untuk klip terakhir, sesuaikan durasinya agar total output = audio_duration
                if i == n_clips - 1:
                    clip_duration = audio_duration - scene_duration * (n_clips - 1)
                else:
                    clip_duration = scene_duration
                
                scene_end = scene_start + clip_duration
                # Jika scene_end melebihi durasi video sumber, potong agar tidak error
                if scene_end > video.duration:
                    scene_end = video.duration
                    clip_duration = scene_end - scene_start
                # Ambil subclip dan tambahkan ke daftar klip
                clip = video_resized.subclip(scene_start, scene_end)
                clips.append(clip)
                
                # (Opsional) Anda bisa memberikan progress update di sini jika diinginkan
            
            if clips:
                final_video = concatenate_videoclips(clips)
                output_path = os.path.splitext(video_path)[0] + "_recap.mp4"
                final_video.write_videofile(
                    output_path,
                    fps=original_fps,
                    codec='libx264',
                    audio=False,
                    threads=4,
                    preset='medium'
                )
                final_video.close()
            
            video.close()
            audio.close()
            
        except Exception as e:
            try:
                video.close()
                audio.close()
            except:
                pass
            raise e
