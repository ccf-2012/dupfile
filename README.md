# dupfile
* Hard link items in dir A to dir B, with history cached.

> script write for Dai-lo Maolin


## Usage
```sh
python3 dupfile.py -h 
```

```
usage: dupfile.py [-h] -i input_path -o output_path [-s] [-c]

Hard link files to another dir

optional arguments:
  -h, --help            show this help message and exit
  -i input_path, --input-path input_path
                        File or Folder which to be hardlinked
  -o output_path, --output-path output_path
                        Directory as hardlink destination
  -s, --single-dir      Optional. Indicates whether to search for all the items inside the input
                        directory
  -c, --clear-log       Optional. less ouput log message
```

## Example
```sh
python3 dupfile.py -i /home/ccf2012/Downloads/  -o /home/ccf2012/MyLib/
```

