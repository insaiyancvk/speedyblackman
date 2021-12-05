# An AI that plays NFS Rivals

> Note: "speedyblackman" is [YT/Blackpanthaa](https://www.youtube.com/c/Blackpanthaa)'s IGN. _Nothing racist._

Here's the plan (Oct 13 2021):

- Three different models on three different datasets. 
    1. Acceleration, break, reverse frames
    2. Left, right turn frames

- Work on left/right dataset first, then acceleration/break dataset.
- Implement _speedyblackman_.

Vague TODO:
- Create dataloader for the dataset working with and save the copy to drive.
- Test the dataset on different models.

## Training completed (Nov 30 2021).
- Trained the turns data on ResNet18, VGG-19_bn, InceptionV3, MobileNetV2 and AlexNet.
    - AlexNet gave the best results when implemented.
    - Although the train, test accuracies were high, all the models seemed to overfit over a few epochs except AlexNet.
- Trained the acceleration data on ResNet18, MobileNetV2 and AlexNet.
    - MobileNetV2 gave the best results when implemented.
    - Almost all the models overfit. So the model that least overfit was chosen for the implementation.
- _The data was not sufficient_
    - 10GB (~52k frames) of turns data was used (which gave pretty good results).
    - 1.35GB (~6.8k frames) of acceleration data was used (which was definitely not sufficient and hence every model overfit).

## Wanna play around with it?

1. Get NFS Rivals - you know what to do

2. Clone this repository and change directory into it

    ```
    git clone https://github.com/insaiyancvk/speedyblackman
    cd speedyblackman
    ```

3. Download the weights from [drive](https://drive.google.com/drive/folders/1UVlAe1nAIbpiU_UYJjTBB_ijhvIx5XCA?usp=sharing) and save them in _speedyblackman_ folder

4. Install the dependencies

    `pip install torch torchvision numpy keyboard opencv-python`

5. Start the game and run the code

    `python speedyblackman.py`

## Enough of my rant, look the result for yourself

Check it on [youtube](https://www.youtube.com/watch?v=9AfSzsOr-H8)
and few other clips in [drive](https://drive.google.com/drive/folders/1LGExSxldYSsDBhlyzmlp0RxWw7yP5g11?usp=sharing)
