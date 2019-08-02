######################################################################
#  CliNER - predict.py                                               #
#                                                                    #
#  Willie Boag                                      wboag@cs.uml.edu #
#                                                                    #
#  Purpose: Use trained model to predict concept labels for data.    #
######################################################################

import os
import sys
import glob
import argparse
import itertools
import pickle

import tools
from model import ClinerModel, write
from notes.documents import Document
import copy

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--txt",
        dest = "txt",
        help = ".txt files of discharge summaries",
    )
    parser.add_argument("--out",
        dest = "output",
        help = "The directory to write the output",
    )
    parser.add_argument("--model",
        dest = "model",
        help = "The model to use for prediction",
    )
    parser.add_argument("--format",
        dest = "format",
        help = "Data format (i2b2)",
    )

    args = parser.parse_args()

    # Error check: Ensure that file paths are specified
    if not args.txt:
        parser.print_help(sys.stderr)
        sys.stderr.write('\n\tError: Must provide text files\n\n')
        sys.stderr.write('\n')
        exit(1)
    if not args.output:
        parser.print_help(sys.stderr)
        sys.stderr.write('\n\tError: Must provide output directory\n\n')
        sys.stderr.write('\n')
        exit(1)
    if not args.model:
        parser.print_help(sys.stderr)
        sys.stderr.write('\n\tError: Must provide path to model\n\n')
        sys.stderr.write('\n')
        exit(1)
    if not os.path.exists(args.model):
        parser.print_help(sys.stderr)
        sys.stderr.write('\n\tError: ClinerModel does not exist: %s\n\n' % args.model)
        sys.stderr.write('\n')
        exit(1)

    #Parse arguments
    files = glob.glob(args.txt)
    tools.mkpath(args.output)

    if args.format:
        format = args.format
    else:
        parser.print_help(sys.stderr)
        sys.stderr.write('\n\tERROR: must provide "format" argument\n\n')
        exit(1)

    # Predict
    predict(files, args.model, args.output, format=format)


def predict(files, model_path, output_dir, format, use_lstm=True):

    # Must specify output format
    if format not in ['i2b2']:
        sys.stderr.write('\n\tError: Must specify output format\n')
        sys.stderr.write('\tAvailable formats: i2b2\n')
        sys.stderr.write('\n')
        exit(1)

    # Load model
    #if use_lstm==False: 
    with open(model_path, 'rb') as f:
    	model = pickle.load(f, encoding='latin1')

    if model._use_lstm:
        import helper_dataset as hd
        import DatasetCliner_experimental as Exp
        import entity_lstm as entity_model

        parameters=hd.load_parameters_from_file("LSTM_parameters.txt")  
        parameters['use_pretrained_model']=True

        temp_pretrained_dataset_adress=parameters['model_folder']+os.sep+"dataset.pickle"
        model._pretrained_dataset = pickle.load(open(temp_pretrained_dataset_adress, 'rb'))
        model._pretrained_wordvector=hd.load_pretrained_token_embeddings(parameters)
        model._current_model=None

        '''
        updating_notes=[]
        for i,txt in enumerate(sorted(files)):
           note=Document(txt)
           tokenized_sents  = note.getTokenizedSentences()
           updating_notes+=tokenized_sents
        print (updating_notes)
        fictional_labels= copy.deepcopy(tokenized_sents)
        for idx,x in enumerate(fictional_labels):
           for val_id,value in enumerate(x):
                fictional_labels[idx][val_id]='O'
        Datasets_tokens={}
        Datasets_labels={}
        Datasets_tokens['deploy']=tokenized_sents
        Datasets_labels['deploy']=fictional_labels
        dataset = Exp.Dataset() 
        token_to_vector=dataset.load_dataset(Datasets_tokens, Datasets_labels, "", parameters,token_to_vector=model._pretrained_wordvector, pretrained_dataset=model._pretrained_dataset)
        parameters['Feature_vector_length']=dataset.feature_vector_size
        parameters['use_features_before_final_lstm']=False       
        dataset.update_dataset("", ['deploy'],Datasets_tokens,Datasets_labels)
        model._pretrained_dataset=dataset
        model_LSTM=entity_model.EntityLSTM(dataset,parameters)
        model._current_model=model_LSTM
        ._current_model
        '''
        print ("END TEST")
        #exit()
        #model.parameters=None

    # Tell user if not predicting
    if not files:
        sys.stderr.write("\n\tNote: You did not supply any input files\n\n")
        exit()

    n = len(files)

    for i,txt in enumerate(sorted(files)):
        note = Document(txt)

        # Output file
        fname = os.path.splitext(os.path.basename(txt))[0] + '.' + 'con'
        out_path = os.path.join(output_dir, fname)

        #'''
        if os.path.exists(out_path):
            print('\tWARNING: prediction file already exists (%s)' % out_path)
            #continue
        #'''

        sys.stdout.write('%s\n' % ('-' * 30))
        sys.stdout.write('\n\t%d of %d\n' % (i+1,n))
        sys.stdout.write('\t%s\n\n' % txt)

        # Predict concept labels
        labels = model.predict_classes_from_document(note)

        # Get predictions in proper format
        output = note.write(labels)

        # Output the concept predictions
        sys.stdout.write('\n\nwriting to: %s\n' % out_path)
        with open(out_path, 'w') as f:
            write(f, '%s\n' % output)
        sys.stdout.write('\n')


if __name__ == '__main__':
    main()
