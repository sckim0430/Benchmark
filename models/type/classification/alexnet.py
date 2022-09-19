"""The AlexNet class implementation.
"""
import torch.nn as nn
from base_classification import BaseClassification


class AlexNet(BaseClassification):
    """AlexNet Architecture                                                                   

    Args:
        backbone (nn.Module) : alexnet backbone model class
        cls_head (nn.Module) : alexnet classification head model class
        init_weight (bool) : option for weight initialization
    """

    def __init__(self, backbone, cls_head=None):
        """The initalization.

        Args:
            backbone (torch.nn.Module): The feature extractor.
            cls_head (torch.nn.Module, optional): The classification head. Defaults to None.
        """
        super.__init__(backbone, cls_head)

    def _forward_train(self, imgs, labels, **kwargs):
        """The train method.

        Args:
            imgs (torch.Tensor): The input images.
            labels (torch.Tensor): The input labels.

        Returns:
            dict: The loss function value.
        """
        assert self.with_cls_head, "Alexnet should have classification head."

        losses = dict()

        features = self.backbone(imgs)
        cls_scores = self.cls_head(features)
        loss_cls = self.cls_head.loss(cls_scores, labels, **kwargs)
        losses.update(loss_cls)

        return losses

    def _forward_test(self, imgs):
        """The test method.

        Args:
            imgs (torch.Tensor): The input images.

        Returns:
            torch.Tensor: The output of the model.
        """
        features = self.backbone(imgs)

        if self.with_cls_head:
            cls_scores = self.cls_head(features)
            return cls_scores

        return features
