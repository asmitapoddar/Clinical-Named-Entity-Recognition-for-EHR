######################################################################
#  CliNER - train.py                                                 #
#                                                                    #
#  Willie Boag                                      wboag@cs.uml.edu #
#                                                                    #
#  Purpose: Build model for given training data.                     #
######################################################################


import os
import os.path
import glob
import argparse
import pickle
import sys

import tools
from model import ClinerModel
from notes.documents import Document

# base directory
CLINER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--txt",
        dest = "txt",
        help = "The files that contain the training examples",
    )
    parser.add_argument("--annotations",
        dest = "con",
        help = "The files that contain the labels for the training examples",
    )
    parser.add_argument("--val-txt",
        dest = "val_txt",
        help = "The files that contain the validation examples",
    )
    parser.add_argument("--val-annotations",
        dest = "val_con",
        help = "The files that contain the labels for the validation examples",
    )
    parser.add_argument("--test-txt",
        dest = "test_txt",
        help = "The files that contain the test examples",
    )
    parser.add_argument("--test-annotations",
        dest = "test_con",
        help = "The files that contain the labels for the test examples",
    )
    parser.add_argument("--model",
        dest = "model",
        help = "Path to the model that should be generated",
    )
    parser.add_argument("--log",
        dest = "log",
        help = "Path to the log file for training info",
        default = os.path.join(CLINER_DIR, 'models', 'train.log')
    )
    parser.add_argument("--use-lstm",
        dest = "use_lstm",
        help = "Whether to use an LSTM model",
        action = 'store_true',
        default = False
    )
    parser.add_argument("--format",
        dest = "format",
        help = "Data format ( i2b2 )"
    )


    # Parse the command line arguments
    args = parser.parse_args()

    # Error check: Ensure that file paths are specified
    if not args.txt:
        parser.print_help(sys.stderr)
        sys.stderr.write('\n\tError: Must provide text files\n')
        sys.stderr.write('\n')
        exit(1)
    if not args.con:
        parser.print_help(sys.stderr)
        sys.stderr.write('\n\tError: Must provide annotations for text files\n')
        sys.stderr.write('\n')
        exit(1)
    if not args.model:
        parser.print_help(sys.stderr)
        sys.stderr.write('\n\tError: Must provide valid path to store model\n')
        sys.stderr.write('\n')
        exit(1)
    modeldir = os.path.dirname(args.model)
    if (not os.path.exists(modeldir)) and (modeldir != ''):
        parser.print_help(sys.stderr)
        sys.stderr.write('\n\tError: Model dir does not exist: %s\n' % modeldir)
        sys.stderr.write('\n')
        exit(1)

    # A list of txt and concept file paths
    train_txt_files = glob.glob(args.txt)
    train_con_files = glob.glob(args.con)

    # data format
    if args.format:
        format = args.format

    # Must specify output format
    if args.format not in ['i2b2']:
        print >>sys.stderr, '\n\tError: Must specify output format'
        print >>sys.stderr,   '\tAvailable formats: i2b2'
        sys.stderr.write('\n')
        exit(1)


    # Collect training data file paths
    train_txt_files_map = tools.map_files(train_txt_files) 
    train_con_files_map = tools.map_files(train_con_files)

    training_list = []
    for k in train_txt_files_map:
        if k in train_con_files_map:
            training_list.append((train_txt_files_map[k], train_con_files_map[k]))

    # If validation data was specified
    if args.val_txt and args.val_con:
        val_txt_files = glob.glob(args.val_txt)
        val_con_files = glob.glob(args.val_con)

        val_txt_files_map = tools.map_files(val_txt_files) 
        val_con_files_map = tools.map_files(val_con_files)
        
        val_list = []
        for k in val_txt_files_map:
            if k in val_con_files_map:
                val_list.append((val_txt_files_map[k], val_con_files_map[k]))
    else:
        val_list=[]

    # If test data was specified
    if args.test_txt and args.test_con:
        test_txt_files = glob.glob(args.test_txt)
        test_con_files = glob.glob(args.test_con)

        test_txt_files_map = tools.map_files(test_txt_files)
        test_con_files_map = tools.map_files(test_con_files)

        test_list = []
        for k in test_txt_files_map:
            if k in test_con_files_map:
                test_list.append((test_txt_files_map[k], test_con_files_map[k]))
    else:
        test_list=[]

    # Train the model
    train(training_list, args.model, args.format, args.use_lstm, logfile=args.log, val=val_list, test=test_list)




def train(training_list, model_path, format, use_lstm, logfile=None, val=[], test=[]):

    # Read the data into a Document object
    train_docs = []
    for txt, con in training_list:
        doc_tmp = Document(txt,con)
        train_docs.append(doc_tmp)

    val_docs = []
    for txt, con in val:
        doc_tmp = Document(txt,con)
        val_docs.append(doc_tmp)

    test_docs = []
    for txt, con in test:
        doc_tmp = Document(txt,con)
        test_docs.append(doc_tmp)

    # file names
    if not train_docs:
        print( 'Error: Cannot train on 0 files. Terminating train.')
        return 1

    # Create a Machine Learning model
    model = ClinerModel(use_lstm)

    # Train the model using the Documents's data
    model.train(train_docs, val=val_docs, test=test_docs)

    # Pickle dump
    print('\nserializing model to %s\n' % model_path)
    with open(model_path, "wb") as m_file:
        pickle.dump(model, m_file)
        
    model.log(logfile   , model_file=model_path)
    model.log(sys.stdout, model_file=model_path)
    


if __name__ == '__main__':
    main()
