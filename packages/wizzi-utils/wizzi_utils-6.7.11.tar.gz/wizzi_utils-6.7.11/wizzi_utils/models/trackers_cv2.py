# noinspection PyPackageRequirements
import cv2
from enum import Enum
import numpy as np
from wizzi_utils.misc import misc_tools as mt
from wizzi_utils.open_cv import open_cv_tools as cvt
from wizzi_utils.pyplot import pyplot_tools as pyplt


# noinspection PyUnresolvedReferences
class Trackes(Enum):
    # fps relate to scooter on this vid - not clear if running on cpu\gpu
    CSRT = cv2.legacy.TrackerCSRT_create  # 48.05 FPS
    KCF = cv2.legacy.TrackerKCF_create  # 170.63 FPS
    BOOSTING = cv2.legacy.TrackerBoosting_create  # 55 FPS
    MIL = cv2.legacy.TrackerMIL_create  # 14.79 FPS
    TLD = cv2.legacy.TrackerTLD_create  # 30 FPS
    MF = cv2.legacy.TrackerMedianFlow_create  # 800 FPS
    MOSSE = cv2.legacy.TrackerMOSSE_create  # 3000 FPS
    GOTURN = cv2.TrackerGOTURN_create  # error


class Cv2Tracker:
    def __init__(self, model_obj: Trackes):
        """
        :param model_obj: from class Trackes(Enum)
        """
        if model_obj not in Trackes:
            exit(-1)
        self.tracker_type = model_obj.name
        self.tracker_ctor = model_obj.value
        self.trackers = []
        return

    def to_string(self, tabs: int = 1) -> str:
        tabs_s = tabs * '\t'
        string = '{}{}'.format(tabs_s, mt.add_color(string='Cv2Tracker:', ops='underlined'))
        string += '\n\t{}tracker_type={}'.format(tabs_s, self.tracker_type)
        string += '\n\t{}supports multi objects tracking'.format(tabs_s)
        return string

    def add_obj_bbox_manual(self, cv_img: np.array, xywh: tuple, frame_idx: int, ack: bool = False):
        """
        :param cv_img:
        :param xywh:
        :param ack:
        :param frame_idx:
        :return:
        """
        if not xywh == (0, 0, 0, 0):  # clicked space\enter after selecting a bbox
            xywh = self.tuple_to_int(xywh)
            tracker = self.tracker_ctor()
            tracker.init(cv_img, xywh)
            tracker_dict = {
                'active': True,  # will be set to off when user decides no tracking needed (e.g. object left the frame)
                'type': self.tracker_type,
                'obj': tracker,
                'start_info': {
                    'post_frame': frame_idx,
                    'init_xywh': xywh,
                    'image_dims': cv_img.shape
                },
                'bboxes': {},  # will contain all bboxes of object found over iters
                'trails': []  # will contain all center of mass points - can create points trail of the object
            }
            self.trackers.append(tracker_dict)

            if ack:
                tl, br = self.convert_xywh_to_tl_and_br(xywh=xywh)
                msg = '\tpost frame {}: tracker {} created - tracking object on tl={}, br={} (xywh={})'
                print(msg.format(frame_idx, len(self.trackers), tl, br, xywh))
        return

    def add_obj_bbox_roi(self, cv_title: str, cv_img: np.array, frame_idx: int, ack: bool = False) -> None:
        """
        :param cv_title:
        :param cv_img:
        :param ack:
        :param frame_idx:
        :return:
        give an option to select a bbox and add to the trackers
        since we want to do it on the already open cv window, we pass title and we can't reshape the cv_img.
        the bbox that we will get from ROI will be in the cv_img dims. need to convert to self.in_dims
        """
        xywh = cv2.selectROI(cv_title, cv_img, fromCenter=False, showCrosshair=True)
        self.add_obj_bbox_manual(cv_img=cv_img, xywh=xywh, frame_idx=frame_idx, ack=ack)
        return

    def track_frame(
            self,
            cv_img: np.array,
            frame_idx: int,
            ack: bool = False,
            tabs: int = 1,
    ) -> list:
        detections = []

        if ack:
            print('{}Frame {} - image shape = {}:'.format(tabs * '\t', frame_idx, cv_img.shape))

        for idx, tracker_dict in enumerate(self.trackers):
            if tracker_dict['active']:
                (success, xywh) = tracker_dict['obj'].update(cv_img)
                if success:
                    xywh = self.tuple_to_int(xywh)
                    (x0, y0), (x1, y1) = self.convert_xywh_to_tl_and_br(xywh=xywh)
                    center_x = (x0 + x1) / 2
                    center_y = (y0 + y1) / 2
                    center = (center_x, center_y)
                    center = self.tuple_to_int(center)
                    tracker_dict['trails'].append(center)
                    if ack:
                        msg = '{}\tTrackerID={}: success. object on tl={}, br={} (center={}, xywh={})'
                        print(msg.format(tabs * '\t', idx, (x0, y0), (x1, y1), center, xywh))
                else:
                    x0, y0, x1, y1 = -1, -1, -1, -1
                    if ack:
                        print('{}\tTrackerID={}: object not found'.format(tabs * '\t', idx))
                    # TODO go over last 'x' detections - if all false - remove from active tracker

                detection_d = {
                    'tracker_idx': idx,
                    'success': success,
                    'bbox': {
                        #  pt1 = (x0, y0)  # obj frame top left corner
                        #  pt2 = (x1, y1)  # obj frame bottom right corner
                        'x0': x0,
                        'y0': y0,
                        'x1': x1,
                        'y1': y1,
                    },
                }

                detections.append(detection_d)
                tracker_dict['bboxes'][frame_idx] = detection_d  # save for future calculation. e.g. calculate direction
        return detections

    @staticmethod
    def convert_xywh_to_tl_and_br(xywh: tuple) -> (tuple, tuple):
        x0, y0, w, h = xywh
        x1, y1 = x0 + w, y0 + h
        return (x0, y0), (x1, y1)

    @staticmethod
    def convert_tl_and_br_to_xywh(tl: tuple, br: tuple) -> (tuple, tuple):
        x0, y0 = tl
        x1, y1 = br
        xywh = (x0, y0, x1 - x0, y1 - y0)
        return xywh

    @staticmethod
    def change_dims(xywh: tuple, old_dims: tuple, new_dims: tuple) -> tuple:
        # change scale to in_dims
        (x, y, w, h) = xywh
        new_w, new_h = new_dims
        old_w, old_h = old_dims
        x *= new_w / old_w
        w *= new_w / old_w
        y *= new_h / old_h
        h *= new_h / old_h
        return x, y, w, h

    @staticmethod
    def tuple_to_int(t: tuple) -> tuple:
        new_t = tuple([int(item) for item in t])
        return new_t

    def get_tracker_dict(self, tracker_id: int) -> dict:
        tr_dict = None
        if len(self.trackers) >= tracker_id + 1:
            tr_dict = self.trackers[tracker_id]
        return tr_dict

    def draw_detections(
            self,
            detections: list,
            cv_img: np.array,
            colors_d: dict = None,
            draw_trail: dict = 0,
            header_tl: dict = None,
            header_bl: dict = None,
            header_tr: dict = None,
            header_br: dict = None,
    ) -> None:
        """
        :param detections: output of self.classify_cv_img() on od models
        :param colors_d: colors in str form:
            bbox color
            label_bbox color
            text color
            if class_id_bbox exist - color the bbox of that class in the given color
            e.g. colors_d={
                    'bbox_c': 'black',
                },
        :param draw_trail: if to draw the "trail" of the object
            trail:= the center of the bbox from previous iterations
            if not None:
            e.g.
            draw_trail = {
                    'color': 'blue',
                    'len_trail': 100,
                    'radius': 1,
                    'thickness': -1
                }
        :param cv_img: the same that was given input to self.classify_cv_img()
        :param header_tl: dict with args for cvt.add_header on top_left corner
        :param header_bl: dict with args for cvt.add_header on bottom_left corner
        :param header_tr: dict with args for cvt.add_header on top_right corner
        :param header_br: dict with args for cvt.add_header on bottom_right corner
        header e.g.
        header_tl={'text': 'wizzi_utils', 'x_offset': 0, 'text_color': 'aqua', 'with_rect': True, 'bg_color': 'black',
               'bg_font_scale': 1}
        :return:
        """
        if colors_d is None:
            colors_d = {
                'bbox_c': 'lime'
            }
        for detection in detections:
            success = detection['success']
            if success:
                x0 = detection['bbox']['x0']
                y0 = detection['bbox']['y0']
                x1 = detection['bbox']['x1']
                y1 = detection['bbox']['y1']

                # DRAW BBOX
                color_bgr = pyplt.get_BGR_color(colors_d['bbox_c'])
                cv2.rectangle(img=cv_img, pt1=(x0, y0), pt2=(x1, y1), color=color_bgr, thickness=2)

                if draw_trail is not None:
                    color_bgr = pyplt.get_BGR_color(draw_trail['color'])
                    len_trail = draw_trail['len_trail']
                    r = draw_trail['radius']
                    th = draw_trail['thickness']

                    tracker_idx = detection['tracker_idx']

                    trails = self.get_tracker_dict(tracker_id=tracker_idx)['trails']
                    len_trail = min(len_trail, len(trails))  # cant take more than the existing trails
                    trails_to_draw = trails[-len_trail:]  # take last 'draw_trail' trails
                    for trail in trails_to_draw:
                        cv2.circle(cv_img, center=trail, radius=r, color=color_bgr, thickness=th)
        if header_tl is not None:
            h = header_tl
            cvt.add_header(cv_img, header=h['text'], loc=pyplt.Location.TOP_LEFT.value, x_offset=h['x_offset'],
                           text_color=h['text_color'], with_rect=h['with_rect'], bg_color=h['bg_color'],
                           bg_font_scale=h['bg_font_scale'])
        if header_bl is not None:
            h = header_bl
            cvt.add_header(cv_img, header=h['text'], loc=pyplt.Location.BOTTOM_LEFT.value, x_offset=h['x_offset'],
                           text_color=h['text_color'], with_rect=h['with_rect'], bg_color=h['bg_color'],
                           bg_font_scale=h['bg_font_scale'])
        if header_tr is not None:
            h = header_tr
            cvt.add_header(cv_img, header=h['text'], loc=pyplt.Location.TOP_RIGHT.value, x_offset=h['x_offset'],
                           text_color=h['text_color'], with_rect=h['with_rect'], bg_color=h['bg_color'],
                           bg_font_scale=h['bg_font_scale'])
        if header_br is not None:
            h = header_br
            cvt.add_header(cv_img, header=h['text'], loc=pyplt.Location.BOTTOM_RIGHT.value, x_offset=h['x_offset'],
                           text_color=h['text_color'], with_rect=h['with_rect'], bg_color=h['bg_color'],
                           bg_font_scale=h['bg_font_scale'])
        return
