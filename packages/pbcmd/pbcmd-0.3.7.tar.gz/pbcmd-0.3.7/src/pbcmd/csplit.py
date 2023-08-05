"""Split a compressed text file into multiple smaller (compressed) text files."""

import gzip
import bz2
import lzma
from itertools import islice

import click
from tqdm import tqdm

COMP_OPEN = {"gzip": gzip.open, "bz2": bz2.open, "xz": lzma.open, "text": open}
COMP_OPTION_TYPE = click.Choice(list(COMP_OPEN) + ["infer"])


@click.command()
@click.option(
    "-n",
    "--lines-per-file",
    default=1000,
    show_default=True,
    help="Maximum number of lines per output file",
)
@click.option(
    "-e",
    "--encoding",
    default="utf-8",
    show_default=True,
    help="Text encoding of input and output files",
)
@click.option(
    "-c",
    "--input-compression",
    default="infer",
    show_default=True,
    type=COMP_OPTION_TYPE,
    help="Compression format of the input file",
)
@click.option(
    "-d",
    "--output-compression",
    default="infer",
    show_default=True,
    type=COMP_OPTION_TYPE,
    help="Compression format of output files",
)
@click.argument("input-file")
@click.argument("output-file-format")
def csplit(
    lines_per_file,
    encoding,
    input_compression,
    output_compression,
    input_file,
    output_file_format,
):
    """Split a large compressed text file into multiple smaller (compressed) text files.

    {index} in output_file_format will be replaced by index of the output file.
    index of output files start from 0
    """
    if input_compression == "infer":
        if input_file.endswith(".gz"):
            input_compression = "gzip"
        elif input_file.endswith(".bz2"):
            input_compression = "bz2"
        elif input_file.endswith(".xz"):
            input_compression = "xz"
        else:
            input_compression = "text"

    if output_compression == "infer":
        if output_file_format.endswith(".gz"):
            output_compression = "gzip"
        elif output_file_format.endswith(".bz2"):
            output_compression = "bz2"
        elif output_file_format.endswith(".xz"):
            output_compression = "xz"
        else:
            output_compression = "text"

    if "{index}" not in output_file_format:
        raise click.UsageError("Output file format string doesn't contain '{index}'")

    in_open = COMP_OPEN[input_compression]
    out_open = COMP_OPEN[output_compression]

    with in_open(input_file, mode="rt", encoding=encoding) as fin:
        fin = iter(fin)
        index = 0

        obar = tqdm(desc="Writing file")
        while True:
            lines = list(islice(fin, lines_per_file))
            if not lines:
                obar.close()
                return

            ibar = tqdm(lines, desc="Writing line", leave=False)

            output_file = output_file_format.format(index=index)
            with out_open(output_file, mode="wt", encoding=encoding) as fout:
                for line in ibar:
                    fout.write(line)
            index += 1
            obar.update(1)


if __name__ == "__main__":
    csplit()
