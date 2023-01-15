# espnet-asr
*espnet-asr* is an End-to-end Automatic Speech Recognition (ASR) system using [ESPnet](https://github.com/espnet/espnet).

## Installation 
(1) make virtual environment
- venv
  
    ```conda create -n (venv) python=3```

    ```conda activate (venv)```

(2) install packages (with cuda=11.0)

- install pytorch

    ```conda install pytorch==1.7.1 torchvision==0.8.2 torchaudio==0.7.2 cudatoolkit=11.0 -c pytorch```

- install pyworld

    ```conda install pyworld -c conda-forge```

- install libsndfile

    ```pip install libsndfile1```

- install sox, youtube-dl, ffmpeg

    ```sudo apt-get install sox```

    ```conda install -c conda-forge youtube-dl```

    ```conda install -c conda-forge ffmpeg```

- install ESPnet

    ```pip install espnet```

- install ESPnet model zoo

    ```pip install espnet_model_zoo```

- downloading pre-trained models 
  
   ```tools/download_mdl.sh```