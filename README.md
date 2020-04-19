# A Simple Web App for Image Recognition

A web app on GAE showing what I have learned from[ fast.ai course v3](https://course.fast.ai/index.html).

The following were used for model **training** (see requirements.txt):
- Python 3.6
- fastai

The following were used for model **deployment**:    
- Google App Engine
- Flask

Examples:
- Classifier([Oxford-IIIT Pet](http://www.robots.ox.ac.uk/~vgg/data/pets)):    
Recognize 37 categories of pets using ResNet50 with 4% error-rate. Can't do Multi-label.  
[Notebook1](notebooks/Classifier/pets.ipynb)  
[Notebook2](notebooks/Classifier/pets-more.ipynb)

- Segmentation([Camvid](http://mi.eng.cam.ac.uk/research/projects/VideoRec/CamVid/)):   
Segmentation for Camvid video using U-net+ResNet34 with 8% error-rate. But perfromance was not good when I used my own photos. Still have a lot to learn.   
[Notebook](notebooks/Segmentation/Camvid.ipynb)

- To be added: Classification & Localization using newer models



## Thanks
I referred to
>Pattaniyil, Nidhin and Shaikh, Reshama, [Deploying Deep Learning Models On Web And Mobile](https://reshamas.github.io/deploying-deep-learning-models-on-web-and-mobile/), 2019

to code my `main.py`.
