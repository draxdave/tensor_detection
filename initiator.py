#! /usr/bin/python

from models.research import object_detection
from res import xml_to_csv
from res import generate_tfrecord
from res import generate_label_map
import glob
import re
import m_util
import time
import threading

basePath = "/home/siamak/PycharmProjects/tensor3/"
m_util.init_logger(basePath)


def start_training():
    # training ...
    object_detection.run(basePath + 'res/training', basePath + 'res/training/faster_rcnn_inception_v2_pets.config')


def run():
    m_util.log(m_util.EVENT.TRAINING_STARTED)

    # # label map
    labelMapList = generate_label_map.main(basePath)
    m_util.log(m_util.EVENT.TRAINING_STEP_LABEL_MAP)

    # xml to csv -> Done
    xml_to_csv.main(basePath)
    m_util.log(m_util.EVENT.TRAINING_STEP_XML)

    # tfrecords
    generate_tfrecord.run(basePath + 'res/images/train_labels.csv', basePath + 'res/images/train',
                          basePath + 'res/train.record', labelMapList)
    generate_tfrecord.run(basePath + 'res/images/test_labels.csv', basePath + 'res/images/test',
                          basePath + 'res/test.record', labelMapList)
    m_util.log(m_util.EVENT.TRAINING_STEP_TFR)

    threading.Thread(target=start_training, daemon=True).start()

    time.sleep(len(labelMapList) * (60 * 60) * 0.5)
    # time.sleep(180)
    'Wait until the training process generates some files'

    m_util.log(m_util.EVENT.TRAINING_STEP_TRAIN)

    dir_list = [f for f in glob.glob(basePath + "res/training/*.meta")]
    latest = 0
    inference_path = basePath + 'res/inference_graph'
    for item in dir_list:
        portions = item.split("/")
        current_ver = int(re.findall(r'\d+', portions[len(portions) - 1])[0])
        if latest < current_ver:
            latest = current_ver

    m_util.clear_dir(inference_path)
    object_detection.infer_run("image_tensor", basePath + "res/training/faster_rcnn_inception_v2_pets.config",
                               inference_path, basePath + "res/training/model.ckpt-" + str(latest))
    m_util.log(m_util.EVENT.TRAINING_STEP_INFERENCE)
    m_util.log(m_util.EVENT.TRAINING_FINISHED)


if __name__ == '__main__':
    run()
