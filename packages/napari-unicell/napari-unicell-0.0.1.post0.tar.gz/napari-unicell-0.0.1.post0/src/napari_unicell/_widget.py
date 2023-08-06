"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

from magicgui import magic_factory, magicgui
from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget
from napari.utils.notifications import show_info
if TYPE_CHECKING:
    import napari
from typing import List  
import os
join = os.path.join
import time
import numpy as np
from enum import Enum
import torch
import monai
from monai.transforms import Compose, EnsureType, Activations, AsDiscrete
from .models.unicell_modules import UniCell
from .utils.multi_task_sliding_window_inference import multi_task_sliding_window_inference
from .utils.postprocess import watershed_post
import time
from skimage import io, segmentation, morphology, measure, exposure, transform
import pathlib

class DownSampleRate(Enum):
    No_DS = 'No_DS'
    DS2 = 'DS2'
    DS4 = 'DS4'
    DS8 = 'DS'

class ModelName(Enum):
    UniCell = 'unicell'
    UniNuclei = 'uninuclei'

def load_model(model_name, custom_model_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


    # elif model_name == 'swin_unet':
    #     model = monai.networks.nets.SwinUNETR(
    #                     img_size=(256, 256), 
    #                     in_channels=3, 
    #                     out_channels=3,
    #                     feature_size=24, # should be divisible by 12
    #                     spatial_dims=2
    #                 )
    #     if os.path.isfile(custom_model_path):
    #         checkpoint = torch.load(custom_model_path.resolve(), map_location=torch.device(device))
    #     elif os.path.isfile(join(os.path.dirname(__file__), 'work_dir/swinunetr/best_Dice_model.pth')):
    #         checkpoint = torch.load(join(os.path.dirname(__file__), 'work_dir/swinunetr/best_dice_model.pth'), map_location=torch.device(device))
    #     else:
    #         torch.hub.download_url_to_file('https://zenodo.org/record/6792177/files/best_Dice_model.pth?download=1', join(os.path.dirname(__file__), 'work_dir/swinunetr/best_Dice_model.pth'))
    #         checkpoint = torch.load(join(os.path.dirname(__file__), 'work_dir/swinunetr/best_Dice_model.pth'), map_location=torch.device(device))

    if model_name == 'unicell':
        model = UniCell(in_channels=3, out_channels=3, regress_class=1, img_size=256).to(device)
        if os.path.isfile(custom_model_path):
            checkpoint = torch.load(custom_model_path.resolve(), map_location=torch.device(device))
        elif os.path.isfile(join(os.path.dirname(__file__), 'work_dir/unicell/model.pth')):
            checkpoint = torch.load(join(os.path.dirname(__file__), 'work_dir/unicell/model.pth'), map_location=torch.device(device))
        else:
            os.makedirs(join(os.path.dirname(__file__), 'work_dir/unicell'), exist_ok=True)
            torch.hub.download_url_to_file('https://zenodo.org/record/7308987/files/model.pth?download=1', join(os.path.dirname(__file__), 'work_dir/unicell/model.pth'))
            checkpoint = torch.load(join(os.path.dirname(__file__), 'work_dir/unicell/model.pth'), map_location=torch.device(device))

    elif model_name == 'uninuclei':
        model = UniCell(in_channels=3, out_channels=3, regress_class=1, img_size=256).to(device)
        if os.path.isfile(custom_model_path):
            checkpoint = torch.load(custom_model_path.resolve(), map_location=torch.device(device))
        elif os.path.isfile(join(os.path.dirname(__file__), 'work_dir/uninuclei/model.pth')):
            checkpoint = torch.load(join(os.path.dirname(__file__), 'work_dir/uninuclei/model.pth'), map_location=torch.device(device))
        else:
            os.makedirs(join(os.path.dirname(__file__), 'work_dir/uninuclei'), exist_ok=True)
            torch.hub.download_url_to_file('https://zenodo.org/record/7308990/files/model.pth?download=1', join(os.path.dirname(__file__), 'work_dir/unicell/model.pth'))
            checkpoint = torch.load(join(os.path.dirname(__file__), 'work_dir/uninuclei/model.pth'), map_location=torch.device(device))

    model.load_state_dict(checkpoint['model_state_dict'])

    model = model.to(device)
    model.eval()

    return model

class ExampleQWidget(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        btn = QPushButton("Click me!")
        btn.clicked.connect(self._on_click)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(btn)

    def _on_click(self):
        print("napari has", len(self.viewer.layers), "layers")



def normalize_channel(img, lower=0.1, upper=99.9):
    non_zero_vals = img[np.nonzero(img)]
    percentiles = np.percentile(non_zero_vals, [lower, upper])
    if percentiles[1] - percentiles[0] > 0.001:
        img_norm = exposure.rescale_intensity(img, in_range=(percentiles[0], percentiles[1]), out_range='uint8')
    else:
        img_norm = img
    return img_norm

def preprocess(img_data):
    if len(img_data.shape) == 2:
        img_data = np.repeat(np.expand_dims(img_data, axis=-1), 3, axis=-1)
    elif len(img_data.shape) == 3 and img_data.shape[-1] > 3:
        img_data = img_data[:,:, :3]
    else:
        pass
    pre_img_data = np.zeros(img_data.shape, dtype=np.uint8)
    for i in range(3):
        img_channel_i = img_data[:,:,i]
        if len(img_channel_i[np.nonzero(img_channel_i)])>0:
            pre_img_data[:,:,i] = normalize_channel(img_channel_i, lower=0.1, upper=99.9)
    return pre_img_data


def unicell_seg(pre_img_data, model_name, custom_model_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = load_model(model_name, custom_model_path)
    # post_pred = Compose([EnsureType(), Activations(softmax=False), AsDiscrete(threshold=threshold)])
    #%%
    roi_size = (256, 256)
    sw_batch_size = 8
    with torch.no_grad():
        t0 = time.time()
        test_npy01 = pre_img_data/np.max(pre_img_data)
        test_tensor = torch.from_numpy(np.expand_dims(test_npy01, 0)).permute(0,3,1,2).type(torch.FloatTensor).to(device)
        # include softmax; output: interior: [B, 3, H, W], dist: [B, 1, H, W]
        pred_interior, pred_dist = multi_task_sliding_window_inference(test_tensor, roi_size, sw_batch_size, predictor=model) 
        pred_dist_npy = pred_dist.squeeze(1).cpu().numpy() # (B, H, W)
        pred_interior_npy = pred_interior.cpu().numpy()[:,1] # 1-interior (B, H, W)
        seg_inst = watershed_post(pred_dist_npy, pred_interior_npy)   
        if np.max(seg_inst)<60000:
            test_pred_mask = seg_inst.squeeze().astype(np.int16)
        else:
            test_pred_mask = seg_inst.squeeze().astype(np.int64)
        # # post processing
        # for i in range(1, np.max(test_pred_mask)):
        #     cell_inst_i = morphology.remove_small_holes(test_pred_mask==i)
            
        #     if np.sum(cell_inst_i)<16:
        #         test_pred_mask[cell_inst_i] = 0
    
        test_pred_mask, _,_ = segmentation.relabel_sequential(test_pred_mask)   
        t1 = time.time()
        bw_mask = np.uint8(test_pred_mask>0.2)
        print(f'Prediction finished; img size = {pre_img_data.shape}; costing: {t1-t0:.2f}s')
    show_info(f'Prediction finished; img size = {pre_img_data.shape}; costing: {t1-t0:.2f}s')
    return test_pred_mask, bw_mask

# @magicgui(call_button='run segmentation', layout='vertical',
#             model_name=dict(widget_type='ComboBox', label='select model', choices=['unicell', 'uninuclei'], value='unicell'),
#             custom_model_path=dict(widget_type='FileEdit', label='custom model path', value=''),
#             downsample_rate = dict(widget_type='SpinBox', label='downsample rate', value=1, min=1, max=8, step=2),
#             binary_mask = dict(widget_type='CheckBox', text='binary mask', value=False, tooltip='output binary mask')
# )

@magic_factory
def unicell_widget(image_layer: "napari.layers.Image", model_name: ModelName, custom_model_path: pathlib.Path, downsample_rate: DownSampleRate) -> List["napari.types.LayerDataTuple"]:
    print(f"you have selected {image_layer}")
    img_data = image_layer.data
    img_dim = len(img_data.shape)
    if downsample_rate.value == 'DS2':
        if img_dim > 2:
            img_data_ds = img_data[::2, ::2, :]
        else:
            img_data_ds = img_data[::2, ::2]
    elif downsample_rate.value == 'DS4':
        if img_dim > 2:
            img_data_ds = img_data[::4, ::4, :]
        else:
            img_data_ds = img_data[::4, ::4]
    elif downsample_rate.value == 'DS8':
        if img_dim > 2:
            img_data_ds = img_data[::8, ::8, :]
        else:
            img_data_ds = img_data[::8, ::8]
    else:
        img_data_ds = img_data

    inst_seg, bw_seg = unicell_seg(preprocess(img_data_ds), model_name.value, custom_model_path)

    if downsample_rate.value != 'No_DS':
        final_seg = transform.resize(inst_seg, (img_data.shape[0], img_data.shape[1]), order=0, preserve_range=True, anti_aliasing=False).astype(inst_seg.dtype)
        # final_bw = transform.resize(bw_seg, (img_data.shape[0], img_data.shape[1]), order=0, preserve_range=True, anti_aliasing=False).astype(bw_seg.dtype)
    else:
        final_seg = inst_seg
        # final_bw = bw_seg

    seg_layer = (final_seg, {"name": f"{image_layer.name}_inst"}, "labels")
    # bw_layer = (final_bw, {"name": f"{image_layer.name}_bw"}, "labels")
    return seg_layer

# Uses the `autogenerate: true` flag in the plugin manifest
# to indicate it should be wrapped as a magicgui to autogenerate
# a widget.
# def example_function_widget(image_layer: "napari.layers.Image"):
#     print(f"you have selected {image_layer}")

