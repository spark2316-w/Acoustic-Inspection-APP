from pydub import AudioSegment
import numpy as np
import os
import pandas as pd
from scipy.signal import correlate
import matplotlib.pyplot as plt

# แปลงไฟล์ .m4a เป็น numpy array พร้อม normalize
def audio_to_normalized_numpy(audio_file):
    audio = AudioSegment.from_file(audio_file, format="m4a")
    audio = audio.set_channels(1)
    samples = np.array(audio.get_array_of_samples()).astype(np.float32)
    samples -= np.mean(samples)
    samples /= np.std(samples) + 1e-9  # ป้องกันหารศูนย์
    return samples

# เปรียบเทียบไฟล์เสียงในโฟลเดอร์กับไฟล์ reference
def compare_audio_folder(reference_path, folder_path, output_excel_path):
    ref_signal = audio_to_normalized_numpy(reference_path)
    results = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".m4a") and os.path.join(folder_path, filename) != reference_path:
            test_path = os.path.join(folder_path, filename)
            try:
                test_signal = audio_to_normalized_numpy(test_path)

                # --- พล็อตสัญญาณก่อนทำ cross-correlation ---
                plt.figure(figsize=(14, 8))
                plt.subplot(2, 1, 1)
                plt.plot(ref_signal, color='b')
                plt.title("Reference Signal")
                plt.xlabel("Sample Index")
                plt.ylabel("Amplitude")
                plt.xlim(0, len(ref_signal))

                plt.subplot(2, 1, 2)
                plt.plot(test_signal, color='r')
                plt.title(f"Test Signal: {filename}")
                plt.xlabel("Sample Index")
                plt.ylabel("Amplitude")
                plt.xlim(0, len(test_signal))
                plt.tight_layout()
                plt.show()

                # --- คำนวณ cross-correlation ---
                cross_corr = correlate(ref_signal, test_signal, mode='full', method='auto')
                max_corr = np.max(cross_corr) / len(ref_signal)
                lags = np.arange(-(len(test_signal) - 1), len(ref_signal))

                # --- พล็อตกราฟ cross-correlation ---
                plt.figure(figsize=(14, 6))
                plt.plot(lags, cross_corr)
                plt.title(f"Cross-Correlation with {filename}")
                plt.xlabel("Lag")
                plt.ylabel("Correlation")
                plt.grid(True)
                plt.tight_layout()
                plt.show()

                # --- ระดับความคล้ายคลึง ---
                if max_corr > 0.3:
                    similarity = "Very Similar"
                elif max_corr > 0.2:
                    similarity = "Moderately Similar"
                else:
                    similarity = "Not Similar"

                results.append({
                    "Filename": filename,
                    "Normalized Max Correlation": round(max_corr, 5),
                    "Similarity": similarity
                })

                print(f"{filename} -> Max Corr: {max_corr:.5f} => {similarity}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

    # บันทึกลง Excel
    df = pd.DataFrame(results)
    df.to_excel(output_excel_path, index=False)
    print(f"\nResults saved to: {output_excel_path}")

# ตัวอย่างการเรียกใช้
reference_file = r"C:\Users\User\Desktop\Project\TestGG\Recording (109).m4a"
test_folder = r"C:\Users\User\Desktop\Project\TestGG"
output_excel = os.path.join(test_folder, "comparison_results_normalized.xlsx")

compare_audio_folder(reference_file, test_folder, output_excel)
