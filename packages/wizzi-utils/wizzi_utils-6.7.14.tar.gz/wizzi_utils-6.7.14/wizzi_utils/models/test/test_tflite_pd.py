from wizzi_utils.misc import misc_tools as mt
from wizzi_utils.misc.test import test_misc_tools as mtt
from wizzi_utils.open_cv import open_cv_tools as cvt
from wizzi_utils.open_cv.test import test_open_cv_tools as cvtt
from wizzi_utils.pyplot import pyplot_tools as pyplt
import numpy as np
import os
# noinspection PyPackageRequirements
import cv2
from wizzi_utils.models.models_configs import MODELS_CONFIG
from wizzi_utils.models.models_configs import ModelType
from wizzi_utils.models.tflite_models import pose_detection as pd

CAM_FRAMES = 300
IMAGE_MS = 5000
VID_X_FRAMES_CV = 80

WITH_TF = True
WITH_SUB_IMG = True
WITH_LABELS = True
DEBUG_DETECTIONS = False
# DEBUG_DETECTIONS = True  # TODO comment out

PD_OP = 1
PD_IM_TEST = True
PD_CAM_TEST = False
PD_VID_TEST = False


def __get_pd_dict(op: int = 1):
    if op == 1:
        pd_solo = {
            'model_names': ['pose_landmark_lite'],
            # 'model_names': ['pose_landmark_full'],
            # 'model_names': ['pose_landmark_heavy'],
            # 'model_names': ['posenet'],
            # 'model_names': ['openpose_pose_mpi'],
            # 'model_names': ['openpose_pose_coco'],
            # 'model_names': ['openpose_pose_coco_multi'],
            # 'model_names': ['body25'],
            # 'model_names': ['hand_pose'],
            'dis_size': (640, 480),
            'grid': (1, 1),
        }
        pd_meta_dict = pd_solo
    elif op == 2:
        pd_dual = {
            'model_names': [
                'pose_landmark_full',
                # 'posenet'
                # 'openpose_pose_coco'
                'openpose_pose_coco_multi'
            ],
            'dis_size': (640 * 2, 480),
            'grid': (1, 2),
        }
        pd_meta_dict = pd_dual
    elif op == 3:
        all_models_names = pd.PdBaseModel.get_pose_detection_models(ack=False)
        # remove hand pose - not the same work
        all_models_names.remove('hand_pose')
        pd_all_models = {
            'model_names': all_models_names,
            'dis_size': 'fs',
            'grid': (2, 4),
        }
        pd_meta_dict = pd_all_models
    else:
        pd_meta_dict = None
    return pd_meta_dict


def _get_models(model_names: list) -> list:
    models = []
    for model_name in model_names:
        model_cfg = MODELS_CONFIG[model_name]
        m_save_dir = '{}/{}/{}'.format(mtt.MODELS, MODELS_CONFIG[model_name]['job'], model_name)
        if model_cfg['model_type'] == ModelType.PdTflNormal.value:
            model = pd.TflPdModel(
                save_load_dir=m_save_dir,
                model_name=model_name,
                # allowed_joint_names=['nose', 'leftEyeInside', 'leftEye']
            )
        elif model_cfg['model_type'] == ModelType.PdTflPoseNet.value:
            model = pd.TflPdModelPoseNet(
                save_load_dir=m_save_dir,
                model_name=model_name,
            )
        else:
            model = None
            mt.exception_error('model type not found')
            exit(-1)
        print(model.to_string(tabs=1))
        models.append(model)
    return models


