### Questions

1. Should `wandb` be even included? (No. It's not free.)
2. Making training data for all the other features (i.e. LE and vertices)?
3. No need to merge the regular U-Net package anymore.
4. Weird prev_image augmentation bug
5. Weird tif bug
6. How generalizable is our method if an iteration needs to be cherry picked from Siam-UNet cosh?
7. self.imgs_shape[0] == 1 in predict.py. To implement or not to implement.
8. `n_filter=32`
9. ActNN for training? But with 32 filters the graphics memory use is pretty managable (< 8GB, around 6.1GB). Currently, inference takes less than 3GB of graphics memory and regular memory. It works perfectly on my laptop.

## Pretrained models

Can be found at [https://dataservice.duke.edu/#/project/284bbd3b-5cd4-46f6-bf67-9aee93ad54d6]. Should be made public at release of this package to the public.