import torch
import torch.nn.functional as F
import numpy as np
import os, argparse
import cv2
from PraNet_Res2Net import PraNet
from data import test_dataset
import time


parser = argparse.ArgumentParser()
parser.add_argument('--testsize', type=int, default=352, help='testing size')
parser.add_argument('--gpu_id', type=str, default='0', help='select gpu id')
parser.add_argument('--snapshot', type=str,
                    default='./Net_epoch_best.pth')
parser.add_argument('--test_path', type=str, default='./data/ValDataset/', help='test dataset path')
opt = parser.parse_args()

dataset_path = opt.test_path

# set device for test
if opt.gpu_id == '0':
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    print('USE GPU 0')
elif opt.gpu_id == '1':
    os.environ["CUDA_VISIBLE_DEVICES"] = "1"
    print('USE GPU 1')

# load the model
model = PraNet(channel=32).cuda()
model.load_state_dict(torch.load(opt.snapshot))
model.cuda()
model.eval()

# test
save_path = './mask/'
dataset_path = './medico2020/'

if not os.path.exists(save_path):
    os.makedirs(save_path)

time_taken = []
test_loader = test_dataset(dataset_path, dataset_path, opt.testsize)
for i in range(test_loader.size):
    image, gt, name, image_for_post = test_loader.load_data()
    gt = np.asarray(gt, np.float32)
    gt /= (gt.max() + 1e-8)

    image = image.cuda()
    # Start time
    start_time = time.time()
    # Prediction
    res = model(image)
    # End timer
    end_time = time.time() - start_time

    time_taken.append(end_time)
    print("{} - {:.10f}".format(name, end_time))

    res = F.upsample(res[3], size=gt.shape, mode='bilinear', align_corners=False)
    res = res.sigmoid().data.cpu().numpy().squeeze()
    res = res > 0.5
    res = res.astype(np.float32)
    res = (res - res.min()) / (res.max() - res.min() + 1e-8)
    # print('Save Img To: ', save_path + name)
    cv2.imwrite(save_path + name, res * 255)

mean_time_taken = np.mean(time_taken)
mean_fps = 1/mean_time_taken
print("Mean FPS: ", mean_fps)
print('Test Done!')
