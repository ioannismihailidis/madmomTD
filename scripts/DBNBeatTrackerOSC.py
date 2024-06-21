#!/usr/bin/env python
# encoding: utf-8
"""
DBNBeatTracker beat tracking algorithm.

"""

from __future__ import absolute_import, division, print_function

import argparse

from madmom.audio import SignalProcessor
from madmom.features import (ActivationsProcessor, DBNBeatTrackingProcessor,
                             RNNBeatProcessor)
from madmom.ml.nn import NeuralNetworkEnsemble
from madmom.processors import IOProcessor, io_arguments
from pythonosc import udp_client

_oscClient = None
_beats = 0
def write_beats(beats, filename, fmt=None, delimiter='\t', header=None):
    global _oscClient, _beats
    """
    Write the beats to a file.

    Parameters
    ----------
    beats : numpy array
        Beats to be written to file.
    filename : str or file handle
        File to write the beats to.
    fmt : str or sequence of strs, optional
        A single format (e.g. '%.3f'), a sequence of formats (e.g.
        ['%.3f', '%d']), or a multi-format string (e.g. '%.3f %d'), in which
        case `delimiter` is ignored.
    delimiter : str, optional
        String or character separating columns.
    header : str, optional
        String that will be written at the beginning of the file as comment.

    """
    if fmt is None and beats.ndim == 2:
        fmt = ['%.3f', '%d']
    elif fmt is None:
        fmt = '%.3f'
    if len(beats)==1:
        _beats = (_beats + 1) % 4
        #print("BEAT")
        _oscClient.send_message("/beat", _beats)
    #write_events(beats, filename, fmt, delimiter, header)

def main():
    global _oscClient, _beats
    """DBNBeatTracker"""

    # define parser
    p = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description='''
    The DBNBeatTracker program detects all beats in an audio file according to
    the method described in:

    "A Multi-Model Approach to Beat Tracking Considering Heterogeneous Music
     Styles"
    Sebastian Böck, Florian Krebs and Gerhard Widmer.
    Proceedings of the 15th International Society for Music Information
    Retrieval Conference (ISMIR), 2014.

    It does not use the multi-model (Section 2.2.) and selection stage (Section
    2.3), i.e. this version corresponds to the pure DBN version of the
    algorithm for which results are given in Table 2.

    Instead of the originally proposed state space and transition model for the
    DBN, the following is used:

    "An Efficient State Space Model for Joint Tempo and Meter Tracking"
    Florian Krebs, Sebastian Böck and Gerhard Widmer.
    Proceedings of the 16th International Society for Music Information
    Retrieval Conference (ISMIR), 2015.

    This program can be run in 'single' file mode to process a single audio
    file and write the detected beats to STDOUT or the given output file.

      $ DBNBeatTracker single INFILE [-o OUTFILE]

    If multiple audio files should be processed, the program can also be run
    in 'batch' mode to save the detected beats to files with the given suffix.

      $ DBNBeatTracker batch [-o OUTPUT_DIR] [-s OUTPUT_SUFFIX] FILES

    If no output directory is given, the program writes the files with the
    detected beats to the same location as the audio files.

    The 'pickle' mode can be used to store the used parameters to be able to
    exactly reproduce experiments.

    ''')
    # version
    p.add_argument('--version', action='version', version='DBNBeatTracker.2016')
    # input/output options
    io_arguments(p, output_suffix='.beats.txt', online=True)
    ActivationsProcessor.add_arguments(p)
    # signal processing arguments
    SignalProcessor.add_arguments(p, norm=False, gain=0)
    # peak picking arguments
    DBNBeatTrackingProcessor.add_arguments(p)
    NeuralNetworkEnsemble.add_arguments(p, nn_files=None)

    p.add_argument("--osc_serverip", default="127.0.0.1", help="The ip of the OSC server")
    p.add_argument("--osc_serverport", type=int, default=7000, help="The port the OSC server is listening on")

    # parse arguments
    args = p.parse_args()

    # set immutable arguments
    args.fps = 100

    _beats = 0
    _oscClient = udp_client.SimpleUDPClient(args.osc_serverip, args.osc_serverport)
    
    # print arguments
    if args.verbose:
        print(args)

    # input processor
    if args.load:
        # load the activations from file
        in_processor = ActivationsProcessor(mode='r', **vars(args))
    else:
        # use a RNN to predict the beats
        in_processor = RNNBeatProcessor(**vars(args))

    # output processor
    if args.save:
        # save the RNN beat activations to file
        out_processor = ActivationsProcessor(mode='w', **vars(args))
    else:
        # track the beats with a DBN and output them
        beat_processor = DBNBeatTrackingProcessor(**vars(args))
        out_processor = [beat_processor, write_beats]

    # create an IOProcessor
    processor = IOProcessor(in_processor, out_processor)

    # and call the processing function
    args.func(processor, **vars(args))


if __name__ == '__main__':
    main()
