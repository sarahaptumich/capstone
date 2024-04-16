import json
from pathlib import Path

import numpy as np
import pandas as pd
from torch.utils.data.dataset import Dataset
from tqdm import tqdm


def get_frame_number_from_id(video_id, frame_id, img_ext='.png'):
    n = frame_id.replace(f'{video_id}/', '').replace('img-', '').replace(img_ext, '')

    try:
        return int(n)
    except ValueError:
        raise ValueError(f'Invalid frame id: {frame_id}')


def get_box_from_keypoints(keypoints, box_border=100):
    box_x1, box_y1 = keypoints[:, :2].min(axis=0)
    box_x2, box_y2 = keypoints[:, :2].max(axis=0)
    box_x1 -= box_border
    box_y1 -= box_border
    box_x2 += box_border
    box_y2 += box_border
    w = box_x2 - box_x1
    h = box_y2 - box_y1
    assert w > 0 and h > 0, f'Invalid box: {box_x1}, {box_x2}, {box_y1}, {box_y2}'
    box = (box_x1, box_y1, w, h, 1)  # confidence score 1
    return box


def normalise_keypoints(box, keypoints):
    x, y, w, h, _ = box
    xk = (keypoints[:, 0] - x) / w
    yk = (keypoints[:, 1] - y) / h
    nk = np.stack((xk, yk), axis=1)  # no need to stack the scores
    return nk

def load_clip(pose_path, img_ext='.png', broken_policy='skip_frame', policy_warning=False):
    with open(pose_path) as f:
        d = json.load(f)

    frame_ids = sorted(d.keys())
    video_id = frame_ids[0].split('/')[0]
    frame_numbers = [get_frame_number_from_id(video_id, f_id, img_ext=img_ext) for f_id in frame_ids]
    clip = []

    for i, (frame_id, frame_number) in enumerate(zip(frame_ids, frame_numbers)):
        keypoints = np.array(d[frame_id]['keypoints'])

        try:
            box = get_box_from_keypoints(keypoints, box_border=0)
            norm_kpt = normalise_keypoints(box, keypoints)
        except AssertionError as e:
            if broken_policy == 'skip_frame':

                if policy_warning:
                    print(f'Got broken keypoints at frame {frame_id}. Skipping as per broken policy')
                continue
            else:
                raise e

        clip.append(norm_kpt)

    clip = np.stack(clip, axis=0)
    clip_id = pose_path.stem

    return clip, clip_id, video_id


def BraceDataset(df, pose_jsons):
    clips = []
    clip_labels = []

    for video_id in df.video_id.unique():
        video_paths = [p for p in pose_jsons if p.stem.startswith(video_id)]
        clip_paths_by_video = {}

        for vp in video_paths:
            label = re.search(r'([^/]+)\.json\.json', str(vp)).group(1).split('_')[-1]
            name = re.search(r'([^/]+)_[a-z]+\.json\.json', str(vp)).group(1)
            name = re.sub(r'[_-]', '.', name)
            splits = vp.stem.replace(f'{video_id}_', '').split('_')
            clip_start, clip_end = (int(x) for x in splits[0].split('-'))
            clip_paths_by_video[name] = vp
            clip_labels.append(label)
        
        for uid, uid_path in clip_paths_by_video.items():
            clip, _, _ = load_clip(uid_path, img_ext='.png', broken_policy='skip_frame', policy_warning=False)
            clips.append(clip)

    return clips, clip_labels