def pd_run(
        model: (pd.TflPdModel, pd.TflPdModelPoseNet),
        cv_img: np.array,
        fps: mt.FPS
):
    fps.start()
    detections = model.detect_cv_img(cv_img, ack=DEBUG_DETECTIONS)
    fps.update(ack_progress=True, tabs=1, with_title=True)

    if WITH_SUB_IMG:
        detections = model.add_sub_sub_image_to_detection(
            detections,
            cv_img=cv_img,
            bbox_image_p={
                'x_left_start': 0.2,
                'x_left_end': 0.8,
                'y_top_start': 0,
                'y_top_end': 0.5,
            },
            ack=DEBUG_DETECTIONS
        )
    model.draw_detections(
        detections,
        colors_d={
            'bbox_c': 'blue',
            'sub_image_c': 'black',
            'text_c': 'black',
        },
        cv_img=cv_img,
        draw_joints=True,
        draw_labels=WITH_LABELS,
        draw_edges=True,
        draw_bbox=WITH_SUB_IMG,
        draw_sub_image=WITH_SUB_IMG,
        header_tl={'text': 'wizzi_utils', 'x_offset': 0, 'text_color': 'aqua', 'with_rect': True, 'bg_color': 'black',
                   'bg_font_scale': 1},
        header_bl={'text': '{}-{}'.format(model.model_name, model.device), 'x_offset': 0, 'text_color': 'white',
                   'with_rect': True, 'bg_color': 'black', 'bg_font_scale': 1},
        header_tr={'text': '{:.2f} FPS'.format(fps.get_fps()), 'x_offset': 190, 'text_color': 'r', 'with_rect': False,
                   'bg_color': None, 'bg_font_scale': 1},
        header_br={'text': mt.get_time_stamp(format_s='%Y_%m_%d'), 'x_offset': 200, 'text_color': 'aqua',
                   'with_rect': True, 'bg_color': 'black', 'bg_font_scale': 1},
    )

    return


def od_or_pd_Model_image_test(
        cv_img: np.array,
        model_names: list,
        ms: int = cvtt.BLOCK_MS_NORMAL,
        dis_size: tuple = (640, 480),
        grid: tuple = (1, 1),
):
    mt.get_function_name(ack=True, tabs=0)
    cv_imgs_post = []
    models = _get_models(model_names)

    for model in models:
        cv_img_clone = cv_img.copy()
        fps = mt.FPS(summary_title='{}'.format(model.model_name))
        pd_run(model, cv_img_clone, fps=fps)
        cv_imgs_post.append(cv_img_clone)
    cvt.display_open_cv_images(
        cv_imgs_post,
        ms=ms,
        title='{}'.format(cv_img.shape),
        loc=pyplt.Location.CENTER_CENTER.value,
        grid=grid,
        resize=dis_size,
        header=None,
        save_path=None
    )
    cv2.destroyAllWindows()
    return


def _od_or_pd_Model_cam_test(
        cam: (cv2.VideoCapture, cvt.CameraWu),
        model_names: list,
        max_frames: int = CAM_FRAMES,
        work_every_x_frames: int = 1,
        dis_size: tuple = (640, 480),
        grid: tuple = (1, 1),
):
    if isinstance(cam, cv2.VideoCapture):
        img_w, img_h = cvt.get_dims_from_cap(cam)
    else:
        img_w, img_h = cvt.get_dims_from_cap(cam.cam)
    print('\tFrame dims {}x{}'.format(img_w, img_h))

    if len(model_names) == 1:
        mp4_out_dir = '{}/{}/{}'.format(mtt.VIDEOS_OUTPUTS, mt.get_function_name(), model_names[0])
        if not os.path.exists(mp4_out_dir):
            mt.create_dir(mp4_out_dir)
        out_fp = '{}/{}_detected.mp4'.format(mp4_out_dir, 'cam')
        out_dims = (img_w, img_h)
        mp4 = cvt.Mp4_creator(
            out_full_path=out_fp,
            out_fps=20.0,
            out_dims=out_dims
        )
        print(mp4)
    else:
        mp4 = None

    models = _get_models(model_names)

    fps_list = [mt.FPS(summary_title='{}'.format(model.model_name)) for model in models]
    for i in range(max_frames):
        if isinstance(cam, cv2.VideoCapture):
            success, cv_img = cam.read()
        else:
            success, cv_img = cam.read_img()
        if i % work_every_x_frames != 0:  # s
            # do only x frames
            continue
        cv_imgs_post = []
        if success:
            for model, fps in zip(models, fps_list):
                cv_img_clone = cv_img.copy()
                pd_run(model, cv_img_clone, fps=fps)
                cv_imgs_post.append(cv_img_clone)
                if i == 0:  # first iter take much longer - measure from second iter
                    fps.clear()
            if mp4 is not None:
                mp4.add_frame(cv_imgs_post[0])
        else:
            mt.exception_error(e='failed to grab frame {}'.format(i))
            continue
        k = cvt.display_open_cv_images(
            cv_imgs_post,
            ms=1,
            title='cam 0',
            loc=pyplt.Location.CENTER_CENTER.value,
            grid=grid,
            resize=dis_size,
            header='{}/{}'.format(i + 1, max_frames),
            save_path=None
        )
        if k == ord('q'):
            mt.exception_error('q was clicked. breaking loop')
            break
    for fps in fps_list:
        fps.finalize()
    if mp4 is not None:
        mp4.finalize()
    cv2.destroyAllWindows()
    return


