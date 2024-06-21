#!/usr/bin/env python
import typing as t
from time import perf_counter 
from dataclasses import dataclass
import linecache as lc # https://stackoverflow.com/a/620397
import click


type Seconds = float 

@dataclass
class MathResults:
    mean: int
    minimal: int
    maximal: int
    median: float 
    largest_inreasing_sequence: t.List[int]
    largest_decreasing_sequence: t.List[int]
    exec_time: Seconds


class BufferedReader:
    """Batch reader for file"""

    def __init__[T](self,
                 filename: str,
                 transform: t.Callable[str, T] = None):
        """Initialize file reader.
        ...

        Parameters
        ----------
        filename : str
            name of the file containing data
        transform : Callable[str, T]
            something like a lambda function
            which is applied to each line when reading file
        """
            
        self.__transform = transform if transform else lambda x: x
        self.__file = None
        self.__fname = filename
        
    def __enter__(self, ):
        if not self.__file:
            self.__file = open(self.__fname, mode='r')
        return self.get_line_reader()
    
    def __exit__(self, type, value, traceback):
        self.__file.close()
    
    def get_line_reader[T](self) -> t.Generator[t.List[T], None, None]:
        for line in self.__file:
            yield self.__transform(line)


def handle_calculations(filename) -> MathResults:
    nmax = None
    nmin = None
    nsum = 0
    linecount = 0

    largest_inc_seq = []
    largest_dec_seq = []

    current_inc_seq = []
    current_dec_seq = []

    tstart = perf_counter()
    with BufferedReader(filename, lambda x: int(x)) as reader:
        l = next(reader)
        nmax = nmin
        linecount = 1
        nsum = int(l)

        largest_inc_seq = current_inc_seq = [l]
        largest_dec_seq = current_dec_seq = [l]

        for l in reader:
            nsum += l
            linecount += 1
            if not nmax or l > nmax:
                nmax = l
            if not nmin or l < nmin:
                nmin = l

            if current_dec_seq[-1] > l:
                current_dec_seq.append(l)
            else:
                current_dec_seq = [l]

            if current_inc_seq[-1] < l:
                current_inc_seq.append(l)
            else:
                current_inc_seq = [l]

            if len(largest_inc_seq) < len(current_inc_seq):
                largest_inc_seq = current_inc_seq
            if len(largest_dec_seq) < len(current_dec_seq):
                largest_dec_seq = current_dec_seq

    mean = round(nsum / linecount, 3)
    ln = round(linecount / 2)
    median = int(lc.getline(filename, ln))
    if linecount % 2 == 0:
        median = (median + int(lc.getline(filename, ln + 1))) / 2

    return MathResults(
        mean,
        nmin,
        nmax,
        median,
        largest_inc_seq,
        largest_dec_seq,
        round(float(perf_counter() - tstart), 5),
    )
    


@click.group('main')
def cmd_main():
    ...


@cmd_main.command('start')
@click.option('-f', '--filename',
              required=True,
              prompt="Enter file path",
              help="File name to perform calculations for")
@click.option('-o', '--save-to-file',
              default=None,
              required=False)
def start_script(filename: str, save_to_file: str):
    result = handle_calculations(filename)
    result_string = f"""
    Mean: {result.mean}
    Min: {result.minimal}
    Max: {result.maximal}
    Median: {result.median}
    Largest Increasing Sequence: {result.largest_inreasing_sequence}
    Largest Decreasing Sequence: {result.largest_decreasing_sequence}

    Execution time: {result.exec_time} s
    """

    if save_to_file:
        with open(save_to_file, 'w') as file:
            file.write(result_string)
            return

    print(result_string)



if __name__ == "__main__":
    cmd_main()
