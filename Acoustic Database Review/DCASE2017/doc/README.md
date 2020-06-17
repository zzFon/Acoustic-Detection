Title:  TUT Rare Sound events 2017, Development dataset

TUT Rare Sound events 2017, Development dataset
===============================================
[Audio Research Group / Tampere University of Technology](http://arg.cs.tut.fi/)

Authors
- Aleksandr Diment (<aleksandr.diment@tut.fi>, <http://www.cs.tut.fi/~diment/>)
- Toni Heittola (<toni.heittola@tut.fi>, <http://www.cs.tut.fi/~heittolt/>)
- Annamaria Mesaros (<annamaria.mesaros@tut.fi>, <http://www.cs.tut.fi/~mesaros/>)
- Tuomas Virtanen (<tuomas.virtanen@tut.fi>, <http://www.cs.tut.fi/~tuomasv/>)

Background data recording and annotation
- Eemi Fagerlund
- Aku Hiltunen

Event data annotation, mixture synthesizer software:
- Aleksandr Diment


# Table of Contents
1. [Dataset](#1-dataset)
2. [Usage](#2-usage)
3. [License](#3-license)
4. [References](#4-references)

1. Dataset
=================================
TUT Rare Sound events 2017, development dataset consists of source files for creating mixtures of rare sound events with background audio, as well a set of readily generated mixtures and recipes for generating them.

The "source" part of the dataset consists of two subsets:

- background recordings from 15 different acoustic scenes,
- recordings with the target rare sound events from three classes, accompanied by annotations of their temporal occurrences,
- a set of meta files providing the cross-validation setup: lists of background and target event recordings split into training and test subsets (called "devtrain" and "devtest", respectively, indicating they are provided as the development dataset, as opposed to the evaluation dataset released later). 

The mixture set consists of two subsets (training and testing), each containing 1500 mixtures (500 per target class in each subset, with half of the mixtures not containing any target class events). 


### Background recordings

The background recordings are from 15 different acoustic scenes and are an almost exact copy of TUT Acoustic scenes 2016, development dataset (see <https://zenodo.org/record/45739>), with the exception of recordings naturally containing target class events and interference from mobile phone, which were removed. When using the original version of the dataset, refer to the provided bg_screening.csv and error.txt files to obtain the lists of removed files.

For more information about the dataset of background recordings, see `source_data/bgs/README.md`.


### Sound event recordings

The rare sound events are of the following classes: baby cry, glass break and gun shot. The recordings originate from freesound.org, are presented in their original form, and are accompanied in this dataset by annotations of the temporal occurrences of isolated events. All the events were screened by a human annotator and only the ones clearly corresponding to the target class were retained (e.g. original recordings of baby cries included also sounds of baby sighs, coughs etc., which were discarded). The unique event counts are the following (for training and test subsets, respectively):

- baby cry: 106; 42
- glass break: 96; 43
- gun shot: 134; 53

The isolated sound events were collected from freesound.org in the following manner. All the recordings matching the target class name query and with a sampling rate >= 44100 Hz were downloaded from freesound.org using the API with python wrapper [1]. The target sound events were thereupon isolated from the recordings using a two-step procedure. 

First, a semi-supervised segmentation [2] was performed with an SVM model trained to distingush between high-energy and low-energy short-term frames and then applied on the whole recording. A dynamic thresholding was used to detect the active segments.

The obtained segments were then analyzed by a human annotator, discarding the ones not belonging to the target class (baby coughs, unrealistically sounding gun shots e.g. laser guns etc.) The temporal annotations were then manually refined for all the isolated events with a step of 100 ms in such a way that there would not be abrupt clicks on the boundaries, but no silence regions before or after the events either.

Due to the nature of these sounds, there still might be regions of silence inside the annotated events (e.g. a baby cry consisting of two phrases, annotated as one cry). Providing a frame-level annotation on target event presence was deemed infeasible. However, an attempt was made to eliminate such events with pauses longer than one second. That is, the temporal annotations always indicate that with an error of 100 ms at most there is an onset or an offset of the target event, and within this region the event is either active all the time or might (at rare occasions) include a pause of at most one second.

The statistics of the duration of the isolated events in seconds are the following:

- babycry, max: 5.1, min: 0.66, mean: 2.25, std: 0.98;
- glassbreak, max: 4.54, min: 0.26, mean: 1.16, std: 0.71
- gunshot, max: 4.4, min: 0.24, mean: 1.32, std: 0.88.

The original freesound recordings are located at `source_data/events/[classname]/[fileid].wav` and are accompanied by a text file [`[fileid].yaml`] in the same location, which consists of the annotations of the isolated events (field `valid_segments` with start and end times in seconds), as well as other meta data about the recording, as provided on freesound, including the license. 


### Cross-validation setup

Meta files (`source_data/cv_setup/*devtrain.yaml` and `*devtest.yaml`) are provided indicating the cross-validation setup: lists of isolated events and background recordings split into training ("devtrain") and test ("devtest") subsets. 

The split of backgrounds was done in terms of recording location ID, according to the first fold of the DCASE 2016 task 1 setup (0.75+0.25, 844 training and 277 test files). The meta files provide additionally the acoustic scene class labels for all the backgrounds.

The sound events were split in terms of freesound.org usernames. The ratio of usernames was set to 0.71 devtrain vs. 0.29 devtest and the split was performed in such a way, that the isolated event counts are of a similar ratio (0.72+0.28 for baby cries, 0.69+0.31 for glass breaks, and 0.72+0.28 for gun shots). The meta files contain such fields as:
- filename of the original long recording 
- parent meta data (parent being the original freesound recording containing possibly several children - isolated events)
- timing of the current isolated event in the parent file (field `segment`).

### Mixtures

The parameters of the generated mixtures are the following:

- 500 mixtures per target event class.
- Event presence probability 0.5: this stands for generating 250 mixtures with target event present and 250 "mixtures" of only background, for each target class. This way, the rareness of the events and the detection nature of the task are facilitated.
- Event-to-background ratios (EBR) -6, 0 and 6 dBs. The EBR is defined as a ratio of average RMSE values calculated over the duration of the event and the corresponding background segment on which the event will be mixed, respectively.

The background instance, the event instance, the event timing in the mixture, its presence flag and the EBR value are all selected randomly and uniformly, allowing for a generation of infinite number of mixtures, which might, however, share the underlying source data. This is not an issue for the cross-validation setup, since the split is performed in terms of the origin of the underlying source data.

The creation of the mixtures is performed in two stages: generating mixture recipes and performing the mixing.

#### Generating mixture recipes

Mixture recipes (mixtures) are text files containing: 

- the file paths to the source background and event (if present),
- the event presence flag (some mixtures might not have any target events),
- the timing of the event in the original event recording (fields `segment_start_seconds`, `segment_end_seconds`), 
- the timing of the event in the mixture to be generated (`event_start_in_mixture_seconds`),
- the amplitude scaling factor of the event in the mixture (allowing for different event-to-background ratios, EBR)
- the corresponding EBR value,
- the name of the mixture audio file, constructed as a running id followed by the hash of the parameters that generate the mixture,
- the annotation string to accompany the generated audio. It includes the filename of the mixture, and, if the target event is present in the mixture, its start and end times and its label.
 
The format of the annotation string is the following:

    [audio file (string)][tab][start time seconds][tab][end time seconds][tab][event class label]  # if event is present
	[audio file (string)]  # if no event is present
	
The recipes are generated randomly, but with a fixed seed of the random generator, allowing reproducibility. 

Along with the recipes, event list files are generated, consisting of annotation strings, defined above, for all the mixtures of the current subset. Those contain sufficient information for training from the mixtures. They also follow the submission format of the evaluation set predictions in DCASE 2017 task 2.

#### Generating mixtures

The mixtures are generated by going through the mixture recipes and summing the backgrounds with the corresponding event signals according to the recipes. For the source files with sampling rate different from the target 44100 Hz (event recordings were allowed to be of a higher sampling rate), resampling is performed prior to the summation.
To avoid clipping, the mixtures are scaled with a factor of 0.2 (value found experimentally suitable for the given dataset and mixture parameters). All the mixtures are scaled, not just the clipping ones, so that the dynamics would be preserved. To avoid introducing quantization noise, the files are saved in 24 bit format.

#### Mixture synthesizer software

A software is provided, which, given the default parameters, produces exactly the same mixture recipes and audio mixture files, as in this dataset. It also allows for tuning the parameters in order to obtain larger and more challenging training datasets: number of mixtures, EBR values and event presence probabilities are adjustable. Both devtrain and devtest datasets can be generated with different parameters, however, in the challenge, reporting the performance evaluated on the devtest dataset is naturally to be done with the provided devtest dataset with the default parameters.

The latest version of the mixture generation software is available at <http://github.com/TUT-ARG/TUT_Rare_sound_events_mixture_synthesizer>. 

### File structure

```
README.md			this file, markdown-format
README.html			this file, html-format
data				data folder (source, recipes, mixtures)
└───mixture_data	mixture recipes and mixture audio files
│   │  	EULA.pdf	End user license agreement for the mixture data
│   └───devtest		development set, test subset
│   │    └───20b255387a2d0cddc0a3dff5014875e7	default mixing parameter hash
│   │       └───meta
│   │       │   │   mixture_recipes_devtest_babycry.yaml
│   │       │   │   ...
│   │       │   │   event_list_devtest_babycry.csv	
│   │       │       ...
│   │       └───audio							mixture audio files
│   │           │   mixture_devtest_babycry_000_b8da9d93e4223b58e7b2117a9b4ac436.wav	
│   │           │   ...
│   │         
│   └───devtrain	development set, training subset
│       └───20b255387a2d0cddc0a3dff5014875e7	default mixing parameter hash│
│           └───meta
│           │   │   mixture_recipes_devtrain_babycry.yaml
│           │   │   ...
│           │   │   event_list_devtrain_babycry.csv	
│           │       ...
│           └───audio							mixture audio files
│               │   mixture_devtrain_babycry_000_07a75692b15446e9fbf6cc3afaf96097.wav
│               │   ...
│   
└───source_data
│   │
│   └───bgs							Background dataset
│   │   │   README.md				Detailed description of the original background dataset
│   │  	│  	EULA.pdf				End user license agreement for the background data
│   │   │   bg_screening.csv
│   │   │   error.txt
│   │   └───audio									
│   │       │   a001_0_30.wav		
│   │       │   ...
│   │    
│   └───cv_setup				Cross-vaildation setup: info on source data splits
│       │   bgs_devtest.yaml
│       │   bgs_devtrain.yaml
│       │   events_devtest.yaml
│       │ 	events_devtrain.yaml
│               
└───────events						Original freesound recordings, with licesnses provided file-wise
│       └───────babycry
│       │       │   31527.wav		Filename = freesound file id
│       │       │   31527.yaml		meta file with timing of isolated events, license information etc.
│       │       │   ...
│       │      
│       └───────glassbreak
│       │       │   ...
│       │     
│       └───────gunshot
│               │   ...
│  
TUT_Rare_sound_events_mixture_synthesizer
│   EULA.pdf
│	core.py									core generation programme
│	generate_devtest_mixtures.py			programme for generating devtest mixtures
│	generate_devtrain_mixtures.py			programme for generating devtrain mixtures
│	mixing_params_devtest_dcase_fixed.yaml	parameter file for devtest mixtures as used in DCASE 2017 challenge
│	mixing_params.yaml						parameter file for devtrain mixtures, initially same as above, but tunable
│	requirements.txt						required packages	
``` 


2. Usage
========

The simplest suggested use-case is to work directly on the provided mixtures: train classifiers on the annotated (e.g. `mixture_data/devtrain/meta/event_list_devtrain_babycry.csv`) segments of mixture audio (e.g. `mixture_data/devtrain/audio/mixture_devtrain_babycry_*.wav`) with target class present vs. background-only. Evaluate the performance on the data from `devtest` subset.

For more advanced scenarios, use the provided source data, following the cross-validation setup to obtain train/test splits. To generate mixtures of various quantities, EBR values etc., use the provided software `TUT_Rare_sound_events_mixture_synthesizer`. To generate your own devtrain set, specify the parameters in `TUT_Rare_sound_events_mixture_synthesizer/mixing_params.yaml` and then run:

	python generate_devtrain_mixtures.py
	
(assuming the data folder is located at `../data` relatively to the synthesizer folder). The full command is:

	python generate_devtrain_mixtures.py -data_path '../data' -params mixing_params.yaml

For more details, see the help section of the programme (`python generate_devtrain_mixtures.py --help`).

Similarly, one can generate own devtest mixtures (`generate_devtest_mixtures.py`). Note, however, that reporting the results in DCASE 2017 challenge requires the devtest data to be exactly as provided in this dataset (as generated with parameters `mixing_params_devtest_dcase_fixed.yaml`).

3. License
==========

The dataset components are licensed in the following manner:

- Target sound event recordings (`source_data/events`) are accompanied by the license information on a per-file basis: for each `*.wav` file see the corresponding `*.yaml` file with information about the author and the license. Such licenses as CC BY-NC 3.0, CC BY 3.0, Sampling Plus 1.0 and CC0 1.0 are applicable, depending on the file.
- Source background recordings are licensed under the EULA.pdf file at `source_data/bgs/EULA.pdf`.
- The generated mixtures are licensed under the EULA.pdf file at `mixture_data/EULA.pdf`.
- The mixture sets use many sounds from freesound, for the full list with attribution see files: `source_data/cv_setup/events_devtrain.yaml` and `source_data/cv_setup/events_devtest.yaml`.
- The TUT_Rare_sound_events_mixture_synthesizer software is licensed under EULA.pdf at `TUT_Rare_sound_events_mixture_synthesizer/EULA.pdf`.



4. References
=============

[1] https://github.com/xavierfav/freesound-python

[2] Giannakopoulos T (2015) pyAudioAnalysis: An Open-Source Python Library for Audio Signal Analysis. PLoS ONE 10(12): e0144610. doi:10.1371/journal.pone.0144610