def od_or_pd_Model_cam_test(
        model_names: list = None,
        max_frames: int = CAM_FRAMES,
        dis_size: tuple = (640, 480),
        grid: tuple = (1, 1),
):
    mt.get_function_name(ack=True, tabs=0)
    cam = cvt.CameraWu.open_camera(port=0, type_cam='cv2')

    if cam is not None:
        _od_or_pd_Model_cam_test(
            cam=cam,
            model_names=model_names,
            max_frames=max_frames,
            work_every_x_frames=1,
            dis_size=dis_size,
            grid=grid,
        )
    return


def od_or_pd_Model_video_test(
        model_names: list,
        vid_path: str,
        work_every_x_frames: int = 1,
        dis_size: tuple = (640, 480),
        grid: tuple = (1, 1),
):
    mt.get_function_name(ack=True, tabs=0)
    cam = cv2.VideoCapture(vid_path)
    if cam is not None:
        _od_or_pd_Model_cam_test(
            cam=cam,
            model_names=model_names,
            max_frames=cvt.get_frames_from_cap(cam),
            work_every_x_frames=work_every_x_frames,
            dis_size=dis_size,
            grid=grid,
        )
    return


def test_all():
    print('{}{}:'.format('-' * 5, mt.get_base_file_and_function_name()))
    pd_meta_dict = __get_pd_dict(op=PD_OP)

    # POSE DETECTION TESTS
    if PD_IM_TEST:
        # cv_img = cvtt.load_img_from_web(mtt.FACES, ack=False)
        # cv_img = cvtt.load_img_from_web(mtt.HAND, ack=False)  # if testing 'hand_pose', use HAND image
        cv_img = cvtt.load_img_from_web(mtt.F_MODEL, ack=False)
        # cv_img = cvt.load_img(path='{}/Input2/77.jpg'.format(mtt.IMAGES_PATH))
        # cv_img = cvt.load_img(path='{}/Input2/cam1_0.jpg'.format(mtt.IMAGES_PATH))
        # cv_img = cvt.load_img(path='{}/Input2/90.jpg'.format(mtt.IMAGES_PATH))

        od_or_pd_Model_image_test(
            cv_img=cv_img,
            model_names=pd_meta_dict['model_names'],
            ms=IMAGE_MS,
            dis_size=pd_meta_dict['dis_size'],
            grid=pd_meta_dict['grid'],
        )
    if PD_CAM_TEST:
        od_or_pd_Model_cam_test(
            model_names=pd_meta_dict['model_names'],
            max_frames=CAM_FRAMES,
            dis_size=pd_meta_dict['dis_size'],
            grid=pd_meta_dict['grid'],
        )
    if PD_VID_TEST:
        vid_path = cvtt.get_vid_from_web(name=mtt.WOMAN_YOGA)
        od_or_pd_Model_video_test(
            model_names=pd_meta_dict['model_names'],
            vid_path=vid_path,
            work_every_x_frames=VID_X_FRAMES_CV,
            dis_size=pd_meta_dict['dis_size'],
            grid=pd_meta_dict['grid'],
        )
    print('{}'.format('-' * 20))
    return
