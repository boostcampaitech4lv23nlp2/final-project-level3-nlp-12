import io
import typing as T
import sys
sys.path.append('riffusion')
import numpy as np
import pydub
from PIL import Image
from riffusion.datatypes import InferenceInput, PromptInput
from riffusion.spectrogram_params import SpectrogramParams
from riffusion.streamlit import util as streamlit_util
class Riffusion_interpolation():
    def __init__(self, prompt_a, prompt_b, seed_image, num_inference_steps=50, num_interpolation_steps = 4):
        seed = 42
        denoising = 0.75
        guidance = 7.0
        self.seed_image = seed_image
        self.prompt_input_a = PromptInput(
            prompt=prompt_a,
            seed=seed,
            denoising=denoising,
            guidance=guidance,
        )
        seed = 42
        denoising = 0.75
        guidance = 7.0
        self.prompt_input_b = PromptInput(
            prompt=prompt_b,
            seed=seed,
            denoising=denoising,
            guidance=guidance,
        )
        self.num_interpolation_steps = num_interpolation_steps
        self.num_inference_steps = num_inference_steps

    def run(self, idx, code):
        alphas = list(np.linspace(0, 1, self.num_interpolation_steps))
        alphas_str = ", ".join([f"{alpha:.2f}" for alpha in alphas])
        device = 'cuda'
        init_image = Image.open(self.seed_image).convert("RGB")
        image_list: T.List[Image.Image] = []
        audio_bytes_list: T.List[io.BytesIO] = []
        for i, alpha in enumerate(alphas):
            inputs = InferenceInput(
                alpha=float(alpha),
                num_inference_steps=self.num_inference_steps,
                seed_image_id="og_beat",
                start=self.prompt_input_a,
                end=self.prompt_input_b,
            )
            image, audio_bytes = self.run_interpolation(
                inputs=inputs,
                init_image=init_image,
                device=device,
        )
            image_list.append(image)
            audio_bytes_list.append(audio_bytes)
        audio_segments = [pydub.AudioSegment.from_file(audio_bytes) for audio_bytes in audio_bytes_list]
        concat_segment = audio_segments[0]
        for segment in audio_segments[1:]:
            concat_segment = concat_segment.append(segment, crossfade=0)

        return concat_segment
        # audio_bytes = io.BytesIO()
        # concat_segment.export(audio_bytes, format="mp3")
        # audio_bytes.seek(0)
        # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # with open(os.path.join(BASE_DIR, f'audio_results/test_{code}_{idx}.wav'), mode='bx') as f:
        #         f.write(audio_bytes.getvalue())

    def run_interpolation(self, 
        inputs: InferenceInput, init_image: Image.Image, device: str = "cuda"
    ) -> T.Tuple[Image.Image, io.BytesIO]:
        """
        Cached function for riffusion interpolation.
        """
        pipeline = streamlit_util.load_riffusion_checkpoint(
            device=device,
        # No trace so we can have variable width
            no_traced_unet=True,
    )

        image = pipeline.riffuse(
            inputs,
        init_image=init_image,
        mask_image=None,
    )

    # TODO(hayk): Change the frequency range to [20, 20k] once the model is retrained
        params = SpectrogramParams(
            min_frequency=0,
            max_frequency=10000,
        )

    # Reconstruct from image to audio
        audio_bytes = streamlit_util.audio_bytes_from_spectrogram_image(
            image=image,
        params=params,
        device=device,
        output_format="mp3",
    )

        return image, audio_bytes

