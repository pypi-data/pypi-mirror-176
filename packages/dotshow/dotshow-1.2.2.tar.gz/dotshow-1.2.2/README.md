# dotshow
    We generate image to text on terminal
    It is made for linux server to show image.
    When we want to see image on python  linux server, 
    we have to save image or use jupyter notebook.
    To overcome those problem, I made this package.

    To see thumnail of the image, we can use cv2.imshow in local environment.
    However, it is impossible for server ssh terminal.
    It is simple thumnail printer using python.
    

# Example
    We can print images like down below.
<img width="300" align = "left" alt="before" src="https://user-images.githubusercontent.com/50725139/140743113-9db67704-0a93-4f58-9542-a893b915a543.png">
<img width="300" alt="after" src="https://user-images.githubusercontent.com/50725139/140743199-64cac4d2-08be-4b23-9f21-393b2577bc51.png">
<img width="300" align = "left"  alt="before" src="https://user-images.githubusercontent.com/50725139/140743399-5daf658c-085e-44f5-8e65-d9821f53512d.png">
<img width="300" alt="after" src="https://user-images.githubusercontent.com/50725139/140743425-35af69bf-3aca-4105-9c3b-4540b846ad7f.png">


# How to use
### Git cloning on your repository
    pip install dotshow
    
## import package on python
### load our own package
    from dotshow import loadshow
    dotshow(<img-path>)

### cv2 version
```python
    import cv2
    from dotshow import dotshow
    img = cv2.imread(<img-path>)
    dotshow(img) # run the code
````

### PIL Image version
    import numpy as np
    from PIL import Image
    from dotshow import dotshow
    img = np.array(Image.open(<img-path>))
    dotshow(img) # run the code
    
# Parameters
    loadshow(
        gray = True[default / bool]
        size = 7 [default / 0 ~ 10]
    )
    dotshow(
        gray = True[default]
        size = 7 [default / 0 ~ 10]
    )
    
    gray - if your image is not interpretable, give gray parater False
    size - if your image is too big in your terminal, reduce size using this parameter
    
    when you use low size parameter, image will undersampled too much 
    and it will decrease image quality.
