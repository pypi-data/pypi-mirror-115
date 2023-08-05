import numpy as np
import tensorflow as tf
from PIL import Image
from skimage.filters import gaussian
from skimage.transform import resize
from tqdm import tqdm

from uberlimb.frame import LimbFrame
from uberlimb.input_space import InputSpace
from uberlimb.model.model import LimbModel
from uberlimb.parameters import RendererParams, FrameColorMap
from uberlimb.video.video_recorder import VideoRecorder

# Allow parallel run of multiple Uberlimb processes
physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)


class Renderer:
    def __init__(self,
                 params: RendererParams,
                 mask: np.ndarray = None):
        self.params = params
        self.num_model_outputs = (
            3
            if params.post_fx.color_map == FrameColorMap.BINNING
            else 1
        )
        self.model = LimbModel.build_model(self.params.model, self.num_model_outputs)
        self._mask = mask
        self.input_space = InputSpace(self.params.input,
                                      self._mask)

    def load_mask_from_raster_image(self,
                                    mask_img: Image):
        # TODO: handle AA
        mask_img = (mask_img
                    .convert('L')
                    .resize((self.input_space.arr_x_resolution,
                             self.input_space.arr_y_resolution)))
        mask_arr = np.array(mask_img, dtype=np.float32)
        mask_arr = gaussian(mask_arr, sigma=7)
        mask_noise = 1 + np.random.random(mask_arr.shape) * 0.02
        mask_arr *= mask_noise
        self._mask = mask_arr
        self.update_input_space()

    def update_model(self):
        self.num_model_outputs = (
            3
            if self.params.post_fx.color_map == FrameColorMap.BINNING
            else 1
        )
        self.model = LimbModel.build_model(self.params.model, self.num_model_outputs)

    def update_input_space(self):
        self.input_space = InputSpace(self.params.input,
                                      self._mask)

    def render_frame(self) -> LimbFrame:
        # TODO set batch size based on params count
        arr = self.model.predict(self.input_space.arr,
                                 batch_size=int(2 ** 17),
                                 verbose=0)
        arr = arr.reshape(self.input_space.arr_y_resolution,
                          self.input_space.arr_x_resolution,
                          self.num_model_outputs)
        frame = LimbFrame(arr)
        del arr
        frame.apply_post_fx(self.params.post_fx)
        if frame.arr.shape[:2] != (self.params.input.y_resolution, self.params.input.x_resolution,):
            frame.arr = resize(frame.arr,
                               (self.params.input.y_resolution,
                                self.params.input.x_resolution,),
                               order=3,
                               anti_aliasing=True, preserve_range=True)
        frame.arr = frame.arr.astype(np.uint8)
        return frame

    def render_video(self,
                     recorder: VideoRecorder):
        with recorder:
            with tqdm(total=3600) as pbar:
                for input_space in self.input_space.get_animation_generator():
                    self.input_space.arr = input_space
                    frame_arr = self.render_frame().as_array()
                    recorder.write_frame(frame_arr)
                    pbar.update()
        return recorder.params.filepath
