import os
import glob


class Label:
    name = ""
    id = 0

    def __init__(self, mid, name):
        self.id = mid
        self.name = name


labelMapList = []
basePath = ""


def generate_node(label):
    return """\n item {
  id: %d
  name: '%s'
}\n""" % (label.id, label.name)


def create_label_map():
    resources_path = basePath.replace('tensor3', 'ODPyWS') + "/res/images"
    iteration = 0

    with open(basePath + "res/training/labelmap.pbtxt", 'w') as label_map_file:
        for dir_name in os.listdir(resources_path):
            iteration += 1
            label = Label(iteration, dir_name)
            labelMapList.append(label)
            label_map_file.write(generate_node(label))

        label_map_file.close()
    print('Successfully created the Label Map')
    return iteration


def create_config_file(iteration_count):
    with open(basePath + 'res/samples/SAMPLE_faster_rcnn_inception_v2_pets.config', 'r') as sample_rcnn:
        content = sample_rcnn.read()
        content = content.replace("%num_classes%", str(iteration_count))
        content = content.replace("%fine_tune_checkpoint%",
                                  basePath + "res/faster_rcnn_inception_v2_coco_2018_01_28/model.ckpt")
        content = content.replace("%train_input_path%", basePath + "res/train.record")
        content = content.replace("%train_input_map%", basePath + "res/training/labelmap.pbtxt")
        content = content.replace("%num_examples%", str(len(glob.glob(basePath + "res/images/test/*.jpg"))))
        content = content.replace("%eval_input_path%", basePath + "res/train.record")
        content = content.replace("%eval_input_map%", basePath + "res/training/labelmap.pbtxt")
        sample_rcnn.close()

    with open(basePath + 'res/training/faster_rcnn_inception_v2_pets.config', 'w') as rcnn:
        rcnn.write(content)
        rcnn.close()

    print('Successfully created the Config file')


def main(base_path):
    global basePath
    basePath=base_path

    iteration = create_label_map()
    create_config_file(iteration)
    return labelMapList
