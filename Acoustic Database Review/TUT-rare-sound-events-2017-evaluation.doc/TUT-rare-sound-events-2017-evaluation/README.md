Title:  TUT Rare Sound events 2017, Evaluation dataset

TUT Rare Sound events 2017, Evaluation dataset
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


Dataset
=======

TUT Rare Sound events 2017, evaluation dataset consists of source files for creating mixtures of rare sound events with background audio, as well a set of readily generated mixtures and recipes for generating them.

The "source" part of the dataset consists of two subsets:

- background recordings from 15 different acoustic scenes,
- recordings with the target rare sound events from three classes, accompanied by annotations of their temporal occurrences.

The mixture set consists of 1500 mixtures (500 per target class, with half of the mixtures not containing any target class events).


### Background recordings

The background recordings are from 15 different acoustic scenes and are an almost exact copy of TUT Acoustic scenes 2016, evaluation dataset (see <https://zenodo.org/record/1040168>), with the exception of recordings naturally containing target class events, which were removed. When using the original version of the dataset, refer to the provided bg_screening.csv file to obtain the lists of removed files.

For more information about the dataset of background recordings, see `source_data/bgs/README.md`.


### Sound event recordings

The rare sound events are of the following classes: baby cry, glass break and gun shot. The recordings originate from freesound.org, are presented in their original form, and are accompanied in this dataset by annotations of the temporal occurrences of isolated events. All the events were screened by a human annotator and only the ones clearly corresponding to the target class were retained (e.g. original recordings of baby cries included also sounds of baby sighs, coughs etc., which were discarded). The unique event counts are the following:

- baby cry: 61
- glass break: 58
- gun shot: 76

The isolated sound events were collected from freesound.org in the following manner. All the recordings matching the target class name query and with a sampling rate >= 44100 Hz were downloaded from freesound.org using the API with python wrapper [1]. The target sound events were thereupon isolated from the recordings using a two-step procedure.

First, a semi-supervised segmentation [2] was performed with an SVM model trained to distinguish between high-energy and low-energy short-term frames and then applied on the whole recording. A dynamic thresholding was used to detect the active segments.

The obtained segments were then analyzed by a human annotator, discarding the ones not belonging to the target class (baby coughs, unrealistically sounding gun shots e.g. laser guns etc.) The temporal annotations were then manually refined for all the isolated events with a step of 100 ms in such a way that there would not be abrupt clicks on the boundaries, but no silence regions before or after the events either.

Due to the nature of these sounds, there still might be regions of silence inside the annotated events (e.g. a baby cry consisting of two phrases, annotated as one cry). Providing a frame-level annotation on target event presence was deemed infeasible. However, an attempt was made to eliminate such events with pauses longer than one second. That is, the temporal annotations always indicate that with an error of 100 ms at most there is an onset or an offset of the target event, and within this region the event is either active all the time or might (at rare occasions) include a pause of at most one second.

The statistics of the duration of the isolated events in seconds are the following:

- babycry, max: 4.82, min: 0.48, mean: 1.80, std: 0.99
- glassbreak, max: 2.16, min: 0.24, mean: 0.85, std: 0.41
- gunshot, max: 2.28, min: 0.20, mean: 0.83, std: 0.58

The original freesound recordings are located at `source_data/events/[classname]/[fileid].wav` and are accompanied by a text file [`[fileid].yaml`] in the same location, which consists of the annotations of the isolated events (field `valid_segments` with start and end times in seconds), as well as other meta data about the recording, as provided on freesound, including the license.

### Mixtures

The parameters of the generated mixtures are the following:

- 500 mixtures per target event class.
- Event presence probability 0.5: this stands for generating 250 mixtures with target event present and 250 "mixtures" of only background, for each target class. This way, the rareness of the events and the detection nature of the task are facilitated.
- Event-to-background ratios (EBR) -6, 0 and 6 dBs. The EBR is defined as a ratio of average RMSE values calculated over the duration of the event and the corresponding background segment on which the event will be mixed, respectively.

The background instance, the event instance, the event timing in the mixture, its presence flag and the EBR value are all selected randomly and uniformly, allowing for a generation of infinite number of mixtures, which might, however, share the underlying source data. Therefore, this dataset is not suited to be split into training and test subsets. Instead, the
separately released Development dataset should be used for training (see <https://zenodo.org/record/401395>). The underlying
source data in devtrain, devtest subsets of the Development set as well as of the current Evaluation set is different
(in terms of locations of the backgrounds and usernames of the sound event files).

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

Along with the recipes, event list files are generated, consisting of annotation strings, defined above, for all the mixtures of the current subset.

#### Generating mixtures

The mixtures are generated by going through the mixture recipes and summing the backgrounds with the corresponding event signals according to the recipes. For the source files with sampling rate different from the target 44100 Hz (event recordings were allowed to be of a higher sampling rate), resampling is performed prior to the summation.
To avoid clipping, the mixtures are scaled with a factor of 0.2 (value found experimentally suitable for the given dataset and mixture parameters). All the mixtures are scaled, not just the clipping ones, so that the dynamics would be preserved. To avoid introducing quantization noise, the files are saved in 24 bit format.

#### Mixture synthesizer software

A software is provided, which, given the default parameters, produces exactly the same mixture recipes and audio mixture files, as in this dataset. It also allows for tuning the parameters in order to obtain larger datasets: number of mixtures, EBR values and event presence probabilities are adjustable.

The latest version of the mixture generation software is available at <http://github.com/TUT-ARG/TUT_Rare_sound_events_mixture_synthesizer>.

### File structure

```
README.md                  this file, markdown-format
README.html                this file, html-format
data                       data folder (source, recipes, mixtures)
└───mixture_data           mixture recipes and mixture audio files
│   │  EULA.pdf            End user license agreement for the mixture data
│   └───evaltest           evaluation set, test subset
│        └───bbb81504db15a03680a0044474633b67  mixing parameter hash
│           └───meta
│           │   │   mixture_recipes_evaltest_babycry.yaml
│           │   │   ...
│           │   │   event_list_evaltest_babycry.csv
│           │       ...
│           └───audiomixture audio files
│               │   mixture_evaltest_babycry_000_35c7bc20a21ec8fbb7097c6fb71487b5.wav
│               │   ...
│      
└───source_data
│   │
│   └───bgs                 Background dataset
│   │   │   README.md       Detailed description of the original background dataset
│   │   │  EULA.pdf         End user license agreement for the background data
│   │   │   bg_screening.csv
│   │   └───audio
│   │       │   1.wav
│   │       │   ...
│   │    
│   └───cv_setup             Cross-vaildation setup (as part of the cominded Development and Evaluation dataset)
│       │   bgs_evaltest.yaml
│       │   events_evaltest.yaml
│               
└───────events               Original freesound recordings, with licesnses provided file-wise
│       └───────babycry
│       │       │   13801.wav          Filename = freesound file id
│       │       │   13801.yamlmeta     file with timing of isolated events, license information etc.
│       │       │   ...
│       │      
│       └───────glassbreak
│       │       │   ...
│       │     
│       └───────gunshot
│               │   ...
│  
TUT_Rare_sound_events_mixture_synthesizer
│ EULA.pdf
│core.py                          core generation programme
│generate_evaltest_mixtures.py    programme for generating evaltest mixtures
│mixing_params_evaltest.yaml      parameter file for evaltest mixtures as used in DCASE 2017 challenge
│requirements.txt                 required packages
```


Usage
=====

The simplest suggested use-case is to work directly on the provided mixtures.

For more advanced scenarios, use the provided source data. To generate mixtures of various quantities, EBR values etc., use the provided software `TUT_Rare_sound_events_mixture_synthesizer`. To generate your own evaltest set, specify the parameters in `TUT_Rare_sound_events_mixture_synthesizer/mixing_params_evaltest.yaml` and then run:

python generate_evaltest_mixtures.py

(assuming the data folder is located at `../data` relatively to the synthesizer folder). The full command is:

python generate_evaltest_mixtures.py -data_path '../data' -params mixing_params_evaltest.yaml

For more details, see the help section of the programme (`python generate_evaltest_mixtures.py --help`).

License
=======

The dataset components are licensed in the following manner:

- Target sound event recordings (`source_data/events`) are accompanied by the license information on a per-file basis: for each `*.wav` file see the corresponding `*.yaml` file with information about the author and the license. Such licenses as CC BY-NC 3.0, CC BY 3.0, Sampling Plus 1.0 and CC0 1.0 are applicable, depending on the file.
- Source background recordings are licensed under the EULA.pdf file at `source_data/bgs/EULA.pdf`.
- The generated mixtures are licensed under the EULA.pdf file at `mixture_data/EULA.pdf`.
- The mixture sets use many sounds from freesound, for the full list with attribution see file: `source_data/cv_setup/events_evaltest.yaml`.
- The TUT_Rare_sound_events_mixture_synthesizer software is licensed under EULA.pdf at `TUT_Rare_sound_events_mixture_synthesizer/EULA.pdf`.



References
==========

[1] https://github.com/xavierfav/freesound-python-tools

[2] Giannakopoulos T (2015) pyAudioAnalysis: An Open-Source Python Library for Audio Signal Analysis. PLoS ONE 10(12): e0144610. doi:10.1371/journal.pone.0144610
