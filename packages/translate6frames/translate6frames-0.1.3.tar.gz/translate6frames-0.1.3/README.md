Useful tool to translate gene sequences to protein sequences

# Description
    
This tool consists one module:

- `translate6frames`: tool to translate gene sequences to protein sequences (all 6 frames)

# Installation
 
## Normal installation

```bash
pip install translate6frames
```

## Development installation

```bash
git clone https://github.com/khaledianehdieh/translate6frames.git
```

## Usage

```bash
python3
>>> from translate6frames import translate6frames as TF
>>> p= TF.translate6frames(FASTA_FILE, TYPE) # FASTA_FILE is the input gene file, the TYPE is "DNA", or "RNA"
>>> p.Output() # returns 6 fasta files, one for each frame (direct/reverse), and a csv file that contains all 6 frames in 6 columns

```
