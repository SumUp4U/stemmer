# coding=utf-8
""" Stemming for russian texts """
import argparse
import datetime
import logging
import os
import time

from pymystem3 import Mystem

# Creating stemmer instance take lot of time and resources, so we create it once
# if you use multithreading create instance in every thread and pass to  stemming function

main_stemmer = Mystem()

# if you use multithreading create instance in every thread and pass to  stemming function

def parse_args(test_args=None):
    """ Argument parser. ['-v', 'DEBUG'] for console testing
    Args:
        test_args(Optional[list]): Use for testing purposes. Defaults to None.
            Used instead of command line arguments
    Returns:
        argparse.Namespace: Command line args if test_args = None, parsed test_args otherwise
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-L',
        choices=['FATAL', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
        dest='logging_level',
        nargs='?',
        const='INFO', default='INFO',
        help='Set logging level. Default value - INFO'
    )
    parser.add_argument(
        'in_file',
        help='Input file'
    )
    parser.add_argument(
        'out_file',
        nargs='?',
        const='', default='',
        help='Output file'
    )
    if test_args:
        return parser.parse_args(test_args)
    else:
        return parser.parse_args()


def cleaning(text):
    """Change stop words in text to spaces

    Args:
        text(str): Text for cleaning

    Returns:
        str: Clean text
    """

    def replace(words, text, with_spaces=True):
        for word in words:
            if with_spaces:
                word = ' {} '.format(word)
            if word in text:
                text = text.replace(word, ' ')
        return text

    stop_words = {
        'вы', 'a', 'из-под', 'on', 'n', 'ая', 'только', 'ст', 'ъ', 'l', 'из', 'at', 'до', 'not', 'и', 'б', 'из-за',
        'кто', 'е', 'сам', 'хх', 'об', 'd', 'вот', 'c', 'of', 'v', 'т', 'над', 'тогда', 'по', 'даже', 'e', 'бо', 'м',
        'r', 'этот', 'шт', 'еще', 'чтобы', 'тоже', 'to', 'вне', 'она', 'его', 'stream', 'или', 'то', 'ага', 'ч', 'на',
        'i', 'да', 'там', 'куда', 'o', 'многий', 'х', 'я', 'вб', 'xxx', 'мо', 'э', 'usd', 'как', 'их', 'g', 'в', 'p',
        'что', 'также', 'ее', 'данный', 'это', 'й', 'н', 'are', 'm', 'при', 'and', 'же', 'за', 'для', 'др', 'о', 'а',
        'or', 'b', 'никакой', 'оно', 'от', 'анк', 'с', 'эд', 'предыдущий', 'ас', 'ти', 's', 'ми', 'ф', 'какой',
        'второй', 'тц', 'in', 'пвх', 'юрий', 'ю', 'д', 'к', 'р', 'ед', 'вообще', 'ср', 'тот', 'ххх', 'by', 'пр', 'ж',
        'for', 'либо', 'п', 'он', 'прежде', 'г', 'который', 'from', 'гг', 'ар', 'но', 'ли', 'тыс', 'со', 'у', 'л', 'ц',
        'де', 'de', 'the'
    }

    symbols = {
        '»', '"', '^', '!', '—', '§', '◦', '▪', '\uf0d8', ',', '-', '@', '=', '€', '‒', '“', '?', '/', '\uf0f1',
        '\uf0a7', ']', '\u200b', '\uf0b7', '\uf02d', ':', '№', '[', '–', '(', '…', ' ', '*', '+', ';', '↑', '•', '%',
        '’', '«', '_', '.', '~', '|', '©', '”', '·', ')'
    }

    text = text.lower()  # convert to lower. need for non russian chars
    text = replace(symbols, text, with_spaces=False)
    text = replace(stop_words, text)
    return text


def stemming(text, stemmer=main_stemmer):
    """

    Args:
        text(str): Text for stemming
        stemmer(pymystem3.Mystem) : stemmer instance

    Returns:
        str:  output produced by stemming lib
    """
    return ''.join(stemmer.lemmatize(text))


def main(in_name, out_name):
    if not out_name:
        out_name = '{}.stemmed'.format(in_name)
    with open(in_name) as in_f, open(out_name, 'w') as out_f:
        text = in_f.read()
        cleaned_text = cleaning(text)
        stemmed_text = stemming(cleaned_text)
        out_f.write(stemmed_text)


if __name__ == "__main__":
    start_time = time.time()
    args = parse_args()
    logging.basicConfig(
        level=args.logging_level,
        format='%(asctime)s %(name)s %(levelname)s: %(message)s',
        datefmt='%H:%M:%S',
    )
    logging.debug(args)
    try:
        main(args.in_file, args.out_file)
    except (KeyboardInterrupt, SystemExit):
        logging.info('Interrupt signal received')
    except Exception:
        logging.exception('Unhandled error happened')
    finally:
        execution_time = time.time() - start_time
        logging.info('Execution time: %s', datetime.timedelta(seconds=execution_time))
