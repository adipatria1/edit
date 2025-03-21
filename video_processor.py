import cv2
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, ColorClip, ImageClip, concatenate_videoclips
import os
import math
import random

class VideoProcessor:
    def __init__(self):
        pass
        
    def process_video(self, video_path, audio_path, resolution, scene_duration, random_scene, 
                      pause_probability=0.3, pause_min=1, pause_max=3):
        """
        Pendekatan:
          • Kita ingin mengambil n_clips secara berurutan dari film sumber sehingga 
            seluruh film (misalnya 1 jam 30 menit) terwakili secara merata.
          • Jumlah klip n_clips dihitung berdasarkan audio_duration yang diinginkan.
            Misalnya, jika audio berdurasi 30 menit (1800 detik) dan scene_duration = 5 detik,
            maka n_clips = 1800/5 = 360.
          • Mapping film: film_interval = (film_duration - scene_duration) / (n_clips - 1)
            sehingga klip ke-i diambil dari film mulai pada film_clip_start = i * film_interval.
          • Jika random_scene aktif, kita tidak menambahkan offset acak (agar tetap berurutan).
            (Anda dapat mengubahnya jika diinginkan, tetapi di sini kita pilih pengambilan berurutan.)
          • Setelah setiap klip, dengan probabilitas tertentu (misalnya 30%), disisipkan pause clip,
            berupa freeze frame (menggunakan frame terakhir dari scene) dengan durasi acak antara pause_min dan pause_max.
          • Klip-klipek tersebut dikonkatenasi secara berurutan sehingga output mengikuti narasi film.
          • Perlu diingat: Final output durasinya akan menjadi 
                total_scene_time + total_pause_time,
            jadi mungkin akan lebih panjang dari audio_duration awal.
        """
        try:
            # Buka video dan audio
            video = VideoFileClip(video_path)
            audio = AudioFileClip(audio_path)
            original_fps = video.fps if video.fps else 30

            # Tentukan target resolusi
            if resolution == 720:
                target_resolution = (1280, 720)
            else:
                target_resolution = (854, 480)
            video_resized = video.resize(target_resolution)
            
            # Kita gunakan audio.duration sebagai patokan jumlah scene yang diinginkan.
            desired_audio_duration = audio.duration  # misalnya 1800 detik (30 menit)
            n_clips = math.ceil(desired_audio_duration / scene_duration)
            if n_clips < 1:
                n_clips = 1
            
            film_duration = video.duration  # misalnya 5400 detik (1 jam 30 menit)
            # Hitung interval pengambilan di film agar mencakup seluruh film secara berurutan
            if n_clips > 1:
                film_interval = (film_duration - scene_duration) / (n_clips - 1)
            else:
                film_interval = 0

            clips = []
            current_output_time = 0  # timeline output (akan bertambah seiring penambahan scene & pause)
            
            for i in range(n_clips):
                # Pengambilan secara berurutan dari film
                film_clip_start = i * film_interval
                # Pastikan tidak melebihi durasi film
                if film_clip_start + scene_duration > film_duration:
                    film_clip_start = film_duration - scene_duration
                film_clip_end = film_clip_start + scene_duration
                
                # Ambil subclip dari film (secara berurutan, tanpa offset acak)
                scene_clip = video_resized.subclip(film_clip_start, film_clip_end).set_start(current_output_time)
                clips.append(scene_clip)
                current_output_time += scene_duration  # scene ditempatkan secara berurutan
                
                # Sisipkan pause clip dengan probabilitas tertentu
                if random.random() < pause_probability:
                    # Ambil frame terakhir dari scene sebagai freeze frame
                    freeze_frame = video_resized.get_frame(film_clip_end - 0.1)
                    pause_duration = random.uniform(pause_min, pause_max)
                    pause_clip = ImageClip(freeze_frame).set_duration(pause_duration).set_start(current_output_time)
                    pause_clip = pause_clip.set_fps(original_fps)
                    clips.append(pause_clip)
                    current_output_time += pause_duration
            
            # Final output duration sesuai dengan timeline yang telah dibangun
            final_output_duration = current_output_time
            
            # Buat base clip (latar hitam) sepanjang final_output_duration
            base = ColorClip(size=target_resolution, color=(0, 0, 0), duration=final_output_duration).set_fps(original_fps)
            
            # Buat composite video
            composite = CompositeVideoClip([base] + clips, size=target_resolution)
            composite.duration = final_output_duration
            
            output_path = os.path.splitext(video_path)[0] + "_recap_pause.mp4"
            composite.write_videofile(
                output_path,
                fps=original_fps,
                codec='libx264',
                audio=False,
                threads=4,
                preset='medium'
            )
            
            composite.close()
            video.close()
            audio.close()
            
        except Exception as e:
            try:
                video.close()
                audio.close()
            except:
                pass
            raise e
