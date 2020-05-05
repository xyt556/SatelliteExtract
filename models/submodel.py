import torchvision.models as models
import numpy as np
import torch
import matplotlib.pyplot as plt

class SubModel(torch.nn.Module):
    def __init__(self,selected_layer):
        super(SubModel,self).__init__()
        self.selected_layer=selected_layer
        self.pretrained_model = models.mobilenet_v2(pretrained=True).features
        self.criterion = torch.nn.L1Loss(reduction='mean')
        for params in self.pretrained_model.parameters():
            params.requires_grad = False
    
    def forward(self,pred,gt,vis=True):
        pred = self.get_features(pred)
        gt = self.get_features(gt)
        if vis:
            self.plot(pred,gt)
        loss = self.criterion(pred,gt)
        return loss

    def get_features(self,x):
        for index,layer in enumerate(self.pretrained_model):
            x = layer(x)
            if (index == self.selected_layer):
                return x
    
    def plot(self,pred,gt):
        print(pred.shape)
        pred = pred.mean(axis=1).data.numpy()
        pred = 1.0/(1+np.exp(-1*pred))
        pred = np.round(pred*255)
        gt = gt.mean(axis=1).data.numpy()
        gt = 1.0/(1+np.exp(-1*gt))
        gt = np.round(gt*255)
        for i in range(pred.shape[0]):
            img = np.concatenate([pred[i],gt[i]],axis=1)
            plt.imshow(img)
            plt.show()

if __name__ == "__main__":
    np.random.seed(0)
    torch.manual_seed(0)
    torch.cuda.manual_seed_all(0)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    batchsize = 4
    classnum = 1
    H = 128
    pred = torch.rand(batchsize,classnum,H,H)
    gt = torch.ones(batchsize,H,H)

    pred = torch.sigmoid(pred).squeeze(dim=1)
    
    pred = torch.stack([pred,pred,pred],dim=1)
    print(pred.shape)

    gt = torch.stack([gt,gt,gt],dim=1)
    print(gt.shape)

    model = SubModel(3)

    loss = model(pred,gt)
    print(loss)


